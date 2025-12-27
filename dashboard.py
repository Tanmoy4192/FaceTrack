import tkinter as tk
from tkinter import ttk
import sqlite3
import pandas as pd
from datetime import datetime
from config import DATABASE_PATH


class IPMASDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("IPMAS Attendance Dashboard")
        self.root.geometry("1000x500")

        # --- Table setup ---
        columns = (
            "Name",
            "First Entry",
            "Exit Count",
            "Total Outside Duration(s)",
            "Final Exit",
            "Current Status"
        )

        self.tree = ttk.Treeview(root, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # --- Manual refresh button ---
        refresh_btn = tk.Button(
            root,
            text="Refresh Data",
            command=self.load_data
        )
        refresh_btn.pack(pady=10)

        # --- Automatic refresh (every 5 seconds) ---
        self.refresh_interval_ms = 5000
        self.schedule_refresh()

    def schedule_refresh(self):
        self.load_data()
        self.root.after(self.refresh_interval_ms, self.schedule_refresh)

    def load_data(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect(DATABASE_PATH)

        try:
            df = pd.read_sql("SELECT * FROM attendance", conn)
        except Exception as e:
            print("[ERROR] Failed to load attendance data:", e)
            conn.close()
            return

        if df.empty:
            conn.close()
            return

        # Ensure expected columns are present
        for col in [
            "person_name",
            "entry_time",
            "exit_time",
            "outside_duration",
            "status"
        ]:
            if col not in df.columns:
                df[col] = None

        # Convert time columns safely
        df["entry_time"] = pd.to_datetime(df["entry_time"], errors="coerce")
        df["exit_time"] = pd.to_datetime(df["exit_time"], errors="coerce")

        # Process data per person
        grouped = df.groupby("person_name")

        for person, group in grouped:
            group = group.sort_values("entry_time")

            # First recorded entry
            first_entry = group["entry_time"].iloc[0].strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # Number of completed exits
            exit_count = group["exit_time"].notna().sum()

            # Total time spent outside
            total_outside = group["outside_duration"].fillna(0).sum()

            # Most recent exit
            final_exit = group["exit_time"].dropna().max()
            final_exit_str = (
                final_exit.strftime("%Y-%m-%d %H:%M:%S")
                if pd.notna(final_exit)
                else "Still inside"
            )

            # Determine current status
            last_row = group.iloc[-1]

            if pd.isna(last_row["exit_time"]):
                current_status = "Inside"

                # Live duration since last entry
                live_duration = (
                    datetime.now() - last_row["entry_time"]
                ).total_seconds()

                total_outside_str = (
                    f"{total_outside:.1f}s + "
                    f"{live_duration:.1f}s (ongoing)"
                )
            else:
                current_status = "Outside"
                total_outside_str = f"{total_outside:.1f}s"

            self.tree.insert(
                "",
                tk.END,
                values=(
                    person,
                    first_entry,
                    exit_count,
                    total_outside_str,
                    final_exit_str,
                    current_status
                )
            )

        conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = IPMASDashboard(root)
    root.mainloop()

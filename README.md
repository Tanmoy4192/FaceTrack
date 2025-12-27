<h1 align="center">FaceTrack</h1>
<h3 align="center">Intelligent Person Monitoring & Attendance System (IPMAS)</h3>

<p align="center">
  A real-time face recognition based monitoring and attendance system using
  <b>Python, OpenCV, and SQLite</b>.
</p>

<hr>

<h2>📌 Overview</h2>
<p>
FaceTrack (IPMAS) is a real-time computer vision project that detects and recognizes
faces from a live camera feed, automatically tracks entry and exit events, stores
attendance data in a database, and displays live status through a dashboard.
</p>

<hr>

<h2>🎥 Demo Video</h2>
<p>
A short demonstration of the FaceTrack system showing
real-time face recognition, entry-exit tracking, and the live dashboard.
</p>

<p>
<a href="(https://drive.google.com/file/d/1T4pjdmibuRkOpw-z2JiQy4dbWUG2J5lQ/view?usp=drive_link)" target="_blank">
▶ Click here to watch the demo video
</a>
</p>
<p>
<b>Note:</b> Video is hosted on Google Drive for faster playback.
</p>

<p>
This project demonstrates practical usage of
<b>computer vision, multithreading, database handling, and GUI development</b>.
</p>

<hr>

<h2>🚀 Key Features</h2>
<ul>
  <li>Real-time face detection and recognition</li>
  <li>Automatic entry and exit tracking</li>
  <li>New person registration via webcam</li>
  <li>Unknown / intruder face detection</li>
  <li>Multithreaded processing for better performance</li>
  <li>SQLite database for attendance storage</li>
  <li>Live Tkinter dashboard</li>
  <li>FPS and recognition latency display</li>
</ul>

<hr>

<h2>🧠 System Workflow</h2>
<ol>
  <li>Camera captures live video frames</li>
  <li>Frames are resized for performance</li>
  <li>Faces are detected and encoded</li>
  <li>Encodings are matched with known faces</li>
  <li>Entry and exit events are tracked</li>
  <li>Attendance data is stored in SQLite</li>
  <li>Dashboard displays live status</li>
</ol>

<hr>

<h2>📂 Project Structure</h2>

<pre>
FaceTrack/
├── main.py
├── dashboard.py
├── config.py
├── face_utils.py
├── tracking_utils.py
├── db_utils.py
├── setup_db.py
├── requirements.txt
├── README.md
└── data/
    ├── attendance.db
    ├── known_faces/
    ├── unknown_faces/
    └── intruders/
</pre>

<hr>

<h2>⚙️ Technologies Used</h2>
<ul>
  <li>Python</li>
  <li>OpenCV</li>
  <li>face_recognition (dlib)</li>
  <li>NumPy</li>
  <li>SQLite</li>
  <li>Tkinter</li>
  <li>Pandas</li>
  <li>Multithreading</li>
</ul>

<hr>

<h2>🛠️ Installation & Setup</h2>

<pre>
git clone https://github.com/Tanmoy4192/FaceTrack.git
cd FaceTrack
pip install -r requirements.txt
python setup_db.py
</pre>

<hr>

<h2> Running the Application</h2>

<pre>
python main.py
</pre>

<h3>Controls</h3>
<ul>
  <li><b>q</b> – Quit application</li>
  <li><b>r</b> – Register a new person</li>
</ul>

<hr>

<h2>📊 Dashboard</h2>

<pre>
python dashboard.py
</pre>

<p>The dashboard displays:</p>
<ul>
  <li>Person name</li>
  <li>First entry time</li>
  <li>Exit count</li>
  <li>Total outside duration</li>
  <li>Final exit time</li>
  <li>Current status</li>
</ul>

<hr>

<h2> Important Notes</h2>
<ul>
  <li>Ensure good lighting for accurate recognition</li>
  <li>Only one face should be visible during registration</li>
  <li>First run may take time to load models</li>
  <li>Camera source can be changed in <code>config.py</code></li>
</ul>

<hr>

<h2> Future Enhancements</h2>
<ul>
  <li>Web-based dashboard</li>
  <li>Email / SMS intruder alerts</li>
  <li>Cloud database integration</li>
  <li>Mask detection support</li>
</ul>

<hr>

<h2> Author</h2>
<p>
<b>Tanmoy Samanta</b><br>
Computer Vision | Python | AI & ML Enthusiast<br>
GitHub:
<a href="https://github.com/Tanmoy4192">https://github.com/Tanmoy4192</a>
</p>

<hr>

<h2> License</h2>
<p>
This project is created for <b>educational and learning purposes</b>.
</p>

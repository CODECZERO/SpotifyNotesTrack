# SpotifyNotesTrack
Got it! Let’s break down this **demo task** and how your Django + PostgreSQL project can be described according to the requirements. Here’s a clear explanation you can use in your **README or documentation**:

---

## **Project Overview**

**Project Name:** Spotify Notes Tracker (example)

This project is a **full-stack web application** built using **Python Django** with **PostgreSQL** (Supabase can be used optionally). It allows users to track notes on Spotify tracks, analyze their sentiment, and visualize note data.

The application demonstrates **CRUD operations**, **API integration**, and **data visualization** as required in the demo task.

---

### **Features Implemented**

1. **CRUD Functionality via REST APIs**

   * **Create Notes:** Users can add a note for a specific Spotify track.
   * **Read Notes:** Users can view all notes for a track.
   * **Update Notes:** Users can update existing notes.
   * **Delete Notes:** Users can remove notes.
   * APIs are implemented using Django views and can be called directly via REST clients like Postman.

2. **API Integration**

   * Integrated with **Spotify API** to fetch:

     * User’s top tracks
     * Track details including album cover and artist
   * Demonstrates pulling data from a third-party API and using it in the application.

3. **Data Visualization**

   * Sentiment analysis of user notes using **TextBlob**.
   * Visual representation using **Plotly**:

     * Pie chart showing the distribution of **positive, neutral, and negative notes**.
   * Visualization is embedded directly in the Django template.

4. **User Authentication & Session Management**

   * Simple session-based login using Spotify OAuth.
   * Ensures only authenticated users can add or view notes.

---

### **Technology Stack**

* **Backend:** Python, Django
* **Database:** PostgreSQL (or Supabase)
* **Frontend:** Django templates, HTML, CSS, minimal JS
* **API Integration:** Spotify API
* **Data Analysis:** TextBlob (for sentiment)
* **Visualization:** Plotly (charts embedded in frontend)
* **Deployment:** Hosted on Render / any cloud platform

---

### **Project Structure**

```
spotifyNotes/
│
├── playlist/
│   ├── views.py           # Handles CRUD and sentiment analysis
│   ├── models.py          # Database models (playlistNotesTrack)
│   ├── urls.py            # Routing for API endpoints and views
│   ├── templates/         # HTML templates (notes, dashboards)
│   └── services/          # Analytics, Spotify API integration
│
├── spotifyNotes/
│   ├── settings.py        # Django configuration
│   ├── urls.py            # Project-level routing
│
├── manage.py              # Django command-line utility
└── requirements.txt       # Python dependencies
```

---

### **How to Run Locally**

1. Clone the repository:

   ```bash
   git clone <repo-url>
   cd spotifyNotes
   ```
2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Set up PostgreSQL / Supabase and configure credentials in `settings.py`.
4. Run migrations:

   ```bash
   python manage.py migrate
   ```
5. Start the server:

   ```bash
   python manage.py runserver
   ```
6. Visit `http://127.0.0.1:8000` in your browser.

---

### **Demo Features**

* Add / update / delete notes for any track.
* View sentiment analysis pie chart of notes.
* Retrieve user top tracks from Spotify API.
* Interactive dashboard with album images and notes.

---

### **Submission**

* GitHub repo: [`SpotifyNotesTrack`](https://github.com/CODECZERO/SpotifyNotesTrack)
* Live deployment: [`live-link`](https://spotifynotestrack.onrender.com)

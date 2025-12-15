# 🎥 Movie App Frontend (UI)

The user interface for the Movie Application, built with **Streamlit**. This dashboard connects to the FastAPI backend to allow users to interact with the movie database.

## ✨ Features

* **🔐 Secure Authentication:** Login and Sign-up forms that exchange JWT tokens with the backend.
* **🌍 Community Feed:** View a list of all movies shared by all users.
* **👤 My Collection:** A filtered view showing only the movies *you* have added.
* **✏️ Full Management:** Add new movies, edit details (rating, director), or delete movies you own.
* **🚫 Access Control:** The UI automatically hides "Edit" and "Delete" buttons for movies that don't belong to you.

## ⚙️ Configuration

The application is set to connect to localhost by default.
If your backend is running on a different port or server, update the `API_URL` variable in `app.py`:

```python
# app.py
API_URL = "[http://127.0.0.1:8000](http://127.0.0.1:8000)"
```
### 📦 Installation & Usage
1. Install Requirements: Make sure you are inside the movie_ui folder:
```bash
pip install -r requirements.txt
```
2. Run the App:
```bash
streamlit run app.py
```
🧩 Dependencies
```bash
streamlit - The UI framework.

requests - For sending HTTP requests to the FastAPI backend.

pandas - For displaying movie data in clean tables.
```

### 👤 Author
Built by Erfan Hosseini as a backend engineering project. Feel free to check out my other repositories!
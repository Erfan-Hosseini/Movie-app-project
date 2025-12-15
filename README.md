# 🎬 Full Stack Movie Application

A complete Movie Collection application built with a separate Backend (FastAPI) and Frontend (Streamlit).

This project demonstrates a fully functional **CRUD** application with **User Authentication**.

## 🏗️ Architecture

The project is divided into two distinct parts:

* **`movie_api/` (Backend):** Built with **FastAPI** and **SQLAlchemy**. Handles the database, user authentication (JWT), and business logic.
* **`movie_ui/` (Frontend):** Built with **Streamlit**. Provides a user-friendly dashboard for users to log in, browse movies, and manage their collections.

## 🚀 Quick Start Guide

To run this application, you need to launch the backend and frontend in **two separate terminals**.

### Step 1: Start the Backend
1.  Open a terminal and navigate to the api folder:
    ```bash
    cd movie_api
    ```
2.  Install backend dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Start the server:
    ```bash
    uvicorn main:app --reload
    ```
    *The API is now running at `http://127.0.0.1:8000`*

### Step 2: Start the Frontend
1.  Open a **new** terminal and navigate to the ui folder:
    ```bash
    cd movie_ui
    ```
2.  Install frontend dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```
    *The Dashboard will open in your browser at `http://localhost:8501`*

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Backend:** FastAPI, SQLAlchemy, Pydantic, Passlib (Security)
* **Frontend:** Streamlit, Pandas, Requests
* **Database:** SQLite (Default)

## 📂 Documentation

For detailed information on specific features, please refer to the README files inside each folder:
* [Frontend Documentation](./movie_ui/README.md)
* [Backend Documentation](./movie_api/README.md)

### 👤 Author
Built by Erfan Hosseini as a backend engineering project. Feel free to check out my other repositories!
# 🎬 FastAPI Movie Manager API

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-Built%20In-003B57?style=for-the-badge&logo=sqlite)

A robust RESTful API built with **FastAPI** to manage a movie database. The system features secure user authentication (JWT), role-based ownership permissions, and advanced filtering capabilities. 

> **Key Learning Focus:** Backend architecture, Authentication flows, ORM relationships, and API Security.

---

## 🚀 Features

### 🔐 Authentication & Security
* **User Registration & Login:** Secure password hashing using `bcrypt`.
* **JWT Authorization:** Stateless authentication using JSON Web Tokens (OAuth2).
* **Route Protection:** Secured endpoints that require a valid token to access.

### 🎥 Movie Management (CRUD)
* **Create:** Users can add movies to the database.
* **Read:** Retrieve lists of movies with **Pagination** (limit/skip) to handle large datasets.
* **Update/Delete:** Strict **Ownership Logic** — a user can only edit or delete the movies *they* created.
* **Search:** Filter movies by Director, Year, Rating, or Title.

---

## 🛠️ Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (High performance, easy to learn).
* **Database:** SQLite (SQLAlchemy ORM).
* **Validation:** Pydantic models.
* **Security:** Passlib (Hashing), Python-Jose (JWT).
* **Environment:** Python-Dotenv for secret management.

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone https://github.com/Erfan-Hosseini/New-start_python-projects.git
cd New-start_python-projects/movie_api
```
### 2. Create Virtual Environment
It is recommended to use a virtual environment to manage dependencies.
```bash
# Create the environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a .env file in the movie_api folder and add your secret keys:

```bash
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
### 5. Run the Server
```bash
uvicorn main:app --reload
```
The API will be available at: http://127.0.0.1:8000

### 📖 API Documentation
FastAPI provides automatic interactive documentation. Once the server is running, access:

Swagger UI: http://127.0.0.1:8000/docs (Test the API directly in your browser).

ReDoc: http://127.0.0.1:8000/redoc

### 🧪 Example Usage
1. Register a User POST /users/create-user
```bash
{
  "username": "johndoe",
  "password": "securepassword123",
  "email": "john@example.com"
}
```
2. Login to get Token POST /users/login (Returns a Bearer Token)

3. Create a Movie (Requires Auth) POST /movies/
```bash 
{
  "title": "Inception",
  "director": "Christopher Nolan",
  "year": 2010,
  "rating": 8.8
}
```
### 👤 Author
Built by Erfan Hosseini as a backend engineering project. Feel free to check out my other repositories!

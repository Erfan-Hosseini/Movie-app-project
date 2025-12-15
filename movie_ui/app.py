import streamlit as st
import requests
import pandas as pd

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="Movie App", page_icon="🎬")

# --- SESSION STATE (The Memory) ---
if "token" not in st.session_state:
    st.session_state.token = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"

def go_to_signup():
    st.session_state.current_page = "signup"

def go_to_login():
    st.session_state.current_page = "login"

# --- FUNCTIONS ---
def signup_page():
    st.header("👤 Create an account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")

    if st.button("Create an account", key="signup_submit"):
        payload = {"username": username, "password": password, "email": email}

        try:
            response = requests.post(f"{API_URL}/users/create-user", json=payload)

            if response.status_code == 200:
                st.success("Account created! Redirecting...")
                st.session_state.current_page = "login"
                st.rerun()

            elif response.status_code == 400:
                st.error("Username already exists")

            elif response.status_code == 422:

                st.error(f"Validation Error: {response.json()}")

            else:
                st.error(f"Signup failed. Status: {response.status_code}")

        except Exception as e:
            st.error(f"Connection Error: {e}")
            
    st.write("---")
    st.button("Back to login", on_click=go_to_login, key="back_to_login")

def get_current_user():
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    try:
        res = requests.get(f"{API_URL}/users/me", headers=headers)
        
        if res.status_code != 200:
            st.error(f"Backend Error ({res.status_code}): {res.text}")
            return None
            
        return res.json()
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None
    
def login_page():
    st.header("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # --- LOGIC START ---
    if st.button("Login"):
        payload = {"username": username, "password": password}
        
        try:
            response = requests.post(f"{API_URL}/users/login", data=payload)
            
            if response.status_code == 200:
                token_data = response.json()
                st.session_state.token = token_data["access_token"]
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")

        except Exception as e:
            st.error(f"Connection Error: {e}")
    # --- LOGIC END ---

    st.write("---")
    st.write("Don't have an account?")
    st.button("Create an account", on_click=go_to_signup,key="goto_signup")

def logout():
    st.session_state.token = None
    st.rerun()

def show_dashboard():
    current_user = get_current_user()

    if not current_user:
        st.warning("Please log in to view your collection.")
        st.stop()
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🎬 Movie Dashboard")
    with col2:
        if st.button("Logout", type="primary"):
            logout()
    st.divider()

    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    movies_data = []
     
    if not current_user:
        st.warning("Could not identify current user. Some features may be locked.")
        current_user_id = -1
    else:
        current_user_id = current_user.get("id") 

    try:
        response = requests.get(f"{API_URL}/movies/", headers=headers)
        if response.status_code == 200:
            movies_data = response.json()
    except Exception as e:
        st.error(f"Connection Error: {e}")

    my_movies = [m for m in movies_data if m.get('owner_id') == current_user_id]

    # 3. THE 4 TABS
    tab1, tab2, tab3, tab4 = st.tabs([
        "🌍 Community (All)", 
        "👤 My Collection", 
        "➕ Add Movie", 
        "⚙️ Manage (Edit/Delete)"
    ])

    # --- TAB 1: COMMUNITY (ALL MOVIES) ---
    with tab1:
        st.subheader("Global Movie Database")
        if movies_data:
            df = pd.DataFrame(movies_data)
            st.dataframe(
                df.drop(columns=["id"], errors="ignore").rename(columns={"owner_id": "Owner ID"}), 
                width="stretch"
            )
        else:
            st.info("No movies in the database.")

    # --- TAB 2: MY COLLECTION (ONLY MINE) ---
    with tab2:
        st.subheader(f"{(current_user or {}).get('username', 'My')}'s Collection")
        if my_movies:
            df_mine = pd.DataFrame(my_movies)
            st.dataframe(
                df_mine.drop(columns=["id", "owner_id"], errors="ignore"), 
                width="stretch"
            )
        else:
            st.info("You haven't added any movies yet.")

    # --- TAB 3: ADD MOVIE (Same as before) ---
    with tab3:
        st.subheader("Add a New Movie")
        with st.form("add_movie_form", clear_on_submit=True):
            new_title = st.text_input("Title")
            new_director = st.text_input("Director")
            new_year = st.number_input("Year", 1888, 2025, step=1, value=2024)
            new_rating = st.slider("Rating", 0.0, 10.0, 5.0, 0.1)
            new_available = st.checkbox("Is Available?", value=True)
            
            if st.form_submit_button("Save Movie"):
                movie_payload = {
                    "title": new_title,
                    "director": new_director,
                    "year": new_year,
                    "rating": new_rating,
                    "available": new_available
                }
                res = requests.post(f"{API_URL}/movies/", json=movie_payload, headers=headers)
                if res.status_code == 200:
                    st.success("Movie added!")
                    st.rerun()
                else:
                    st.error(f"Error: {res.text}")

    # --- TAB 4: MANAGE (EDIT/DELETE ONLY MINE) ---
    with tab4:
        st.subheader("Manage Your Movies")
        
        if my_movies:
            # Dropdown only shows MY movies
            movie_options = {m['title']: m for m in my_movies}
            selected_title = st.selectbox("Select a movie to manage:", list(movie_options.keys()))
            
            selected_movie = movie_options[selected_title]
            selected_id = selected_movie['id']

            st.divider()
            
            with st.form("edit_form"):
                st.write(f"Editing: **{selected_title}**")
                edit_director = st.text_input("Director", value=selected_movie['director'])
                edit_rating = st.slider("Rating", 0.0, 10.0, value=float(selected_movie['rating']))
                edit_available = st.checkbox("Is Available?", value=selected_movie['available'])
                
                if st.form_submit_button("Update Movie"):
                    update_payload = {
                        "title": selected_title, 
                        "director": edit_director,
                        "rating": edit_rating,
                        "available": edit_available
                    }
                    res = requests.put(f"{API_URL}/movies/{selected_id}", json=update_payload, headers=headers)
                    if res.status_code == 200:
                        st.success("Updated!")
                        st.rerun()
                    else:
                        st.error("Failed to update.")

            # DELETE BUTTON
            if st.button(f"Delete '{selected_title}'", type="primary"):
                res = requests.delete(f"{API_URL}/movies/{selected_id}", headers=headers)
                if res.status_code == 200 or res.status_code == 204:
                    st.success("Deleted!")
                    st.rerun()
                else:
                    st.error("Failed to delete.")
        else:
            st.info("You have no movies to edit.")
# --- MAIN CONTROLLER ---
if st.session_state.token is not None:
    show_dashboard()

else:
    if st.session_state.current_page == "login":
        login_page()
    elif st.session_state.current_page == "signup":
        signup_page()
import streamlit as st
import json
import os
import base64

# Database files
DB_FILE = "selection.json"
MENU_FILE = "menu.json"

# --- Helper Functions ---
def load_selection():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f).get("dish")
    return None

def save_selection(dish_name):
    with open(DB_FILE, "w") as f:
        json.dump({"dish": dish_name}, f)

def load_menu():
    if os.path.exists(MENU_FILE):
        with open(MENU_FILE, "r") as f:
            return json.load(f)
    return []

def save_menu(menu_data):
    with open(MENU_FILE, "w") as f:
        json.dump(menu_data, f)

# --- App Setup ---
st.set_page_config(page_title="Dinner Decider", page_icon="🍽️", layout="centered")
st.title("🍽️ The Dinner Decider")

# Load the custom menu
menu = load_menu()

# Create the three views
tab1, tab2, tab3 = st.tabs(["Menu", "Kitchen", "⚙️ Manage Menu"])

# --- YOUR VIEW ---
with tab1:
    st.header("What are you craving?")
    if not menu:
        st.info("The menu is empty! Head over to the 'Manage Menu' tab to add your first dish.")
    else:
        st.write("Tap a dish below to send it to the kitchen.")
        cols = st.columns(2) # 2 columns look better on mobile
        for i, dish in enumerate(menu):
            with cols[i % 2]:
                # Decode the saved image to display it
                img_bytes = base64.b64decode(dish["image_base64"])
                st.image(img_bytes, use_container_width=True)
                
                if st.button(f"Choose {dish['name']}", key=f"btn_{i}_{dish['name']}"):
                    save_selection(dish['name'])
                    st.success(f"Selected {dish['name']}!")

# --- HER VIEW ---
with tab2:
    st.header("Tonight's Menu")
    current_selection = load_selection()
    
    if current_selection:
        st.success(f"He has chosen: **{current_selection}**!")
        
        # Find and display the image of the chosen dish
        for dish in menu:
            if dish["name"] == current_selection:
                img_bytes = base64.b64decode(dish["image_base64"])
                st.image(img_bytes, width=400)
                break
                
        if st.button("Clear Selection (Meal Completed)"):
            save_selection(None)
            st.rerun()
    else:
        st.info("Waiting for him to choose... no selection made yet.")

# --- ADMIN VIEW ---
with tab3:
    st.header("Add a New Dish")
    st.write("Upload photos of your girlfriend's cooking here.")
    
    with st.form("add_dish_form", clear_on_submit=True):
        new_dish_name = st.text_input("Dish Name (e.g., Spicy Chicken Tacos)")
        uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])
        
        submitted = st.form_submit_button("Add to Menu")
        
        if submitted:
            if new_dish_name and uploaded_file:
                # Convert the image into a string so it can be saved in our simple JSON database
                base64_string = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
                
                new_dish = {
                    "name": new_dish_name,
                    "image_base64": base64_string
                }
                
                menu.append(new_dish)
                save_menu(menu)
                st.success(f"Added {new_dish_name} to the menu!")
                st.rerun()
            else:
                st.error("Please provide both a name and an image.")
    
    # Optional: A way to clear the menu if you make a mistake
    if menu:
        st.divider()
        st.write("Danger Zone")
        if st.button("Delete All Dishes"):
            save_menu([])
            st.rerun()

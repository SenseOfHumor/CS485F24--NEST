import streamlit as st
import os
import tempfile
from pymongo import MongoClient
from dotenv import load_dotenv
import openai
import datetime

## Importing functions
from image_recognition_openAI import (
    extract_platforms_usernames_and_passwords,
    upload_to_mongo,
    search_credentials,
    update_credential
)


## Custom CSS to make buttons and font larger
## Changes made after feedback from test subjects
## Only makes the button size larger, due to streamlit's limitations
st.markdown("""
    <style>
    .stButton button {
        font-size: 30px;
        padding: 15px 25px;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown p {
        font-size: 30px;
    }
    </style>
    """, unsafe_allow_html=True)


st.title("NEST 🪺")
st.header("Safe Haven for Your Passwords")

## upload section
st.markdown("## Upload Image and Extract Usernames, Passwords")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    ## Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image_file:
        temp_image_file.write(uploaded_file.read())
        temp_image_path = temp_image_file.name

    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract and Upload Usernames, Passwords"):
        with st.spinner("Extracting usernames, passwords and uploading to MongoDB..."):
            try:
                upload_to_mongo(temp_image_path)
                st.success("usernames, passwords extracted and uploaded successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")


## TODO: Use the password suggestion function and have a dedicated section for it
# 
# workflow:
# - Upon searching up passwords, call the password suggestion function
# - If it is weak, suggest a stronger password
# - Have a UI button to accept the suggestion
# - Update the password in the database using update_credential function (optional)
# - Display suggestions using st.alert or st.warning (optional)
# 


## Search Credentials Section
st.sidebar.markdown("### Search Username, Password")
search_query = st.sidebar.text_input("Enter platform or username to search:")
if st.sidebar.button("Search"):
    # with st.sidebar.spinner("Searching for credentials..."):
        try:
            results = search_credentials(search_query)
            if results:
                st.sidebar.write("Search Results:")
                for result in results:
                    st.sidebar.write(
                        f"**Platform:** {result['platform']} | "
                        f"**Username:** {result['username']} | "
                        f"**Password:** {result['password']} | "
                        f"**Created At:** {result['created_at']} | "
                        f"**Updated At:** {result['updated_at']}"
                    )
            else:
                st.sidebar.warning("No matching credentials found.")
        except Exception as e:
            st.sidebar.error(f"An error occurred: {e}")

## Update Credential Section
st.sidebar.markdown("### Update Username, Password")
platform_to_update = st.sidebar.text_input("Enter the platform to update:")
username_to_update = st.sidebar.text_input("Enter the username to update:")
new_password = st.sidebar.text_input("Enter the new password:", type="password")
if st.sidebar.button("Update Password"):
    # with st.sidebar.spinner("Updating credential..."):
        try:
            updated_doc = update_credential(platform_to_update, username_to_update, new_password)
            if updated_doc:
                st.sidebar.success(
                    f"Password for {username_to_update} on {platform_to_update} updated successfully!"
                )
            else:
                st.sidebar.warning(
                    f"No Username/Passwords found for username {username_to_update} on platform {platform_to_update}."
                )
        except Exception as e:
            st.sidebar.error(f"An error occurred: {e}")

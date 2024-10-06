import gspread
from google.oauth2.service_account import Credentials  # Updated from oauth2client to google-auth
import streamlit as st
import pandas as pd
from datetime import datetime

# Authenticate and connect to Google Sheets
def connect_to_gsheet(creds_json, spreadsheet_name, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", 
             'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", 
             "https://www.googleapis.com/auth/drive"]
    
    credentials = Credentials.from_service_account_file(creds_json, scopes=scope)  # Updated to use google-auth
    client = gspread.authorize(credentials)
    spreadsheet = client.open(spreadsheet_name)
    return spreadsheet.worksheet(sheet_name)  # Access specific sheet by name

# Google Sheet credentials and details
SPREADSHEET_NAME = 'Entry_Form'
SHEET_NAME = 'Tenant'
CREDENTIALS_FILE = './credentials.json'  # Ensure this file exists and is valid

# Connect to the Google Sheet
sheet_by_name = connect_to_gsheet(CREDENTIALS_FILE, SPREADSHEET_NAME, sheet_name=SHEET_NAME)

st.title("Tenant Feedback")
st.markdown("Provide your thoughts below")

# Read Data from Google Sheets
def read_data():
    data = sheet_by_name.get_all_records()  # Get all records from Google Sheet
    return pd.DataFrame(data)

# Add Data to Google Sheets
def add_data(row):
    sheet_by_name.append_row(row)  # Append the row to the Google Sheet

# Form for submitting new feedback
with st.form(key='feedback_form'):
    # Input fields
    date = st.date_input("Date*", value=datetime.today())
    name = st.text_input("Name (Optional)")
    comment = st.text_area("Comment*")
    
    # Mark mandatory fields
    st.markdown("**required*")
    # Submit button
    submit_button = st.form_submit_button(label="Submit Feedback")

    # If the form is submitted
    if submit_button:
        if not comment:  # Check if the comment (mandatory) field is filled
            st.warning("Please ensure all mandatory fields are filled.")
            st.stop()
        else:
            row = [date.strftime("%Y-%m-%d"), name if name else "Anonymous", comment]
            add_data(row)  # Add new feedback to Google Sheets
            st.success(f"Thank you {name if name else 'Anonymous'}! Your feedback has been submitted.")


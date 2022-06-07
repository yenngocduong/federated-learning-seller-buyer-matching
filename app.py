import streamlit as st
import matching_page
import information_page
import history_page
from time import time
import time
import Pyrebase

#database
firebaseConfig = {
    'apiKey': "AIzaSyD79ky9cGg4TgZN1wC-6Q3yKkAOz6kJfdw",
    'authDomain': "federated-learning-3fe90.firebaseapp.com",
    'databaseURL': "https://ureca-5416c-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "federated-learning-3fe90",
    'storageBucket': "federated-learning-3fe90.appspot.com",
    'messagingSenderId': "406892630649",
    'appId': "1:406892630649:web:9b8acd7a39e3f440927aa8",
    'measurementId': "G-3CLV68BGM5"
}

firebase = Pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

db = firebase.database()
storage = firebase.storage()


st.set_page_config(
        page_title='Federated Learning Matching',
        page_icon="🗒️"
        )


page = st.sidebar.selectbox('Choose page', ('Information', 'Model', 'History'))
if page == 'Information':
    information_page.show_information()
if page == 'Model':
    matching_page.show_matching(db)
if page == 'History':
    history_page.show_history(db)
import pyrebase
import streamlit as st
import datetime
import pandas as pd, numpy as np

def show_history(db):
  records = db.child('record').get()
  # print(records.val())
  record_id = list(records.val())
  record_id.insert(0, "Choose record")
  id = st.selectbox('Please select record to view', record_id)
  data = db.child('record').child(id).get()
  # print(data.val())
  print()
  if id!="Choose record":
    st.write(f'Experiment id {id} on {datetime.datetime.fromtimestamp(int(id))}')
    st.write('Number of seller', data.val()['seller_num'])
    st.write('Number of buyer', data.val()['buyer_num'])
    st.write('Asking information')
    seller_ask = data.val()['seller_ask']
    seller_ask_df = pd.DataFrame(np.array(seller_ask).reshape(1, -1),
                                  columns=[f'seller_{i+1}' for i in range(len(seller_ask))], index = ['ask'])
    st.table(seller_ask_df)

    st.write('Budget information')
    buyer_budget = data.val()['seller_ask']
    buyer_budget_df = pd.DataFrame(np.array(buyer_budget).reshape(1, -1),
                                 columns=[f'buyer_{i + 1}' for i in range(len(buyer_budget))], index=['budget'])
    st.table(buyer_budget_df)


def draw():
  pass
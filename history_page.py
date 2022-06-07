import pyrebase
import streamlit as st
import datetime
import pandas as pd, numpy as np

def show_history(db):
  st.write("""# Viewing history information from previous experiments""")
  choice = st.selectbox('Please select operation', ['Please choose an operation',
                                                    'Show previous experiments detailed information',
                                                    'General visualization of all experiments'])

  if choice == 'Show previous experiments detailed information':
    show_record(db)
  elif choice == 'General visualization of all experiments':
    draw()
  else:
    pass




def show_record(db):
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
    st.write("Matching method: ", data.val()['method'])
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

    st.write('Bidding information')
    print(data.val()['buyer_bid'])
    buyer_bid_np = data.val()['buyer_bid'][1:]
    buyer_bid_np = [x[1:] for x in buyer_bid_np]
    buyer_bid_df = pd.DataFrame(np.array(buyer_bid_np), columns=[f'seller_{i+1}' for i in range(data.val()['seller_num'])],
                                index=[f'buyer_{i+1}' for i in range(data.val()['buyer_num'])])
    st.table(buyer_bid_df)

    st.write("""### Result""")
    N = len(data.val()['bid_result'].items())
    st.write(f'There are {N} successful bids')
    st.write("Seller rewards")
    seller_reward = []
    for i in range(N):
      record = data.val()['seller_reward'][f'matching_{i+1}']
      seller_reward.append([record['seller'], record['ask'], record['reward']])
    seller_reward = pd.DataFrame(seller_reward, columns=['seller', 'ask', 'reward'],
                                 index=[f'matching_{i}' for i in range(N)])
    st.table(seller_reward)

    st.write('Bid result')
    bid_result = []
    for i in range(N):
      record = data.val()['bid_result'][f'matching_{i+1}']
      bid_result.append([record['seller'], record['buyer'], record['bid'], record['payment']])
    bid_result = pd.DataFrame(bid_result, columns=['seller', 'buyer', 'bid', 'payment'],
                              index=[f'matching_{i+1}' for i in range(N)])
    bid_result['buyer'] = bid_result['buyer'].astype('int64')
    bid_result['seller'] = bid_result['seller'].astype('int64')
    st.table(bid_result)


def draw():
  pass
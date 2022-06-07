import streamlit as st
from seller import Seller, Ask
from auctioneer import Auctioneer
from buyer import Buyer, Bid
from experience import experience1_2_4, experience3, experience5
import pandas as pd, numpy as np
import time

def matching(seller_num, buyer_num, seller_ask, buyer_bid, bid_box, buyer_budget, method, db):
    sellers = []
    buyers = []
    for i in range(seller_num):
        if seller_ask[i] is None:
            sellers.append(Seller(i))
        else:
            ask = Ask(i, seller_ask[i])
            sellers.append(Seller(i=i, ask=ask))
    for i in range(buyer_num):
        if buyer_bid[i] is None and buyer_budget[i] is None:
            buyers.append(Buyer(i, seller_num))
        elif buyer_budget[i] is None:
            bids = [Bid(i, bid[0], bid[1]) for bid in buyer_bid[i]]
            buyers.append(Buyer(i=i, m=seller_num, bids=bids))
        elif buyer_bid[i] is None:
            buyers.append(Buyer(i=i, m=seller_num, budget=buyer_budget[i]))
        else:
            bids = [Bid(i, bid[0], bid[1]) for bid in buyer_bid[i]]
            buyers.append(Buyer(i=i, m=seller_num, bids=bids, budget=buyer_budget[i]))

    id = int(time.time())
    st.write('Experiment ID:', id)

    #print buyer, seller information
    st.write('Sellers\' information:')
    # print('sellers\' information:')
    ask_df = pd.DataFrame(np.array(seller_ask).reshape(1, -1), columns=[f'seller {i+1}' for i in range(seller_num)], index=['ask'])
    st.table(ask_df)
        # st.write('seller:', i, ', ask:', sellers[i].get_ask().ask)
        # print('seller:', i, ', ask:', sellers[i].get_ask().ask)
    st.write('Buyers\' information:')
    # print('buyers\' information:')
    # for i in range(len(buyers)):
    #     st.write('buyer:', i, 'budget:', buyers[i].get_budget(), 'bids:',
    #           list(map(lambda b: (b.seller, b.bid), buyers[i].get_bids())))
    #     print('buyer:', i, 'budget:', buyers[i].get_budget(), 'bids:',
    #           list(map(lambda b: (b.seller, b.bid), buyers[i].get_bids())))

    budget_df = pd.DataFrame(np.array(buyer_budget).reshape(1, -1), columns=[f'buyer {i+1}' for i in range(buyer_num)], index=['budget'])
    st.table(budget_df)

    st.write('Bid information')
    bid_df = pd.DataFrame(np.array(bid_box), columns=[f'seller {i+1}' for i in range(seller_num)], index=[f'buyer {i+1}' for i in range(buyer_num)])
    st.table(bid_df)
    # threshold pricing based DAI 方法
    print(sellers)
    print(buyers)
    if method == 'Threshold pricing based DAI':
        w_asks, w_bids, p_asks, p_bids = Auctioneer.threshold_pricing(sellers, buyers)
        st.write(f'There are {len(w_bids)} successful bids')
        st.write("""### Result of threshold pricing based DAI:""")
        seller_result = []
        for i in range(len(w_asks)):
            seller_result.append([int(w_asks[i].num)+1, w_asks[i].ask, w_asks[i].reward])
        if w_asks == 1:
            seller_result = np.array(seller_result).reshape(1, -1)
        else:
            seller_result = np.array(seller_result)
        seller_df = pd.DataFrame(seller_result, columns=['seller', 'ask', 'reward'], index=[f'matching {i+1}' for i in range(len(seller_result))])
        st.write('Seller side')
        st.table(seller_df)


        bid_result = []
        for i in range(len(w_bids)):
            bid_result.append([int(w_bids[i].buyer)+1, int(w_bids[i].seller)+1, w_bids[i].bid, w_bids[i].payment])
            # st.write(w_bids[i].buyer, w_bids[i].seller, w_bids[i].bid, w_bids[i].payment)
        if w_bids == 1:
            bid_result = np.array(bid_result).reshape(1, -1)
        else:
            bid_result = np.array(bid_result)
        bid_df = pd.DataFrame(bid_result, columns=['buyer', 'seller', 'bid', 'payment'], index=[f'matching {i+1}' for i in range(len(bid_result))])
        bid_df['buyer'] = bid_df['buyer'].astype('int64')
        bid_df['seller'] = bid_df['seller'].astype('int64')
        st.write('Matching information')
        st.table(bid_df)
    else:
        # dynamic pricing based DAI 方法
        w_asks, w_bids, p_asks, p_bids = Auctioneer.dynamic_pricing(sellers, buyers)
        st.write("""### Result of threshold pricing based DAI:""")
        st.write(f'There are {len(w_bids)} successful bids')
        seller_result = []
        for i in range(len(w_asks)):
            seller_result.append([int(w_asks[i].num)+1, w_asks[i].ask, w_asks[i].reward])
        if w_asks == 1:
            seller_result = np.array(seller_result).reshape(1, -1)
        else:
            seller_result = np.array(seller_result)
        if len(seller_result)>0:
            seller_df = pd.DataFrame(seller_result, columns=['seller', 'ask', 'reward'], index=[f'matching {i+1}' for i in range(len(seller_result))])
            seller_df['seller'].astype('int64')
            st.write('Seller side')
            st.table(seller_df)


        bid_result = []
        for i in range(len(w_bids)):
            bid_result.append([int(w_bids[i].buyer)+1, int(w_bids[i].seller)+1, w_bids[i].bid, w_bids[i].payment])
            # st.write(w_bids[i].buyer, w_bids[i].seller, w_bids[i].bid, w_bids[i].payment)
        if w_bids == 1:
            bid_result = np.array(bid_result).reshape(1, -1)
        else:
            bid_result = np.array(bid_result)
        if len(bid_result)>0:
            bid_df = pd.DataFrame(bid_result, columns=['buyer', 'seller', 'bid', 'payment'], index=[f'matching {i+1}' for i in range(len(bid_result))])
            bid_df['buyer'] = bid_df['buyer'].astype('int64')
            bid_df['seller'] = bid_df['seller'].astype('int64')
            st.write('Matching information')
            st.table(bid_df)

    buyer_bid_dic = {i+1: {buyer_bid[i][j][0]+1: buyer_bid[i][j][1] for j in range(len(buyer_bid[i]))} for i in range(len(buyer_bid))}
    bid_result_dic = {f'matching_{i+1}': {'buyer': bid_result[i][0]+1, 'seller': bid_result[i][1]+1, 'bid': bid_result[i][2], 'payment': bid_result[i][3]} for i in range(len(bid_result))}
    seller_result_dic = {f'matching_{i+1}': {'seller': int(seller_result[i][0])+1, 'ask': int(seller_result[i][1]), 'reward': int(seller_result[i][2])} for i in range(len(seller_result))}
    # print(seller_result[0][0], type(seller_result[0][0]))
    # seller_result_dic = {f'matching_{i}': {'seller': int(seller_result[i][0])} for i in range(len(seller_result))}
    print(seller_result_dic)
    print(type(bid_result_dic))
    data = {"seller_num": seller_num, "buyer_num": buyer_num, 'seller_ask': seller_ask, 'buyer_budget': buyer_budget,
            'buyer_bid': buyer_bid_dic, "method": method,
            'seller_reward': seller_result_dic,
            "bid_result": bid_result_dic}
    db.child('record').child(id).set(data)
    # db.child('record').push(data)
    #end


def show_matching(db):
    st.title('Buyers, Sellers matching')
    st.write("""### We need some information""")

    seller_num = st.number_input('Please input number of sellers', min_value=0, max_value=100)
    buyer_num = st.number_input('Please input number of buyers', min_value=0, max_value=100)

    ask = [None]*seller_num
    for i in range(seller_num):
        if i == 0:
            st.write("""### Input sellers' asking amount""")
        ask[i] = st.number_input(f'Asking of seller {i+1}, leave blank if not specify', min_value=0, key=i)

    budget = [None] * buyer_num
    for i in range(buyer_num):
        if i == 0:
            st.write("""### Input buyers' budget amount""")
        budget[i] = st.number_input(f'Budget of buyer {i + 1}, leave blank if not specify', min_value=0, key=i)
    # bid = []
    # add_bid = st.button('Add bid')
    # index = 0
    # if add_bid:
    #     temp_bid_buyer = st.number_input('Specify buyer', key=index)
    #     temp_bid_seller = st.number_input('Specify seller', key=index)
    #     temp_bid_amount = st.number_input('specify amount', key=index)
    #     index += 1

    # if 'count' not in st.session_state:
    #     st.session_state.count = 0
    #
    # def add_new_row(key):
    #     st.text_input("Please input something", key=key)
    #
    # index = 0
    # if st.button("Add new row"):
    #     st.session_state.count += 1
    #     add_new_row(index)
    #     if st.session_state.count > 1:
    #         for i in range(st.session_state.count-1):
    #             add_new_row(i)
    #     index+=1

    # num_bid = 0
    # new_bid = st.button('New bid', key=num_bid)
    # while new_bid:
    #     num_bid += 1
    #     temp_bid_buyer = st.number_input('Specify buyer', key=index)
    #     temp_bid_seller = st.number_input('Specify seller', key=index)
    #     temp_bid_amount = st.number_input('specify amount', key=index)
    #     new_bid = st.button('New bid', key=num_bid)
    #     finish = st.button('Finish', key=num_bid)
    #     if finish:
    #         break

    c = [None]*buyer_num
    box = [[None for j in range(seller_num)] for i in range(buyer_num)]
    bids = [[] for i in range(buyer_num)]
    for buyer_index in range(buyer_num):
        if buyer_index == 0:
            st.write("""### Input bidding information""")
        c[buyer_index] = st.columns(seller_num)
        for seller_index in range(seller_num):
            with c[buyer_index][seller_index]:
                box[buyer_index][seller_index] = st.number_input(f'Buyer {buyer_index+1} bids from seller {seller_index+1}', key=f'{buyer_index}, {seller_index}')
                bids[buyer_index].append((seller_index, box[buyer_index][seller_index]))

    st.write("""### Please choose pricing method""")
    method = st.selectbox("Pricing method", ('Threshold pricing based DAI', 'Dynamic pricing based DAI'))

    bt = st.button('Calculate')
    if bt:
        if seller_num == 0 and buyer_num == 0:
            st.write("Please input number of sellers and buyers")
        elif seller_num == 0:
            st.write("Please input number of sellers")
        elif buyer_num == 0:
            st.write("Please input number of buyers")
        else:
            st.write("""## Summary""")
            matching(seller_num, buyer_num, ask, bids, box, budget, method, db)


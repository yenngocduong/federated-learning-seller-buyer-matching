from seller import Seller, Ask
from auctioneer import Auctioneer
from buyer import Buyer, Bid
from experience import experience1_2_4, experience3, experience5
from history_page import show_history

def test():
    # 随机生成sellers和buyers
    seller_num = 5
    buyer_num = 5
    sellers = [Seller(i) for i in range(seller_num)]
    buyers = [Buyer(i, seller_num) for i in range(buyer_num)]

    # 打印sellers和buyers信息
    print('sellers\' information:')
    for i in range(len(sellers)):
        print('seller:', i, ', ask:', sellers[i].get_ask().ask)
    print('buyers\' information:')
    for i in range(len(buyers)):
        print('buyer:', i, 'budget:', buyers[i].get_budget(), 'bids:',
              list(map(lambda b: (b.seller, b.bid), buyers[i].get_bids())))

    # threshold pricing based DAI 方法
    print('result of threshold pricing based DAI:')
    w_asks, w_bids, p_asks, p_bids = Auctioneer.threshold_pricing(sellers, buyers)
    print('seller    ask    reward')
    for i in range(len(w_asks)):
        print(w_asks[i].num, w_asks[i].ask, w_asks[i].reward)
    print('buyer    seller    bid    payment')
    for i in range(len(w_bids)):
        print(w_bids[i].buyer, w_bids[i].seller, w_bids[i].bid, w_bids[i].payment)
    print('len(w_bids):', len(w_bids))

    # dynamic pricing based DAI 方法
    print('result of dynamic pricing based DAI: ')
    w_asks, w_bids, p_asks, p_bids = Auctioneer.dynamic_pricing(sellers, buyers)
    print('seller    ask    reward')
    for i in range(len(w_asks)):
        print(w_asks[i].num, w_asks[i].ask, w_asks[i].reward)
    print('buyer    seller    bid    payment')
    for i in range(len(w_bids)):
        print(w_bids[i].buyer, w_bids[i].seller, w_bids[i].bid, w_bids[i].payment)
    print('len(w_bids):', len(w_bids))


#code
def program(seller_num, buyer_num, seller_ask, buyer_bid, buyer_budget):
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

    #print buyer, seller information
    print('sellers\' information:')
    for i in range(len(sellers)):
        print('seller:', i, ', ask:', sellers[i].get_ask().ask)
    print('buyers\' information:')
    for i in range(len(buyers)):
        print('buyer:', i, 'budget:', buyers[i].get_budget(), 'bids:',
              list(map(lambda b: (b.seller, b.bid), buyers[i].get_bids())))

    # threshold pricing based DAI 方法
    print('result of threshold pricing based DAI:')
    w_asks, w_bids, p_asks, p_bids = Auctioneer.threshold_pricing(sellers, buyers)
    print('seller    ask    reward')
    for i in range(len(w_asks)):
        print(w_asks[i].num, w_asks[i].ask, w_asks[i].reward)
    print('buyer    seller    bid    payment')
    for i in range(len(w_bids)):
        print(w_bids[i].buyer, w_bids[i].seller, w_bids[i].bid, w_bids[i].payment)
    print('len(w_bids):', len(w_bids))

    # dynamic pricing based DAI 方法
    print('result of dynamic pricing based DAI: ')
    w_asks, w_bids, p_asks, p_bids = Auctioneer.dynamic_pricing(sellers, buyers)
    print('seller    ask    reward')
    for i in range(len(w_asks)):
        print(w_asks[i].num, w_asks[i].ask, w_asks[i].reward)
    print('buyer    seller    bid    payment')
    for i in range(len(w_bids)):
        print(w_bids[i].buyer, w_bids[i].seller, w_bids[i].bid, w_bids[i].payment)
    print('len(w_bids):', len(w_bids))
#end

def main():
    seller_num = 5
    buyer_num = 5
    seller_ask = [9, 4, 7, 10, 9]
    buyer_budget = [35, 41, 11, 28, 21]
    buyer_bid = [[(0, 7), (1, 12), (2, 6), (3, 7), (4, 6)],
                 [(0, 9), (1, 10), (2, 6), (3, 5), (4, 12)],
                 [(0, 3), (1, 0), (2, 1), (3, 0), (4, 3)],
                 [(0, 2), (1, 0), (2, 10), (3, 1), (4, 14)],
                 [(0, 6), (1, 13), (2, 14), (3, 5), (4, 8)]]
    test()
    print()
    print('PROGRAM')
    program(seller_num, buyer_num, seller_ask, buyer_bid, buyer_budget)

if __name__ == '__main__':
    main()

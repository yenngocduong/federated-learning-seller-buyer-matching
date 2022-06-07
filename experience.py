import random
from config import Config
from matplotlib import pyplot as plt
from seller import Seller
from auctioneer import Auctioneer
from buyer import Buyer
from functools import reduce


# y, labels, markers是具有同样大小的list
# params = [xlabel, ylabel, title, filepath]
def paint_plot(x, y, labels, markers, linestyles, params):
    plt.clf()
    for i in range(len(y)):
        plt.plot(x, y[i], label=labels[i], marker=markers[i], linestyle=linestyles[i])
    plt.xlabel(params[0])
    plt.ylabel(params[1])
    plt.title(params[2])
    plt.legend(labels)
    plt.savefig(params[3])
    # plt.show()


def paint_bar(x, y, labels, width, params):
    plt.clf()
    for i in range(len(y)):
        plt.bar(x, y[i], label=labels[i], width=width[i])
    plt.xlabel(params[0])
    plt.ylabel(params[1])
    plt.title(params[2])
    plt.legend(labels)
    plt.savefig(params[3])


def generate(seller_num, buyer_num):
    sellers = [Seller(i) for i in range(seller_num)]
    buyers = [Buyer(i, seller_num) for i in range(buyer_num)]
    return sellers, buyers


# 更改buyer/seller数量，观察utility、winning bids数量、 budget balance
def experience1_2_4():
    fixed_num = Config.fixed_num
    start_num = Config.start_num
    step = Config.step
    end_num = Config.end_num

    # 基于threshold pricing方法，固定seller_num更改buyer_num
    seller_num = fixed_num
    buyer_num = start_num
    u_buyers = []
    u_sellers = []
    num_w_bids = []
    sum_reward = []
    sum_payment = []
    x_buyers = []
    while buyer_num <= end_num:
        x_buyers += [buyer_num]
        # 以下sum变量均用于计算多次模拟结果的平均值
        sum_u_buyers = 0  # buyer总收益， 中间变量
        sum_u_sellers = 0  # seller总收益， 中间变量
        sum_w_bids = 0  # 总winning bids数量， 中间变量
        sum_sum_reward = 0  # winning bids的总和， 中间变量
        sum_sum_payment = 0  # payment总和， 中间变量
        for i in range(10):
            sellers, buyers = generate(seller_num, buyer_num)
            w_asks, w_bids, p_asks, p_bids = Auctioneer.threshold_pricing(sellers, buyers)
            sum_sum_reward += sum(p_asks)
            sum_sum_payment += sum(p_bids)
            sum_u_buyers += Auctioneer.get_utility(list(map(lambda b: b.bid, w_bids)), p_bids)
            sum_u_sellers += Auctioneer.get_utility(list(map(lambda a: a.ask, w_asks)), p_asks)
            sum_w_bids += len(w_bids)
        u_buyers += [sum_u_buyers/10]
        u_sellers += [sum_u_sellers/10]
        num_w_bids += [sum_w_bids//10]
        sum_reward += [sum_sum_reward/10]
        sum_payment += [sum_sum_payment/10]
        buyer_num += step
    b_u_buyers_tp = u_buyers  # 基于threshold pricing算法，buyer变化时，记录buyer的utility的数组
    b_u_sellers_tp = u_sellers  # 基于threshold pricing算法，buyer变化时，记录seller的utility的数组
    b_num_w_bids_tp = num_w_bids  # 基于threshold pricing算法，buyer变化时，记录winning bids数量的数组

    # 绘制并保存图像
    # 实验四
    paint_bar(x_buyers, [sum_payment, sum_reward], ['sum_payment', 'sum_reward'], [8, 5],
              ['Number of buyers', 'Payment & reward', 'Budget balance based threshold pricing',
               Config.filepath+'\\issue2\\exp4\\img\\img1.png'])

    # 基于threshold pricing方法，固定buyer_num更改seller_num
    seller_num = start_num
    buyer_num = fixed_num
    u_buyers = []
    u_sellers = []
    x_sellers = []
    num_w_bids = []
    sum_reward = []
    sum_payment = []
    while seller_num <= end_num:
        x_sellers += [seller_num]
        sum_u_buyers = 0
        sum_u_sellers = 0
        sum_w_bids = 0
        sum_sum_reward = 0  # winning bids的总和， 中间变量
        sum_sum_payment = 0  # payment总和， 中间变量
        for i in range(10):
            sellers, buyers = generate(seller_num, buyer_num)
            w_asks, w_bids, p_asks, p_bids = Auctioneer.threshold_pricing(sellers, buyers)
            sum_sum_reward += sum(p_asks)
            sum_sum_payment += sum(p_bids)
            sum_u_buyers += Auctioneer.get_utility(list(map(lambda b: b.bid, w_bids)), p_bids)
            sum_u_sellers += Auctioneer.get_utility(list(map(lambda a: a.ask, w_asks)), p_asks)
            sum_w_bids += len(w_bids)
        u_buyers += [sum_u_buyers/10]
        u_sellers += [sum_u_sellers/10]
        num_w_bids += [sum_w_bids//10]
        sum_reward += [sum_sum_reward/10]
        sum_payment += [sum_sum_payment/10]
        seller_num += step
    s_u_buyers_tp = u_buyers
    s_u_sellers_tp = u_sellers
    s_num_w_bids_tp = num_w_bids  # 基于threshold pricing算法，seller变化时，记录winning bids数量的数组

    # 绘制图像
    paint_bar(x_sellers, [sum_payment, sum_reward], ['sum_payment', 'sum_reward'], [8, 5],
              ['Number of sellers', 'Payment & reward', 'Budget balance based threshold pricing',
               Config.filepath+'\\issue2\\exp4\\img\\img2.png'])

    # 基于dynamic pricing方法，固定seller_num更改buyer_num
    seller_num = fixed_num
    buyer_num = start_num
    u_buyers = []
    u_sellers = []
    x_buyers = []
    num_w_bids = []
    sum_reward = []
    sum_payment = []
    while buyer_num <= end_num:
        x_buyers += [buyer_num]
        sum_u_buyers = 0
        sum_u_sellers = 0
        sum_w_bids = 0
        sum_sum_reward = 0  # winning bids的总和， 中间变量
        sum_sum_payment = 0  # payment总和， 中间变量
        for i in range(10):
            sellers, buyers = generate(seller_num, buyer_num)
            w_asks, w_bids, p_asks, p_bids = Auctioneer.dynamic_pricing(sellers, buyers)
            sum_sum_reward += sum(p_asks)
            sum_sum_payment += sum(p_bids)
            sum_u_buyers += Auctioneer.get_utility(list(map(lambda b: b.bid, w_bids)), p_bids)
            sum_u_sellers += Auctioneer.get_utility(list(map(lambda a: a.ask, w_asks)), p_asks)
            sum_w_bids += len(w_bids)
        u_buyers += [sum_u_buyers/10]
        u_sellers += [sum_u_sellers/10]
        num_w_bids += [sum_w_bids//10]
        sum_reward += [sum_sum_reward/10]
        sum_payment += [sum_sum_payment/10]
        buyer_num += step
    b_u_buyers_dp = u_buyers  # 基于dynamic pricing算法，buyer变化时，记录buyer的utility的数组
    b_u_sellers_dp = u_sellers  # 基于dynamic pricing算法，buyer变化时，记录buyer的utility的数组
    b_num_w_bids_dp = num_w_bids  # 基于dynamic pricing算法，buyer变化时，记录winning bids数量的数组

    # 绘制图像
    paint_bar(x_buyers, [sum_payment, sum_reward], ['sum_payment', 'sum_reward'], [8, 5],
              ['Number of buyers', 'Payment & reward', 'Budget balance based dynamic pricing',
               Config.filepath+'\\issue2\\exp4\\img\\img3.png'])

    # 基于dynamic pricing方法，固定buyer_num更改seller_num
    plt.clf()
    seller_num = start_num
    buyer_num = fixed_num
    u_buyers = []
    u_sellers = []
    x_sellers = []
    num_w_bids = []
    sum_reward = []
    sum_payment = []
    while seller_num <= end_num:
        x_sellers += [seller_num]
        sum_u_buyers = 0
        sum_u_sellers = 0
        sum_w_bids = 0
        sum_sum_reward = 0  # winning bids的总和， 中间变量
        sum_sum_payment = 0  # payment总和， 中间变量
        for i in range(10):
            sellers, buyers = generate(seller_num, buyer_num)
            w_asks, w_bids, p_asks, p_bids = Auctioneer.dynamic_pricing(sellers, buyers)
            sum_sum_reward += sum(p_asks)
            sum_sum_payment += sum(p_bids)
            sum_u_buyers += Auctioneer.get_utility(list(map(lambda b: b.bid, w_bids)), p_bids)
            sum_u_sellers += Auctioneer.get_utility(list(map(lambda a: a.ask, w_asks)), p_asks)
            sum_w_bids += len(w_bids)
        u_buyers += [sum_u_buyers/10]
        u_sellers += [sum_u_sellers/10]
        num_w_bids += [sum_w_bids//10]
        sum_reward += [sum_sum_reward/10]
        sum_payment += [sum_sum_payment/10]
        seller_num += step
    s_u_buyers_dp = u_buyers
    s_u_sellers_dp = u_sellers
    s_num_w_bids_dp = num_w_bids

    # 绘制图像
    paint_bar(x_sellers, [sum_payment, sum_reward], ['sum_payment', 'sum_reward'], [8, 5],
              ['Number of sellers', 'Payment & reward', 'Budget balance based dynamic pricing',
               Config.filepath+'\\issue2\\exp4\\img\\img4.png'])

    # 将两个算法的结果放在同一个图里，方便对比
    # 实验一
    # buyer_num变化时
    paint_plot(x_buyers, [b_u_buyers_tp, b_u_sellers_tp, b_u_buyers_dp, b_u_sellers_dp],
               ['u_buyers_tp', 'u_sellers_tp', 'u_buyers_dp', 'u_sellers_dp'], ['d', 'd', '*', '*'],
               ['-', '-', '-', '-'], ['Number of buyers', 'Utility', 'Utility of buyers/sellers',
                                      Config.filepath+'\\issue2\\exp1\\img\\img5.png'])
    # seller_num变化时
    paint_plot(x_sellers, [s_u_buyers_tp, s_u_sellers_tp, s_u_buyers_dp, s_u_sellers_dp],
               ['u_buyers_tp', 'u_sellers_tp', 'u_buyers_dp', 'u_sellers_dp'], ['d', 'd', '*', '*'],
               ['-', '-', '-', '-'], ['Number of sellers', 'Utility', 'Utility of buyers/sellers',
                                      Config.filepath+'\\issue2\\exp1\\img\\img6.png'])
    # 实验二
    paint_plot(x_buyers, [b_num_w_bids_tp, b_num_w_bids_dp], ['threshold pricing', 'dynamic pricing'], ['d', '*'],
               ['-', '-'], ['Number of buyers', 'Number of winning bids', 'Number of winning bids',
                            Config.filepath+'\\issue2\\exp2\\img\\img5.png'])
    paint_plot(x_sellers, [s_num_w_bids_tp, s_num_w_bids_dp], ['threshold pricing', 'dynamic pricing'], ['d', '*'],
               ['-', '-'], ['Number of sellers', 'Number of winning bids', 'Number of winning bids',
                            Config.filepath+'\\issue2\\exp2\\img\\img6.png'])


# 观察winning buyers/sellers的bid&payment/ask&reward
def experience3():
    seller_num = 40
    buyer_num = 20
    sellers, buyers = generate(seller_num, buyer_num)

    # threshold pricing方法，经测试和直觉发现，当seller_num>=2*buyer_num时，得出的图像比较贴合[2]，猜测跟budget的取值范围有关
    w_asks, w_bids, p_asks, p_bids = Auctioneer.threshold_pricing(sellers, buyers)
    # 绘制buyer图像
    x_buyers = range(len(w_bids))
    bids = list(map(lambda b: b.bid, w_bids))
    paint_bar(x_buyers, [bids, p_bids], ['bids', 'payment'], [0.6, 0.3],
              ['Number of buyers', 'Bid & payment', 'Bid & payment based threshold pricing',
               Config.filepath+'\\issue2\\exp3\\img\\img1.png'])
    # 绘制seller图像
    x_sellers = range(len(w_asks))
    asks = list(map(lambda a: a.ask, w_asks))
    paint_bar(x_sellers, [p_asks, asks], ['reward', 'ask'], [0.6, 0.3],
              ['Number of sellers', 'Reward & ask', 'Reward & ask based threshold pricing',
               Config.filepath + '\\issue2\\exp3\\img\\img2.png'])

    # dynamic pricing方法
    w_asks, w_bids, p_asks, p_bids = Auctioneer.dynamic_pricing(sellers, buyers)

    x_buyers = range(len(w_bids))
    bids = list(map(lambda b: b.bid, w_bids))
    paint_bar(x_buyers, [bids, p_bids], ['bids', 'payment'], [0.6, 0.3],
              ['Number of buyers', 'Bid & payment', 'Bid & payment based dynamic pricing',
               Config.filepath+'\\issue2\\exp3\\img\\img3.png'])

    x_sellers = range(len(w_asks))
    asks = list(map(lambda a: a.ask, w_asks))
    paint_bar(x_sellers, [p_asks, asks], ['reward', 'ask'], [0.6, 0.3],
              ['Number of sellers', 'Reward & ask', 'Reward & ask based dynamic pricing',
               Config.filepath + '\\issue2\\exp3\\img\\img4.png'])


# 更改buyer的bid/seller的ask，验证算法的真实性
def experience5():
    seller_num = 10
    buyer_num = 10
    sellers, buyers = generate(seller_num, buyer_num)

    # threshold pricing方法
    w_asks, w_bids, p_asks, p_bids = Auctioneer.threshold_pricing(sellers, buyers)
    bids = map(lambda b: b.get_bids(), buyers)
    bids = reduce(lambda b1, b2: b1 + b2, bids)
    l_bids = list(filter(lambda b: b not in w_bids, bids))
    w_bid = w_bids[random.randint(0, len(w_bids)-1)]
    l_bid = l_bids[random.randint(0, len(l_bids)-1)]
    # 验证winning buyer的真实性
    true_bid = w_bid.bid
    w_bid.bid = Config.bid_up
    u_bid = []
    x_bid = []
    while w_bid.bid >= 0:
        w_bids = Auctioneer.threshold_pricing(sellers, buyers)[1]
        if w_bid in w_bids:
            u_bid += [true_bid - w_bid.payment]
        else:
            u_bid += [0]
        x_bid += [w_bid.bid]
        w_bid.bid -= 1
    paint_plot(x_bid, [u_bid], ['utility'], ['+'], [':'],
               ['Bid', 'Utility', 'Winning buyer based threshold pricing', Config.filepath+'\\issue2\\exp5\\img\\img1.png'])
    w_bid.bid = true_bid  # 恢复原样
    # 验证losing buyer的真实性
    true_bid = l_bid.bid
    l_bid.bid = Config.bid_up
    u_bid = []
    x_bid = []
    while l_bid.bid >= 0:
        w_bids = Auctioneer.threshold_pricing(sellers, buyers)[1]
        if l_bid in w_bids:
            u_bid += [true_bid - l_bid.payment]
        else:
            u_bid += [0]
        x_bid += [l_bid.bid]
        l_bid.bid -= 1
    paint_plot(x_bid, [u_bid], ['utility'], ['+'], [':'],
               ['Bid', 'Utility', 'Losing buyer based threshold pricing', Config.filepath + '\\issue2\\exp5\\img\\img2.png'])
    l_bid.bid = true_bid

    # dynamic pricing方法
    w_asks, w_bids, p_asks, p_bids = Auctioneer.dynamic_pricing(sellers, buyers)
    bids = map(lambda b: b.get_bids(), buyers)
    bids = reduce(lambda b1, b2: b1 + b2, bids)
    l_bids = list(filter(lambda b: b not in w_bids, bids))
    w_bid = w_bids[random.randint(0, len(w_bids)-1)]
    l_bid = l_bids[random.randint(0, len(l_bids)-1)]
    # 验证winning buyer的真实性
    true_bid = w_bid.bid
    w_bid.bid = Config.bid_up
    u_bid = []
    x_bid = []
    while w_bid.bid >= 0:
        w_bids = Auctioneer.dynamic_pricing(sellers, buyers)[1]
        if w_bid in w_bids:
            u_bid += [true_bid - w_bid.payment]
        else:
            u_bid += [0]
        x_bid += [w_bid.bid]
        w_bid.bid -= 1
    paint_plot(x_bid, [u_bid], ['utility'], ['+'], [':'],
               ['Bid', 'Utility', 'Winning buyer based dynamic pricing', Config.filepath+'\\issue2\\exp5\\img\\img3.png'])
    w_bid.bid = true_bid  # 恢复原样
    # 验证losing buyer的真实性
    true_bid = l_bid.bid
    l_bid.bid = Config.bid_up
    u_bid = []
    x_bid = []
    while l_bid.bid >= 0:
        w_bids = Auctioneer.dynamic_pricing(sellers, buyers)[1]
        if l_bid in w_bids:
            u_bid += [true_bid - l_bid.payment]
        else:
            u_bid += [0]
        x_bid += [l_bid.bid]
        l_bid.bid -= 1
    paint_plot(x_bid, [u_bid], ['utility'], ['+'], [':'],
               ['Bid', 'Utility', 'Losing buyer based dynamic pricing', Config.filepath + '\\issue2\\exp5\\img\\img4.png'])
    l_bid.bid = true_bid

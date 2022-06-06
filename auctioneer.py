from functools import reduce


class Auctioneer(object):
    threshold_a = 0
    threshold_b = 0

    @classmethod
    def get_candidate(cls, sellers, buyers):
        # 排序
        asks = [s.get_ask() for s in sellers]
        asks = sorted(asks, key=lambda a: a.ask)
        threshold = asks[(len(sellers)-1)//2].ask

        bids = map(lambda b: b.get_bids(), buyers)
        bids = reduce(lambda b1, b2: b1+b2, bids)
        bids = sorted(bids, key=lambda b: b.bid, reverse=True)

        # 初次筛选，筛掉不满足阈值要求的ask和bid
        c_asks = list(filter(lambda a: a.ask >= threshold, asks))
        Auctioneer.threshold_a = threshold
        c_bids = list(filter(lambda b: b.bid >= threshold, bids))
        # 获取不小于threshold的bid的最小值，用于之后的payment定义

        Auctioneer.threshold_b = c_bids[len(c_bids)-1].bid

        # 二次筛选，筛掉 ①竞价<出价②竞价指向的seller不存在 的bid
        c_bids = list(filter(lambda b: b.bid >= sellers[b.seller].get_ask().ask &
                                       sellers[b.seller].get_ask().ask <= threshold, c_bids))

        return c_asks, c_bids

    @classmethod
    def get_winner(cls, sellers, buyers, c_bids):
        w_bids = []
        w_asks = []
        p_bids = []
        p_asks = []

        budget = list(map(lambda b: b.budget, buyers))
        while len(c_bids) > 0:
            s_i = c_bids[0].seller
            # 确定竞争者
            b_s_i = list(filter(lambda b: b.seller == s_i, c_bids))
            # 确定payment
            if len(b_s_i) == 1:
                c_bids[0].payment = Auctioneer.threshold_b
            else:
                c_bids[0].payment = b_s_i[1].bid
            # 确定预算是否足够
            if budget[c_bids[0].buyer] - c_bids[0].payment >= 0:
                w_bids += [c_bids[0]]
                w_asks += [sellers[s_i].get_ask()]
                sellers[s_i].buyer = c_bids[0].buyer
                sellers[s_i].get_ask().reward = Auctioneer.threshold_a
                p_bids += [c_bids[0].payment]
                p_asks += [Auctioneer.threshold_a]
                budget[c_bids[0].buyer] -= c_bids[0].payment
                c_bids = list(filter(lambda b: b.seller != s_i, c_bids))
            else:
                del c_bids[0]

        return w_asks, w_bids, p_asks, p_bids

    @classmethod
    def threshold_pricing(cls, sellers, buyers):
        # 确定候选者
        c_asks, c_bids = Auctioneer.get_candidate(sellers, buyers)
        # 确定胜出者
        w_asks, w_bids, p_asks, p_bids = Auctioneer.get_winner(sellers, buyers, c_bids)

        return w_asks, w_bids, p_asks, p_bids

    @classmethod
    def dynamic_pricing(cls, sellers, buyers):
        # sorting阶段
        asks = [s.get_ask().ask for s in sellers]
        # ask从高到低排序，方便找a_γ
        asks = sorted(asks, key=lambda a: a, reverse=True)

        bids = map(lambda b: b.get_bids(), buyers)
        bids = reduce(lambda b1, b2: b1+b2, bids)
        bids = list(filter(lambda b: b.bid != 0, bids))
        bids = sorted(bids, key=lambda b: b.bid, reverse=True)

        # winner and pricing determination阶段
        # 筛除bid不满足ask的竞标
        c_bids = []
        for i in range(len(bids)):
            s_k = bids[i].seller
            ask_s_k = sellers[s_k].get_ask().ask
            if asks.index(ask_s_k) != 0:
                # 找到大于s_i_ask的最小ask值
                a_gamma = asks[asks.index(ask_s_k)-1]
                if bids[i].bid >= a_gamma:
                    c_bids += [bids[i]]

        # 确定获胜者
        w_bids = []
        w_asks = []
        p_bids = []
        p_asks = []
        budget = list(map(lambda b: b.budget, buyers))
        while len(c_bids) > 0:
            s_i = c_bids[0].seller
            # 确定竞争者
            b_s_i = list(filter(lambda b: b.seller == s_i, c_bids))
            ask_s_i = sellers[s_i].get_ask().ask
            if asks.index(ask_s_i) != 0:
                a_k = asks[asks.index(ask_s_i)-1]  # 大于ask_s_i的最小值
                if len(b_s_i) == 1:
                    c_bids[0].payment = a_k
                else:
                    c_bids[0].payment = b_s_i[1].bid
                if budget[c_bids[0].buyer] - c_bids[0].payment >= 0:
                    w_bids += [c_bids[0]]
                    w_asks += [sellers[s_i].get_ask()]
                    sellers[s_i].buyer = c_bids[0].buyer
                    p_bids += [c_bids[0].payment]
                    sellers[s_i].get_ask().reward = a_k
                    p_asks += [a_k]
                    budget[c_bids[0].buyer] -= c_bids[0].payment
                    c_bids = list(filter(lambda b: b.seller != s_i, c_bids))
                else:
                    del c_bids[0]
            else:
                del c_bids[0]

        return w_asks, w_bids, p_asks, p_bids

    @classmethod
    # 实际支付/获得与出价/要价的差值
    def get_utility(cls, origin, fact):
        return abs(sum(origin)-sum(fact))

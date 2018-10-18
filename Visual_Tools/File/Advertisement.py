data = {
    '台湾': 101687.54,
    '美国': 65776.48,
    '意大利': 22526.28,
    '德国': 27259.57,
    '法国': 17784.43,
    '瑞典': 8916.39,
    '丹麦':8288.94,
    '挪威':5481.00,
    '芬兰': 5481.00,
    '马来西亚': 15574.15,
    '越南': 1699.55,
    '印度': 13820.04,
    '巴基斯坦': 13820.04,
    '巴西': 21936.27,
    '日本': 3345.40,
    '韩国': 5165.99,
     '英国': 22019.85,
    '西班牙': 13699.61,
    '葡萄牙': 3580.02,
    '荷兰': 14905.97,
    '土耳其': 20688.38,
    '爱尔兰': 2544.18,
    '比利时': 9272.15,
    '瑞士': 5629.56,
    '奥地利': 7160.10,
    '希腊': 3622.68,
    '匈牙利': 6429.37,
    '加拿大': 8399.81,
    '南非': 3741.62,
    '墨西哥': 13290.96,
    '澳大利亚': 4521.59,
    '俄罗斯': 1959.59,
    '乌克兰': 146.85,
    '罗马尼亚': 263.92,
    '波兰': 720.07,
    '捷克': 470.33,
    '保加利亚': 286.54,
    '塞尔维亚': 79.87,
    '斯洛伐克': 186.44,
    '克罗地亚': 109.62,
    '白俄罗斯': 38.65,
    '波斯尼亚和黑塞哥维那': 45.88,
    '阿尔巴尼亚': 65.70,
    '立陶宛': 271.46,
    '缅甸': 110.18,
    '柬埔寨': 58.21,
    '泰国': 533.02,
    '新加坡': 571.09,
    '印度尼西亚': 439.88,
    '菲律宾': 792.81,
    '孟加拉国': 47.02,
    '尼泊尔': 49.06,
    '斯里兰卡': 18.97,
    '哈萨克斯坦': 76.67,
    '尼日尼亚': 35.28,
    '多米尼加共和国': 82.11,
    '沙特阿拉伯': 688.44,
    '以色列': 500.04,
    '中国香港': 6118.54,
    '阿根廷': 2014.64,
    '哥伦比亚': 2074.88,
    '智利': 2208.03,
    '秘鲁': 1968.63,
    '科威特': 91.01,
    '厄瓜多尔': 582.79,
    '摩洛哥': 79.76,
    '中国澳门': 315.27,
    '伊拉克': 596.35,
    '阿尔及尼亚': 96.01,
    '埃及': 117.73,
    '委内瑞拉': 91.01,
    '玻利维亚': 176.28,
    '阿拉伯联合酋长国': 157.86,
    '突尼斯': 81.24,
    '危地马拉': 119.57,
    '约旦': 92.88,
    '巴拉圭': 24.96,
    '黎巴嫩': 165.26,
    '利比亚': 33.81,
    '阿富汗': 4.19,
    '洪都拉斯': 13.02,
    '萨尔瓦多': 38.48,
    '卡塔尔': 36.88,
    '巴林': 0.24,
    '乌拉圭': 128.39,
    '波多黎各': 116.07,
    '巴拿马': 8.82,
    '尼加拉瓜': 6.54,
    '也门': 10.81,
    '巴勒斯坦': 43.49,
    '阿曼': 43.49,
}
def sort_by_value(d):

    items=d.items()

    backitems=[[v[1],v[0]] for v in items]

    backitems.sort()

    return [ {'name':backitems[i][1],'value':backitems[i][0]} for i in range(0,len(backitems))]
data=(sort_by_value(data))
data.reverse()
print(data)


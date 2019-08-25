def refine_rate(options_list):
    bonus = 100
    for opt in options_list:
        bonus += opt
    bonus = bonus / 100
    rate = [100, 100, 95, 90, 80, 70, 60, 50, 40, 25, 20, 3, 25, 7, 3]
    rate = [i * bonus for i in rate]
    for idx, item in enumerate(rate):
        if item > 100:
            rate[idx] = 100
    list_1 = list(range(1, 16))
    d = dict(zip(list_1, rate))
    table = ""
    for i in range(1, 6):
        table += f"{i:02}:{d[i]:>7.02f} | {i+5:02}:{d[i+5]:>7.02f} | {i+10}:{d[i+10]:>7.02f} \n"
    return table

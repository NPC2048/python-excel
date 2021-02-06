import re
from datetime import datetime
import calendar

def yyyy_mm_format(date_str: str):
    return re.match(r"\d{4}")


# 解析月租金格式，获取每年月租金、范围
def parse(sh, current_year):
    # 判断类型
    if not(isinstance(sh, str)):
        return
    # 符合正则才进行处理
    if not(re.match(r"\d{4}[.-]\d{1,2}[.-]\d{1,2}[~-]", sh)):
        return
    # 解析开始日期
    begins = re.findall(r"\d{4}[.-]\d{1,2}[.-]\d{1,2}[~-]", sh)
    print(begins)
    # 解析结束日期
    ends = re.findall(r"[~-]\d{4}[.-]\d{1,2}[.-]\d{1,2}", sh)
    print(ends)
    # print('ends: ', ends)
    moneys = re.findall("[:：]\\d+\\.\\d+|[:：]\\d+", sh)
    print(moneys)
    # print('moneys:', moneys)
    # 三个数量不一致则不处理
    begin_len = len(begins)
    if begin_len != len(ends) or begin_len != len(moneys):
        print('此行表格有问题:', sh)
        return

    # 返回该行数据
    data_map: dict = {}
    for i in range(begin_len):
        begin: str = begins[i][:-1]
        end: str = ends[i][1:]
        money = float(moneys[i][1:])
        print('------ begin:', begin, ', end:', end)
        # 结束日期
        begin_date = datetime.strptime(begin.replace('.', '-'), '%Y-%m-%d').date()
        end_date = datetime.strptime(end.replace('.', '-'), '%Y-%m-%d').date()
        # print('date:', begin_date, end_date)
        # 开始到结束的年月都作为 key 存储在 data_map 中
        begin_year = begin_date.year
        begin_month = begin_date.month
        end_year = end_date.year
        end_month = end_date.month
        # print('begin month:', begin_month)
        year_sub = end_year - begin_year
        # print('begin:', begin_year, ', end_year:', end_year, ', sub:', year_sub)
        # 生成中间月数据
        for y in range(year_sub):
            year_end = begin_year + y
            # 结束日期数据
            for m in range(12):
                key = str(year_end) + '-' + str(m + 1)
                data_map[key] = money

        # 结束月数据
        for m in range(begin_month):
            key = str(end_year - 1) + '-' + str(m + 1)
            data_map[key] = money
        # 结束日期数据
        for m in range(end_month - 1):
            key = str(end_year) + '-' + str(m + 1)
            data_map[key] = money
        # print('row:', year, begin, end, money)
        # 计算最后一个月的数据, 判断是否有下个月
        last_key = str(end_year) + '-' + str(end_month)
        # print('handle:', data_map)
        if i != begin_len - 1:
            # 获取下个月的租金
            next_money = float(moneys[i+1][1:])
            # 下月开始天数
            last_money = calc_month(end_date, money, next_money)
            # key
            data_map[last_key] = last_money
        else:
            data_map[last_key] = money
        # print('last_key:', last_key)
        # print('i:',i, data_map)
        # 年份，月份
        data_map['month'] = parse_month(current_year, end_date)
        break
    # 区间正则表达式
    # ^\d{4}(\.|-)\d{1,2}(\.|-)\d{1,2}(~|-)\d{4}(\.|-)\d{1,2}(\.|-)\d{1,2}(:|：)\d+(\.\d+)?$
    # print('------------- parse end')
    # 如果不存在当前年份, 则把大于当前年份的租金计入当前年份中
    return data_map

def parse_month(current_year, end_date):
    if current_year == end_date.year:
        return end_date.month + 1
    else:
        return 12

# 计算当月租金
# 1. 获取指定月份的天数
# 2. (上半月天数 * 上半月租金 + 下半月天数 * 下半月租金) / 当月天数 = 当月租金
def calc_month(end_date, up_money: float, down_money: float):
    # 获取月份天数
    days = calendar.monthrange(end_date.year, end_date.month)
    day = days[1]
    money = (end_date.day * up_money + (day - end_date.day) * down_money) / day
    print('月:', end_date.month, ', 租金:', money)
    return money
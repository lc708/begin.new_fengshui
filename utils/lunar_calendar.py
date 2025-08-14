"""
农历转换工具
提供公历农历转换功能（简化版本）
"""

def solar_to_lunar(solar_date):
    """
    公历转农历（简化版本）
    
    Args:
        solar_date (str): 公历日期 "YYYY-MM-DD"
    
    Returns:
        dict: 农历信息
    """
    # 简化算法，实际项目中建议使用专业的农历转换库
    year, month, day = map(int, solar_date.split("-"))
    
    # 农历月份名称
    lunar_months = ["正月", "二月", "三月", "四月", "五月", "六月",
                    "七月", "八月", "九月", "十月", "十一月", "腊月"]
    
    # 简单估算（实际需要复杂的农历算法）
    # 农历一般比公历晚1-2个月
    lunar_month = month - 1 if month > 1 else 12
    lunar_year = year if month > 1 else year - 1
    
    # 日期简单转换（实际需要考虑大小月）
    lunar_day = day
    
    # 农历日期名称
    day_names = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                 "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                 "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
    
    lunar_day_name = day_names[min(lunar_day - 1, 29)]
    
    return {
        "lunar_year": lunar_year,
        "lunar_month": lunar_month,
        "lunar_day": lunar_day,
        "lunar_month_name": lunar_months[lunar_month - 1],
        "lunar_day_name": lunar_day_name,
        "lunar_date_str": f"{lunar_year}年{lunar_months[lunar_month - 1]}{lunar_day_name}"
    }

def get_solar_terms(year):
    """
    获取某年的二十四节气（简化版本）
    
    Args:
        year (int): 年份
    
    Returns:
        dict: 节气信息
    """
    # 二十四节气名称
    solar_terms = [
        "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
        "立夏", "小满", "芒种", "夏至", "小暑", "大暑", 
        "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
        "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
    ]
    
    # 简化版本：按固定日期估算节气
    # 实际应用中需要精确的天文计算
    base_dates = [
        "02-04", "02-19", "03-05", "03-20", "04-05", "04-20",
        "05-05", "05-21", "06-05", "06-21", "07-07", "07-23",
        "08-07", "08-23", "09-07", "09-23", "10-08", "10-23",
        "11-07", "11-22", "12-07", "12-22", "01-05", "01-20"
    ]
    
    solar_terms_info = {}
    for i, (term, date) in enumerate(zip(solar_terms, base_dates)):
        solar_terms_info[term] = f"{year}-{date}"
    
    return solar_terms_info

if __name__ == "__main__":
    # 测试公历转农历
    lunar_info = solar_to_lunar("2024-01-15")
    print(f"农历信息: {lunar_info}")
    
    # 测试节气查询
    terms = get_solar_terms(2024)
    print("2024年部分节气:")
    for term in ["立春", "春分", "立夏", "夏至"]:
        print(f"{term}: {terms[term]}")

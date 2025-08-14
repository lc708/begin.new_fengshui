"""
八字计算工具
根据公历生日计算天干地支八字
"""

def calculate_bazi(birth_date, gender, location="北京"):
    """
    计算八字信息
    
    Args:
        birth_date (dict): {"year": 1990, "month": 1, "day": 1, "hour": 12}
        gender (str): "male" 或 "female"
        location (str): 出生地
    
    Returns:
        dict: 包含天干地支的八字信息
    """
    
    # 天干地支数组
    tiangang = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # 简化算法：基于公历年份计算（实际应用中需要更精确的农历转换）
    year = birth_date["year"]
    month = birth_date["month"] 
    day = birth_date["day"]
    hour = birth_date["hour"]
    
    # 年柱计算（以1984年甲子年为基准）
    year_offset = (year - 1984) % 60
    year_tg = tiangang[year_offset % 10]
    year_dz = dizhi[year_offset % 12]
    
    # 月柱计算（简化版本）
    month_offset = (month - 1) % 12
    month_tg = tiangang[(year_offset * 2 + month) % 10]
    month_dz = dizhi[month_offset]
    
    # 日柱计算（简化版本）
    # 实际需要考虑农历和节气
    day_offset = (year * 365 + month * 30 + day) % 60
    day_tg = tiangang[day_offset % 10]
    day_dz = dizhi[day_offset % 12]
    
    # 时柱计算
    hour_index = hour // 2  # 每两小时一个时辰
    hour_dz = dizhi[hour_index % 12]
    hour_tg = tiangang[(day_offset * 2 + hour_index) % 10]
    
    # 五行对应
    wuxing_map = {
        "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
        "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水",
        "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土",
        "巳": "火", "午": "火", "未": "土", "申": "金", "酉": "金",
        "戌": "土", "亥": "水"
    }
    
    # 计算五行数量
    all_chars = [year_tg, year_dz, month_tg, month_dz, day_tg, day_dz, hour_tg, hour_dz]
    wuxing_count = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
    
    for char in all_chars:
        element = wuxing_map.get(char, "土")
        wuxing_count[element] += 1
    
    # 生肖计算
    zodiac_animals = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
    zodiac = zodiac_animals[(year - 1984) % 12]
    
    # 纳音五行（简化版本）
    nayin_list = ["海中金", "炉中火", "大林木", "路旁土", "剑锋金", "山头火", 
                  "涧下水", "城头土", "白蜡金", "杨柳木", "泉中水", "屋上土"]
    nayin = nayin_list[year_offset % 12]
    
    return {
        "tiangang": [year_tg, month_tg, day_tg, hour_tg],
        "dizhi": [year_dz, month_dz, day_dz, hour_dz],
        "wuxing": wuxing_count,
        "zodiac": zodiac,
        "nayin": nayin,
        "year_pillar": f"{year_tg}{year_dz}",
        "month_pillar": f"{month_tg}{month_dz}",
        "day_pillar": f"{day_tg}{day_dz}",
        "hour_pillar": f"{hour_tg}{hour_dz}",
        "gender": gender,
        "location": location
    }

if __name__ == "__main__":
    # 测试示例
    test_birth = {"year": 1990, "month": 6, "day": 15, "hour": 14}
    result = calculate_bazi(test_birth, "male", "北京")
    print("八字计算结果:")
    print(f"年柱: {result['year_pillar']}")
    print(f"月柱: {result['month_pillar']}")
    print(f"日柱: {result['day_pillar']}")
    print(f"时柱: {result['hour_pillar']}")
    print(f"生肖: {result['zodiac']}")
    print(f"纳音: {result['nayin']}")
    print(f"五行: {result['wuxing']}")

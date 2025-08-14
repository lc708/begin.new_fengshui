"""
日历查询工具
提供每日宜忌、吉日查询等功能
"""

from datetime import datetime, timedelta
import random

def get_daily_fortune(date_str, user_bazi=None):
    """
    获取指定日期的每日宜忌信息
    
    Args:
        date_str (str): 日期字符串 "YYYY-MM-DD"
        user_bazi (dict): 用户八字信息（可选）
    
    Returns:
        dict: 每日宜忌信息
    """
    
    # 解析日期
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    
    # 天干地支日期计算（简化版本）
    day_offset = (date_obj - datetime(2000, 1, 1)).days
    tiangang = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    day_tg = tiangang[day_offset % 10]
    day_dz = dizhi[day_offset % 12]
    day_ganzhi = f"{day_tg}{day_dz}"
    
    # 基础宜忌事项
    all_activities = {
        "宜": [
            "祭祀", "祈福", "求嗣", "开光", "塑绘", "斋醮", "沐浴", "会亲友",
            "立卷", "交易", "纳财", "开市", "启钻", "安床", "结网", "畋猎",
            "取渔", "捕捉", "牧养", "安葬", "破土", "启钻", "入殓", "移柩"
        ],
        "忌": [
            "嫁娶", "出行", "搬家", "入宅", "动土", "破土", "安门", "上梁",
            "开仓", "出货财", "开渠", "掘井", "栽种", "牧养", "开厕", "造船"
        ]
    }
    
    # 根据天干地支组合决定宜忌（简化算法）
    suitable_count = 3 + (day_offset % 4)  # 3-6个宜事项
    unsuitable_count = 2 + (day_offset % 3)  # 2-4个忌事项
    
    # 设置随机种子保证同一天结果一致
    random.seed(day_offset)
    
    suitable = random.sample(all_activities["宜"], suitable_count)
    unsuitable = random.sample(all_activities["忌"], unsuitable_count)
    
    # 吉凶时辰（简化版本）
    time_fortune = generate_hourly_fortune(day_offset)
    
    # 每日运势（结合用户八字）
    personal_fortune = generate_personal_fortune(day_ganzhi, user_bazi) if user_bazi else None
    
    # 今日财神方位
    wealth_direction = get_wealth_direction(day_tg)
    
    # 今日冲煞
    conflict_zodiac = get_conflict_zodiac(day_dz)
    
    return {
        "date": date_str,
        "ganzhi": day_ganzhi,
        "suitable": suitable,
        "unsuitable": unsuitable,
        "time_fortune": time_fortune,
        "wealth_direction": wealth_direction,
        "conflict_zodiac": conflict_zodiac,
        "personal_fortune": personal_fortune,
        "overall_score": calculate_day_score(suitable_count, unsuitable_count),
        "lunar_info": get_lunar_info(date_obj)
    }

def generate_hourly_fortune(day_offset):
    """生成时辰吉凶"""
    
    hours = [
        "子时(23-01)", "丑时(01-03)", "寅时(03-05)", "卯时(05-07)",
        "辰时(07-09)", "巳时(09-11)", "午时(11-13)", "未时(13-15)",
        "申时(15-17)", "酉时(17-19)", "戌时(19-21)", "亥时(21-23)"
    ]
    
    # 简化算法：根据日期偏移决定吉凶时辰
    fortune_types = ["大吉", "吉", "平", "凶", "大凶"]
    
    time_fortune = {}
    for i, hour in enumerate(hours):
        fortune_index = (day_offset + i) % 5
        time_fortune[hour] = fortune_types[fortune_index]
    
    return time_fortune

def generate_personal_fortune(day_ganzhi, user_bazi):
    """根据用户八字生成个人运势"""
    
    if not user_bazi:
        return None
    
    user_day_master = user_bazi.get("tiangang", ["甲"])[2]  # 日主
    
    # 简化的日主与日干关系分析
    fortune_score = 50  # 基础分数
    
    # 根据天干相合相冲调整分数
    day_tg = day_ganzhi[0]
    
    if user_day_master == day_tg:
        fortune_score += 20
        fortune_desc = "今日与您的日主相同，运势较佳"
    elif is_compatible(user_day_master, day_tg):
        fortune_score += 10
        fortune_desc = "今日天干与您相合，运势平稳"
    else:
        fortune_score -= 10
        fortune_desc = "今日天干与您相冲，宜谨慎行事"
    
    return {
        "score": min(100, max(0, fortune_score)),
        "description": fortune_desc,
        "advice": get_daily_advice(fortune_score)
    }

def is_compatible(tg1, tg2):
    """判断天干是否相合"""
    compatible_pairs = [
        ("甲", "己"), ("乙", "庚"), ("丙", "辛"), ("丁", "壬"), ("戊", "癸")
    ]
    return (tg1, tg2) in compatible_pairs or (tg2, tg1) in compatible_pairs

def get_wealth_direction(day_tg):
    """获取财神方位"""
    wealth_directions = {
        "甲": "东北", "乙": "东南", "丙": "西南", "丁": "西北", "戊": "东北",
        "己": "北方", "庚": "东北", "辛": "东南", "壬": "南方", "癸": "东南"
    }
    return wealth_directions.get(day_tg, "东南")

def get_conflict_zodiac(day_dz):
    """获取冲煞生肖"""
    conflict_map = {
        "子": "马", "丑": "羊", "寅": "猴", "卯": "鸡", "辰": "狗", "巳": "猪",
        "午": "鼠", "未": "牛", "申": "虎", "酉": "兔", "戌": "龙", "亥": "蛇"
    }
    return conflict_map.get(day_dz, "无")

def get_daily_advice(fortune_score):
    """根据运势分数给出建议"""
    if fortune_score >= 80:
        return "今日运势极佳，适合进行重要决策和新的开始"
    elif fortune_score >= 60:
        return "今日运势良好，可以正常进行各项活动"
    elif fortune_score >= 40:
        return "今日运势平平，宜保持平常心，不宜冒险"
    else:
        return "今日运势不佳，宜谨慎行事，避免重要决策"

def calculate_day_score(suitable_count, unsuitable_count):
    """计算当日综合评分"""
    return min(100, max(0, (suitable_count * 20) - (unsuitable_count * 10)))

def get_lunar_info(date_obj):
    """获取农历信息（简化版本）"""
    # 这里简化处理，实际应该使用专业的农历转换
    lunar_months = ["正月", "二月", "三月", "四月", "五月", "六月",
                    "七月", "八月", "九月", "十月", "十一月", "腊月"]
    
    month_index = (date_obj.month - 2) % 12
    day_num = date_obj.day
    
    return {
        "month": lunar_months[month_index],
        "day": day_num,
        "description": f"{lunar_months[month_index]}{day_num}日"
    }

def find_auspicious_days(start_date, end_date, activity_type="general"):
    """
    查找指定时间范围内的吉日
    
    Args:
        start_date (str): 开始日期 "YYYY-MM-DD"
        end_date (str): 结束日期 "YYYY-MM-DD"
        activity_type (str): 活动类型 "wedding", "moving", "business", "general"
    
    Returns:
        list: 吉日列表
    """
    
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    auspicious_days = []
    current_date = start
    
    # 特定活动的关键词
    activity_keywords = {
        "wedding": ["嫁娶", "会亲友", "祈福"],
        "moving": ["搬家", "入宅", "安床"],
        "business": ["开市", "开业", "纳财", "交易"],
        "general": []
    }
    
    keywords = activity_keywords.get(activity_type, [])
    
    while current_date <= end:
        date_str = current_date.strftime("%Y-%m-%d")
        daily_info = get_daily_fortune(date_str)
        
        # 评估是否为吉日
        is_auspicious = False
        
        if activity_type == "general":
            # 通用吉日：宜事项多于忌事项
            is_auspicious = len(daily_info["suitable"]) > len(daily_info["unsuitable"])
        else:
            # 特定活动：包含相关宜事项
            suitable_activities = daily_info["suitable"]
            is_auspicious = any(keyword in " ".join(suitable_activities) for keyword in keywords)
        
        if is_auspicious:
            auspicious_days.append({
                "date": date_str,
                "score": daily_info["overall_score"],
                "reason": f"宜：{', '.join(daily_info['suitable'][:3])}",
                "wealth_direction": daily_info["wealth_direction"]
            })
        
        current_date += timedelta(days=1)
    
    # 按分数排序
    auspicious_days.sort(key=lambda x: x["score"], reverse=True)
    
    return auspicious_days[:10]  # 返回前10个最佳日期

if __name__ == "__main__":
    # 测试每日运势
    today = datetime.now().strftime("%Y-%m-%d")
    fortune = get_daily_fortune(today)
    print(f"今日运势 ({today}):")
    print(f"天干地支: {fortune['ganzhi']}")
    print(f"宜: {', '.join(fortune['suitable'])}")
    print(f"忌: {', '.join(fortune['unsuitable'])}")
    print(f"财神方位: {fortune['wealth_direction']}")
    print(f"综合评分: {fortune['overall_score']}")
    
    print("\n" + "="*50)
    
    # 测试吉日查询
    end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    auspicious = find_auspicious_days(today, end_date, "wedding")
    print(f"未来30天婚嫁吉日:")
    for day in auspicious[:5]:
        print(f"{day['date']} (评分: {day['score']}) - {day['reason']}")

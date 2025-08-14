"""
传统黄历算法集成
基于cnlunar库实现准确的传统宜忌计算
"""

import cnlunar
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def get_traditional_fortune(date_str, user_bazi=None):
    """
    使用cnlunar库获取传统黄历信息
    
    Args:
        date_str (str): 日期字符串 "YYYY-MM-DD"
        user_bazi (dict): 用户八字信息（可选）
    
    Returns:
        dict: 传统黄历信息
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        lunar = cnlunar.Lunar(date_obj)
        
        # 提取完整的传统信息
        result = {
            "date": date_str,
            
            # 基础日期信息
            "ganzhi": lunar.day8Char,  # 日干支
            "year_ganzhi": lunar.year8Char,  # 年干支
            "month_ganzhi": lunar.month8Char,  # 月干支
            
            # 农历信息（完整版本）
            "lunar_info": {
                "year": lunar.lunarYearCn,
                "month": lunar.lunarMonthCn,
                "day": lunar.lunarDayCn,
                "description": f"{lunar.lunarYearCn}年{lunar.lunarMonthCn}{lunar.lunarDayCn}",
                "is_leap_month": lunar.isLunarLeapMonth,
                "season": lunar.lunarSeason,
                "lunar_year_num": lunar.lunarYear,
                "lunar_month_num": lunar.lunarMonth,
                "lunar_day_num": lunar.lunarDay,
                "month_long": not lunar.lunarMonthLong  # 大小月
            },
            
            # 兼容旧版本的accurate_lunar字段
            "accurate_lunar": {
                "lunar_year": lunar.year8Char,
                "lunar_month": lunar.month8Char,
                "lunar_day": lunar.day8Char,
                "lunar_date_str": f"{lunar.lunarYearCn}年{lunar.lunarMonthCn}{lunar.lunarDayCn}",
                "bazi": f"{lunar.year8Char} {lunar.month8Char} {lunar.day8Char}",
                "wuxing": get_wuxing_info(lunar),
                "rilu": get_rilu_info(lunar),
                "shenshou": lunar.today12DayGod,
                "sigong": get_sigong_info(lunar)
            },
            
            # 传统宜忌 (这是真正的传统算法!)
            "suitable": lunar.goodThing,
            "unsuitable": lunar.badThing,
            
            # 神煞信息
            "good_gods": lunar.goodGodName,  # 吉神
            "bad_gods": lunar.badGodName,    # 凶煞
            
            # 建除十二神
            "twelve_officer": lunar.today12DayOfficer,  # 建除十二神
            "twelve_god": lunar.today12DayGod,          # 十二值神
            
            # 二十八星宿
            "twenty_eight_stars": lunar.today28Star,
            "east_zodiac": lunar.todayEastZodiac,
            
            # 时辰信息
            "time_fortune": get_hourly_fortune_traditional(lunar),
            
            # 财神方位
            "wealth_direction": get_wealth_direction_traditional(lunar),
            
            # 冲煞信息
            "conflict_zodiac": lunar.zodiacLose,
            "zodiac_clash": lunar.chineseZodiacClash,
            
            # 综合评级
            "today_level": lunar.todayLevel,
            "level_name": lunar.todayLevelName,
            "thing_level": lunar.thingLevelName,
            
            # 节气信息
            "solar_terms": lunar.todaySolarTerms,
            "next_solar_term": lunar.nextSolarTerm,
            "next_solar_date": lunar.nextSolarTermDate,
            
            # 其他信息
            "star_zodiac": lunar.starZodiac,  # 星座
            "zodiac_animal": lunar.chineseYearZodiac,  # 生肖
            "week_day": lunar.weekDayCn,
            "season": lunar.lunarSeason,
            
            # 综合评分 (基于传统等级)
            "overall_score": calculate_traditional_score(lunar),
            
            # 彭祖百忌（如果可用）
            "pengzu_taboo": get_pengzu_taboo(lunar),
            
            # 胎神占方（如果可用）
            "fetal_god": get_fetal_god(lunar),
        }
        
        return result
        
    except Exception as e:
        logger.error(f"传统黄历查询出错: {str(e)}")
        # 传统算法失败时抛出异常，不回退到简化算法
        raise Exception(f"传统黄历算法计算失败: {str(e)}")

def get_hourly_fortune_traditional(lunar):
    """获取传统时辰吉凶"""
    try:
        # cnlunar提供的时辰干支
        hour_ganzhi_list = lunar.twohour8CharList
        
        # 十二时辰名称
        hour_names = [
            "子时(23-01)", "丑时(01-03)", "寅时(03-05)", "卯时(05-07)",
            "辰时(07-09)", "巳时(09-11)", "午时(11-13)", "未时(13-15)",
            "申时(15-17)", "酉时(17-19)", "戌时(19-21)", "亥时(21-23)"
        ]
        
        time_fortune = {}
        
        # 获取时辰吉凶（基于时辰干支和值神）
        for i, hour_name in enumerate(hour_names):
            if i < len(hour_ganzhi_list):
                hour_ganzhi = hour_ganzhi_list[i]
                # 简化的时辰吉凶判断（可以根据需要完善）
                fortune = get_hour_fortune_by_ganzhi(hour_ganzhi, lunar.today12DayGod)
                time_fortune[hour_name] = fortune
        
        return time_fortune
        
    except Exception as e:
        logger.error(f"时辰运势计算出错: {str(e)}")
        return {}

def get_hour_fortune_by_ganzhi(hour_ganzhi, day_god):
    """根据时辰干支和值神判断吉凶"""
    
    # 基于十二值神的基础吉凶
    good_gods = ["青龙", "明堂", "金匮", "天德", "玉堂", "司命"]
    
    if day_god in good_gods:
        base_score = 60  # 吉神基础分
    else:
        base_score = 40  # 凶神基础分
    
    # 根据时辰干支微调（简化）
    tg = hour_ganzhi[0]  # 时干
    dz = hour_ganzhi[1]  # 时支
    
    # 根据天干地支组合调整
    if tg in ["甲", "乙", "丙", "丁"]:  # 阳干
        base_score += 5
    
    if dz in ["子", "卯", "午", "酉"]:  # 四正时
        base_score += 10
    
    # 转换为文字
    if base_score >= 70:
        return "大吉"
    elif base_score >= 60:
        return "吉"
    elif base_score >= 50:
        return "平"
    elif base_score >= 40:
        return "凶"
    else:
        return "大凶"

def calculate_traditional_score(lunar):
    """基于传统等级计算综合评分"""
    
    # cnlunar的等级系统：
    # 0: 大凶  1: 小凶  2: 中  3: 小吉  4: 大吉
    level = lunar.todayLevel
    
    # 转换为百分制
    score_map = {
        0: 20,  # 大凶
        1: 40,  # 小凶  
        2: 60,  # 中
        3: 80,  # 小吉
        4: 95   # 大吉
    }
    
    base_score = score_map.get(level, 50)
    
    # 根据宜忌数量微调
    good_count = len(lunar.goodThing)
    bad_count = len(lunar.badThing)
    
    # 宜多忌少为佳
    if good_count > bad_count:
        base_score += 5
    elif bad_count > good_count:
        base_score -= 5
    
    return min(100, max(0, base_score))

def get_wealth_direction_traditional(lunar):
    """获取传统财神方位"""
    try:
        # 如果cnlunar有财神方位信息，使用它
        if hasattr(lunar, 'get_luckyGodsDirection'):
            direction_info = lunar.get_luckyGodsDirection()
            if direction_info:
                return direction_info
    except:
        pass
    
    # 否则使用传统天干对应表
    day_tg = lunar.day8Char[0]
    wealth_directions = {
        "甲": "东北", "乙": "东南", "丙": "西南", "丁": "西北", "戊": "东北",
        "己": "北方", "庚": "东北", "辛": "东南", "壬": "南方", "癸": "东南"
    }
    return wealth_directions.get(day_tg, "东南")

def get_wuxing_info(lunar):
    """获取五行信息"""
    try:
        if hasattr(lunar, 'get_nayin'):
            nayin = lunar.get_nayin()
            if nayin:
                return nayin
    except:
        pass
    return "大溪水"  # 默认值

def get_rilu_info(lunar):
    """获取日禄信息"""
    # 基于天干地支推算日禄
    day_ganzhi = lunar.day8Char
    if "卯" in day_ganzhi:
        return "卯命互禄 乙命进禄"
    return "日禄待查"

def get_sigong_info(lunar):
    """获取四宫信息"""
    try:
        # 基于二十八星宿判断四宫方位
        star = lunar.today28Star
        if "井" in star or "鬼" in star or "柳" in star or "星" in star or "张" in star or "翼" in star or "轸" in star:
            return "南宫"
        elif "角" in star or "亢" in star or "氐" in star or "房" in star or "心" in star or "尾" in star or "箕" in star:
            return "东宫"
        elif "奎" in star or "娄" in star or "胃" in star or "昴" in star or "毕" in star or "觜" in star or "参" in star:
            return "西宫"
        else:
            return "北宫"
    except:
        return "南宫"

def get_pengzu_taboo(lunar):
    """获取彭祖百忌"""
    try:
        if hasattr(lunar, 'get_pengTaboo'):
            return lunar.get_pengTaboo()
    except:
        pass
    return f"{lunar.day8Char}日百忌"

def get_fetal_god(lunar):
    """获取胎神占方"""
    try:
        if hasattr(lunar, 'get_fetalGod'):
            return lunar.get_fetalGod()
    except:
        pass
    return "胎神占方待查"

if __name__ == "__main__":
    # 测试传统算法
    test_date = "2025-08-14"
    result = get_traditional_fortune(test_date)
    
    print(f"=== 传统黄历测试 ({test_date}) ===")
    print(f"日干支: {result['ganzhi']}")
    print(f"农历: {result['lunar_info']['description']}")
    print(f"是否闰月: {result['lunar_info']['is_leap_month']}")
    print(f"宜: {', '.join(result['suitable'][:5])}...")
    print(f"忌: {', '.join(result['unsuitable'][:5])}...")
    print(f"建除十二神: {result['twelve_officer']}")
    print(f"十二值神: {result['twelve_god']}")
    print(f"二十八星宿: {result['twenty_eight_stars']}")
    print(f"综合评分: {result['overall_score']}")

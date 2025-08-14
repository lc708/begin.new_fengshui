"""
五行分析工具
分析八字中的五行强弱、喜忌用神等
"""

def analyze_wuxing(bazi_info):
    """
    分析五行强弱和喜忌
    
    Args:
        bazi_info (dict): 八字信息
    
    Returns:
        dict: 五行分析结果
    """
    wuxing_count = bazi_info["wuxing"]
    
    # 五行相生相克关系
    shengke_relations = {
        "木": {"sheng": "火", "ke": "土", "sheng_by": "水", "ke_by": "金"},
        "火": {"sheng": "土", "ke": "金", "sheng_by": "木", "ke_by": "水"},
        "土": {"sheng": "金", "ke": "水", "sheng_by": "火", "ke_by": "木"},
        "金": {"sheng": "水", "ke": "木", "sheng_by": "土", "ke_by": "火"},
        "水": {"sheng": "木", "ke": "火", "sheng_by": "金", "ke_by": "土"}
    }
    
    # 找出五行强弱
    total_count = sum(wuxing_count.values())
    wuxing_strength = {}
    
    for element, count in wuxing_count.items():
        percentage = (count / total_count) * 100
        if percentage > 25:
            strength = "旺"
        elif percentage > 15:
            strength = "中"
        elif percentage > 5:
            strength = "弱"
        else:
            strength = "缺"
        
        wuxing_strength[element] = {
            "count": count,
            "percentage": round(percentage, 1),
            "strength": strength
        }
    
    # 找出缺失的五行
    missing_elements = [element for element, info in wuxing_strength.items() 
                       if info["strength"] == "缺"]
    
    # 找出过旺的五行
    excessive_elements = [element for element, info in wuxing_strength.items() 
                         if info["strength"] == "旺"]
    
    # 确定喜用神（简化版本）
    # 实际需要更复杂的算法考虑日主强弱、季节等因素
    favorable_elements = []
    unfavorable_elements = []
    
    if missing_elements:
        favorable_elements.extend(missing_elements)
    
    if excessive_elements:
        unfavorable_elements.extend(excessive_elements)
        # 添加能克制过旺五行的元素
        for element in excessive_elements:
            ke_by = shengke_relations[element]["ke_by"]
            if ke_by not in favorable_elements:
                favorable_elements.append(ke_by)
    
    # 如果没有明显缺失或过旺，选择较弱的五行作为喜用神
    if not favorable_elements:
        weak_elements = [element for element, info in wuxing_strength.items() 
                        if info["strength"] == "弱"]
        favorable_elements = weak_elements[:2] if weak_elements else ["木", "火"]
    
    # 生成五行建议
    recommendations = generate_wuxing_recommendations(favorable_elements, unfavorable_elements)
    
    return {
        "wuxing_strength": wuxing_strength,
        "missing_elements": missing_elements,
        "excessive_elements": excessive_elements,
        "favorable_elements": favorable_elements,
        "unfavorable_elements": unfavorable_elements,
        "recommendations": recommendations,
        "balance_score": calculate_balance_score(wuxing_strength)
    }

def generate_wuxing_recommendations(favorable, unfavorable):
    """
    根据喜忌五行生成建议
    """
    # 五行对应的颜色、方向、数字等
    element_attributes = {
        "木": {
            "colors": ["绿色", "青色", "蓝色"],
            "directions": ["东方", "东南方"],
            "numbers": [3, 8],
            "items": ["植物", "木制品", "书籍"]
        },
        "火": {
            "colors": ["红色", "紫色", "粉色"],
            "directions": ["南方"],
            "numbers": [2, 7],
            "items": ["蜡烛", "红色装饰", "电器"]
        },
        "土": {
            "colors": ["黄色", "棕色", "米色"],
            "directions": ["中央", "西南方", "东北方"],
            "numbers": [5, 10],
            "items": ["陶瓷", "石制品", "土制工艺品"]
        },
        "金": {
            "colors": ["白色", "银色", "金色"],
            "directions": ["西方", "西北方"],
            "numbers": [4, 9],
            "items": ["金属制品", "钟表", "车辆"]
        },
        "水": {
            "colors": ["黑色", "深蓝色", "灰色"],
            "directions": ["北方"],
            "numbers": [1, 6],
            "items": ["水景", "鱼缸", "镜子"]
        }
    }
    
    recommendations = {
        "lucky_colors": [],
        "lucky_directions": [],
        "lucky_numbers": [],
        "beneficial_items": [],
        "avoid_colors": [],
        "avoid_directions": [],
        "lifestyle_tips": []
    }
    
    # 根据喜用神推荐
    for element in favorable:
        attrs = element_attributes.get(element, {})
        recommendations["lucky_colors"].extend(attrs.get("colors", []))
        recommendations["lucky_directions"].extend(attrs.get("directions", []))
        recommendations["lucky_numbers"].extend(attrs.get("numbers", []))
        recommendations["beneficial_items"].extend(attrs.get("items", []))
    
    # 根据忌神避免
    for element in unfavorable:
        attrs = element_attributes.get(element, {})
        recommendations["avoid_colors"].extend(attrs.get("colors", []))
        recommendations["avoid_directions"].extend(attrs.get("directions", []))
    
    # 去重
    for key in ["lucky_colors", "lucky_directions", "lucky_numbers", 
                "beneficial_items", "avoid_colors", "avoid_directions"]:
        recommendations[key] = list(set(recommendations[key]))
    
    # 生活建议
    recommendations["lifestyle_tips"] = [
        f"多接触{'/'.join(recommendations['lucky_colors'])}的物品",
        f"居住或工作场所朝向{'/'.join(recommendations['lucky_directions'])}较为有利",
        f"选择号码或楼层时优先考虑数字{recommendations['lucky_numbers']}",
        f"避免过多使用{'/'.join(recommendations['avoid_colors'])}的装饰"
    ]
    
    return recommendations

def calculate_balance_score(wuxing_strength):
    """
    计算五行平衡分数
    """
    percentages = [info["percentage"] for info in wuxing_strength.values()]
    ideal_percentage = 20  # 理想状态下每个五行占20%
    
    deviation = sum(abs(p - ideal_percentage) for p in percentages)
    balance_score = max(0, 100 - deviation)
    
    return round(balance_score, 1)

if __name__ == "__main__":
    # 测试用例
    test_bazi = {
        "wuxing": {"木": 2, "火": 1, "土": 3, "金": 1, "水": 1},
        "tiangang": ["甲", "丙", "戊", "庚"],
        "dizhi": ["子", "午", "辰", "申"]
    }
    
    analysis = analyze_wuxing(test_bazi)
    print("五行分析结果:")
    print(f"五行强弱: {analysis['wuxing_strength']}")
    print(f"喜用神: {analysis['favorable_elements']}")
    print(f"忌神: {analysis['unfavorable_elements']}")
    print(f"平衡分数: {analysis['balance_score']}")
    print(f"幸运颜色: {analysis['recommendations']['lucky_colors']}")

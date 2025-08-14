"""
风水建议生成工具
基于用户八字信息提供风水指导
"""

def get_direction_advice(direction):
    """
    获取指定方位的风水建议
    
    Args:
        direction (str): 方位名称
    
    Returns:
        dict: 方位风水建议
    """
    # 方位对应的详细信息
    direction_map = {
        '北': {
            'element': '水',
            'color': '黑色、深蓝色',
            'beneficial': '事业运、智慧运',
            'suggestions': ['摆放水景装饰', '使用蓝黑色调', '放置镜子或玻璃制品']
        },
        '东': {
            'element': '木',
            'color': '绿色、青色',
            'beneficial': '健康运、家庭运',
            'suggestions': ['摆放绿色植物', '使用木制家具', '保持空气流通']
        },
        '南': {
            'element': '火',
            'color': '红色、紫色',
            'beneficial': '名声运、桃花运',
            'suggestions': ['使用红色装饰', '增加照明亮度', '摆放红色花卉']
        },
        '西': {
            'element': '金',
            'color': '白色、金色',
            'beneficial': '贵人运、财运',
            'suggestions': ['摆放金属制品', '使用白色主调', '保持整洁明亮']
        },
        '东南': {
            'element': '木',
            'color': '绿色、青色',
            'beneficial': '财运、学业运',
            'suggestions': ['摆放富贵竹', '使用绿色装饰', '保持明亮通风']
        },
        '西南': {
            'element': '土',
            'color': '黄色、橙色',
            'beneficial': '人际运、婚恋运',
            'suggestions': ['摆放成双摆件', '使用暖色调', '保持温馨整洁']
        },
        '东北': {
            'element': '土',
            'color': '黄色、棕色',
            'beneficial': '学业运、智慧运',
            'suggestions': ['摆放书籍文具', '使用土色调', '保持安静整齐']
        },
        '西北': {
            'element': '金',
            'color': '白色、银色',
            'beneficial': '事业运、权威运',
            'suggestions': ['摆放金属饰品', '使用白银色调', '保持威严整洁']
        }
    }
    
    return direction_map.get(direction, {
        'element': '平衡',
        'color': '中性色',
        'beneficial': '整体运势',
        'suggestions': ['保持空间整洁', '通风透光', '摆放绿色植物']
    })

def generate_fengshui_advice(user_profile, query_type="general"):
    """
    生成风水建议
    
    Args:
        user_profile (dict): 用户信息和八字分析结果
        query_type (str): 查询类型 "general", "home", "career", "relationship"
    
    Returns:
        dict: 风水建议信息
    """
    bazi_info = user_profile.get("bazi_result", {})
    analysis = user_profile.get("analysis_result", {})
    
    # 基础方位信息
    directions = {
        "北": {"element": "水", "color": "黑色", "number": 1},
        "东北": {"element": "土", "color": "黄色", "number": 8},
        "东": {"element": "木", "color": "绿色", "number": 3},
        "东南": {"element": "木", "color": "绿色", "number": 4},
        "南": {"element": "火", "color": "红色", "number": 9},
        "西南": {"element": "土", "color": "黄色", "number": 2},
        "西": {"element": "金", "color": "白色", "number": 7},
        "西北": {"element": "金", "color": "白色", "number": 6}
    }
    
    # 获取用户的喜用神
    favorable_elements = analysis.get("lucky_elements", {}).get("favorable_elements", ["木", "火"])
    
    # 根据查询类型生成不同建议
    if query_type == "general":
        return generate_general_advice(directions, favorable_elements, bazi_info)
    elif query_type == "home":
        return generate_home_advice(directions, favorable_elements, bazi_info)
    elif query_type == "career":
        return generate_career_advice(directions, favorable_elements, bazi_info)
    elif query_type == "relationship":
        return generate_relationship_advice(directions, favorable_elements, bazi_info)
    else:
        return generate_general_advice(directions, favorable_elements, bazi_info)

def generate_general_advice(directions, favorable_elements, bazi_info):
    """生成通用风水建议"""
    
    # 找出有利方位
    lucky_directions = []
    for direction, info in directions.items():
        if info["element"] in favorable_elements:
            lucky_directions.append({
                "direction": direction,
                "element": info["element"],
                "color": info["color"],
                "number": info["number"],
                "advice": f"{direction}方有利于您的运势提升"
            })
    
    # 风水罗盘建议
    compass_advice = {
        "primary_direction": lucky_directions[0]["direction"] if lucky_directions else "东南",
        "lucky_directions": [d["direction"] for d in lucky_directions],
        "beneficial_colors": [d["color"] for d in lucky_directions],
        "lucky_numbers": [d["number"] for d in lucky_directions]
    }
    
    # 通用建议
    general_tips = [
        "保持室内整洁，气场流通顺畅",
        "在有利方位摆放相应颜色的装饰品",
        "避免在休息区域摆放过多电器",
        "定期清理杂物，避免阻塞气场流动"
    ]
    
    return {
        "type": "general",
        "compass_advice": compass_advice,
        "direction_details": lucky_directions,
        "general_tips": general_tips,
        "energy_score": 85  # 模拟能量分数
    }

def generate_home_advice(directions, favorable_elements, bazi_info):
    """生成家居风水建议"""
    
    zodiac = bazi_info.get("zodiac", "龙")
    
    # 房间布局建议
    room_layout = {
        "bedroom": {
            "direction": "根据个人喜用神选择朝向",
            "colors": ["温暖色调", "避免过于鲜艳的颜色"],
            "items": ["床头靠墙", "避免梁压床", "保持通风"]
        },
        "living_room": {
            "direction": "朝向开阔处",
            "colors": ["明亮温馨色调"],
            "items": ["沙发背靠实墙", "茶几选圆形", "适当绿植"]
        },
        "kitchen": {
            "direction": "避开卧室正对",
            "colors": ["清洁明亮"],
            "items": ["保持整洁", "刀具收纳好", "通风良好"]
        }
    }
    
    # 生肖相关建议
    zodiac_tips = get_zodiac_home_tips(zodiac)
    
    return {
        "type": "home",
        "room_layout": room_layout,
        "zodiac_specific": zodiac_tips,
        "plant_recommendations": ["绿萝", "富贵竹", "发财树"],
        "avoid_items": ["尖锐装饰", "破损物品", "枯萎植物"]
    }

def generate_career_advice(directions, favorable_elements, bazi_info):
    """生成事业风水建议"""
    
    return {
        "type": "career",
        "office_direction": "面向东或南方办公",
        "desk_placement": [
            "背靠实墙坐",
            "面向门口但不正对",
            "桌面保持整洁"
        ],
        "career_colors": ["深蓝色", "棕色", "金色"],
        "beneficial_items": ["文昌塔", "水晶球", "绿色植物"],
        "meeting_directions": "选择您的吉利方位开会",
        "promotion_tips": [
            "在办公桌左侧摆放升职物品",
            "穿着有利颜色的服装",
            "选择吉利时间进行重要决策"
        ]
    }

def generate_relationship_advice(directions, favorable_elements, bazi_info):
    """生成感情风水建议"""
    
    gender = bazi_info.get("gender", "male")
    
    relationship_tips = {
        "bedroom_feng_shui": [
            "成双成对的装饰品",
            "粉色或暖色调布置",
            "避免单人照片"
        ],
        "personal_enhancement": [
            "佩戴有利颜色的配饰",
            "在桃花位摆放鲜花",
            "保持个人整洁形象"
        ],
        "date_suggestions": [
            "选择在您的吉利方位约会",
            "穿着幸运颜色的服装",
            "选择吉利日期进行重要交流"
        ]
    }
    
    # 桃花位计算（简化版本）
    peach_blossom_direction = "西南" if gender == "male" else "西北"
    
    return {
        "type": "relationship", 
        "peach_blossom_direction": peach_blossom_direction,
        "relationship_tips": relationship_tips,
        "lucky_flowers": ["玫瑰", "牡丹", "桃花"],
        "enhance_charm": [
            "在桃花位摆放鲜花",
            "佩戴粉水晶饰品",
            "保持愉悦心情"
        ]
    }

def get_zodiac_home_tips(zodiac):
    """根据生肖提供家居建议"""
    
    zodiac_advice = {
        "鼠": {"colors": ["蓝色", "黑色"], "avoid": "红色过多", "items": ["水景装饰"]},
        "牛": {"colors": ["黄色", "棕色"], "avoid": "绿色过多", "items": ["土制品"]},
        "虎": {"colors": ["绿色", "蓝色"], "avoid": "白色过多", "items": ["木制家具"]},
        "兔": {"colors": ["绿色", "红色"], "avoid": "白色", "items": ["植物装饰"]},
        "龙": {"colors": ["黄色", "金色"], "avoid": "绿色过多", "items": ["金属装饰"]},
        "蛇": {"colors": ["红色", "黄色"], "avoid": "黑色过多", "items": ["明亮灯具"]},
        "马": {"colors": ["红色", "绿色"], "avoid": "蓝色过多", "items": ["向阳装饰"]},
        "羊": {"colors": ["黄色", "红色"], "avoid": "黑色", "items": ["温暖装饰"]},
        "猴": {"colors": ["白色", "黄色"], "avoid": "红色过多", "items": ["金属工艺品"]},
        "鸡": {"colors": ["白色", "金色"], "avoid": "绿色过多", "items": ["亮色装饰"]},
        "狗": {"colors": ["黄色", "红色"], "avoid": "绿色", "items": ["土色装饰"]},
        "猪": {"colors": ["黑色", "蓝色"], "avoid": "黄色过多", "items": ["水元素装饰"]}
    }
    
    return zodiac_advice.get(zodiac, zodiac_advice["龙"])

if __name__ == "__main__":
    # 测试用例
    test_profile = {
        "bazi_result": {
            "zodiac": "龙",
            "gender": "male"
        },
        "analysis_result": {
            "lucky_elements": {
                "favorable_elements": ["木", "火"]
            }
        }
    }
    
    advice = generate_fengshui_advice(test_profile, "home")
    print("家居风水建议:")
    print(f"房间布局: {advice['room_layout']['bedroom']}")
    print(f"生肖建议: {advice['zodiac_specific']}")
    print(f"推荐植物: {advice['plant_recommendations']}")

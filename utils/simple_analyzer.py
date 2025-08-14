"""
简化的命理分析器
不依赖LLM，使用传统算法进行分析
"""

import os
from typing import Dict, List

def simple_personality_analysis(wuxing_data: Dict[str, int], zodiac: str) -> Dict:
    """
    基于五行和生肖进行简化的性格分析
    """
    total = sum(wuxing_data.values()) or 1
    ratios = {k: v/total for k, v in wuxing_data.items()}
    
    # 基础性格特征
    traits = []
    strengths = []
    weaknesses = []
    
    # 基于主要五行分析
    dominant_element = max(ratios, key=ratios.get)
    
    element_traits = {
        "木": {
            "traits": ["性格正直", "有上进心", "富有创意"],
            "strengths": ["适应能力强", "思维敏捷", "富有同情心"],
            "weaknesses": ["有时过于理想化", "情绪波动较大"]
        },
        "火": {
            "traits": ["热情开朗", "积极主动", "富有活力"],
            "strengths": ["领导能力强", "善于表达", "乐观向上"],
            "weaknesses": ["有时缺乏耐心", "容易冲动"]
        },
        "土": {
            "traits": ["性格稳重", "踏实可靠", "重视家庭"],
            "strengths": ["责任心强", "执行力好", "值得信赖"],
            "weaknesses": ["有时过于保守", "不够灵活"]
        },
        "金": {
            "traits": ["意志坚定", "原则性强", "注重细节"],
            "strengths": ["组织能力强", "效率高", "有条理"],
            "weaknesses": ["有时过于严格", "不够变通"]
        },
        "水": {
            "traits": ["智慧聪明", "善于思考", "适应性强"],
            "strengths": ["洞察力强", "善于沟通", "足智多谋"],
            "weaknesses": ["有时优柔寡断", "容易多虑"]
        }
    }
    
    if dominant_element in element_traits:
        element_info = element_traits[dominant_element]
        traits.extend(element_info["traits"])
        strengths.extend(element_info["strengths"])
        weaknesses.extend(element_info["weaknesses"])
    
    # 基于生肖补充特征
    zodiac_traits = {
        "鼠": ["机智灵活", "适应能力强"],
        "牛": ["勤劳踏实", "有耐心"],
        "虎": ["勇敢果断", "领导能力强"],
        "兔": ["温和善良", "审美能力强"],
        "龙": ["有远大理想", "具有威严"],
        "蛇": ["智慧深沉", "直觉敏锐"],
        "马": ["热情奔放", "行动力强"],
        "羊": ["温柔体贴", "有艺术天赋"],
        "猴": ["聪明机智", "多才多艺"],
        "鸡": ["勤奋负责", "注重细节"],
        "狗": ["忠诚可靠", "有正义感"],
        "猪": ["善良朴实", "知足常乐"]
    }
    
    if zodiac in zodiac_traits:
        traits.extend(zodiac_traits[zodiac])
    
    return {
        "traits": traits[:3],  # 限制为3个主要特征
        "strengths": strengths[:2],
        "weaknesses": weaknesses[:2]
    }

def simple_fortune_analysis(wuxing_data: Dict[str, int], balance_score: float) -> Dict:
    """
    简化的运势分析
    """
    fortune_level = "良好" if balance_score >= 60 else "平稳" if balance_score >= 40 else "需要调节"
    
    return {
        "career": f"事业运势{fortune_level}，建议发挥自身优势，稳步发展",
        "wealth": f"财运{fortune_level}，适合稳健理财，避免投机",
        "health": f"健康运势{fortune_level}，注意劳逸结合",
        "relationship": f"人际关系{fortune_level}，真诚待人可获得好运"
    }

def simple_lucky_elements(wuxing_data: Dict[str, int]) -> Dict:
    """
    简化的幸运元素分析
    """
    # 找到最少的元素作为需要加强的
    min_element = min(wuxing_data, key=wuxing_data.get)
    
    element_colors = {
        "木": ["绿色", "青色", "蓝绿色"],
        "火": ["红色", "橙色", "粉色"],
        "土": ["黄色", "棕色", "米色"],
        "金": ["白色", "银色", "金色"],
        "水": ["黑色", "蓝色", "深蓝色"]
    }
    
    element_numbers = {
        "木": [3, 8],
        "火": [2, 7],
        "土": [5, 0],
        "金": [4, 9],
        "水": [1, 6]
    }
    
    element_directions = {
        "木": ["东方", "东南"],
        "火": ["南方"],
        "土": ["中央", "东北", "西南"],
        "金": ["西方", "西北"],
        "水": ["北方"]
    }
    
    return {
        "colors": element_colors.get(min_element, ["绿色", "蓝色"]),
        "numbers": element_numbers.get(min_element, [3, 8]),
        "directions": element_directions.get(min_element, ["东方"])
    }

def simple_life_advice(balance_score: float, dominant_element: str) -> List[str]:
    """
    简化的人生建议
    """
    advice = [
        "保持内心平和，以诚待人，建立良好的人际关系网络",
        "在工作和生活中发挥自身优势，扬长避短"
    ]
    
    if balance_score < 50:
        advice.append("注意调节生活节奏，增强缺失的五行能量")
    
    element_advice = {
        "木": "多接触自然，培养创造力和灵活性",
        "火": "保持热情，但要学会控制情绪，避免过于冲动",
        "土": "发挥稳重的优势，同时要敞开心胸，接受新事物",
        "金": "坚持原则的同时，也要学会变通和包容",
        "水": "发挥智慧的同时，要果断行动，避免过度思虑"
    }
    
    if dominant_element in element_advice:
        advice.append(element_advice[dominant_element])
    
    return advice

def generate_simple_analysis(wuxing_data: Dict[str, int], zodiac: str, balance_score: float) -> str:
    """
    生成简化的分析结果（YAML格式）
    """
    dominant_element = max(wuxing_data, key=wuxing_data.get)
    
    personality = simple_personality_analysis(wuxing_data, zodiac)
    fortune = simple_fortune_analysis(wuxing_data, balance_score)
    lucky_elements = simple_lucky_elements(wuxing_data)
    life_advice = simple_life_advice(balance_score, dominant_element)
    
    # 格式化为YAML字符串
    yaml_content = f"""```yaml
personality:
  traits: {personality['traits']}
  strengths: {personality['strengths']}
  weaknesses: {personality['weaknesses']}

fortune:
  career: "{fortune['career']}"
  wealth: "{fortune['wealth']}"
  health: "{fortune['health']}"
  relationship: "{fortune['relationship']}"

lucky_elements:
  colors: {lucky_elements['colors']}
  numbers: {lucky_elements['numbers']}
  directions: {lucky_elements['directions']}

life_advice:
{chr(10).join(f'  - "{advice}"' for advice in life_advice)}
```"""
    
    return yaml_content

if __name__ == "__main__":
    # 测试
    test_wuxing = {"木": 1, "火": 3, "土": 2, "金": 2, "水": 0}
    test_zodiac = "马"
    test_balance = 45.0
    
    result = generate_simple_analysis(test_wuxing, test_zodiac, test_balance)
    print("简化分析结果:")
    print(result)

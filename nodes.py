"""
风水命理应用的核心节点
实现八字分析、风水建议等核心业务逻辑
"""

from macore import Node
from utils.call_llm import call_llm
from utils.bazi_calculator import calculate_bazi
from utils.wuxing_analyzer import analyze_wuxing
from utils.fengshui_advisor import generate_fengshui_advice
from utils.calendar_query import get_daily_fortune, find_auspicious_days
import json

class UserInfoCollectionNode(Node):
    """用户信息收集节点"""
    
    def prep(self, shared):
        """从共享存储中获取用户信息"""
        return shared.get("user_info", {})
    
    def exec(self, user_info):
        """验证并格式化用户输入的信息"""
        print("=== 风水命理大师 - 用户信息收集 ===")
        print("请输入您的基本信息：")
        
        print(f"姓名: {user_info['name']}")
        print(f"出生日期: {user_info['birth_date']['year']}年{user_info['birth_date']['month']}月{user_info['birth_date']['day']}日 {user_info['birth_date']['hour']}时")
        print(f"性别: {'男' if user_info['gender'] == 'male' else '女'}")
        print(f"出生地: {user_info['location']}")
        
        # 验证数据完整性
        required_fields = ["name", "birth_date", "gender", "location"]
        for field in required_fields:
            if field not in user_info or not user_info[field]:
                raise ValueError(f"缺少必要字段: {field}")
        
        return user_info
    
    def post(self, shared, prep_res, exec_res):
        """将用户信息写入共享存储"""
        shared["user_info"] = exec_res
        print("✓ 用户信息收集完成")
        return "default"

class BaziCalculationNode(Node):
    """八字计算节点"""
    
    def prep(self, shared):
        """从共享存储读取用户信息"""
        user_info = shared.get("user_info")
        if not user_info:
            raise ValueError("未找到用户信息")
        return user_info
    
    def exec(self, user_info):
        """调用八字计算工具函数"""
        print("\n=== 正在计算八字信息 ===")
        
        bazi_result = calculate_bazi(
            user_info["birth_date"],
            user_info["gender"],
            user_info["location"]
        )
        
        print(f"年柱: {bazi_result['year_pillar']}")
        print(f"月柱: {bazi_result['month_pillar']}")
        print(f"日柱: {bazi_result['day_pillar']}")
        print(f"时柱: {bazi_result['hour_pillar']}")
        print(f"生肖: {bazi_result['zodiac']}")
        print(f"纳音: {bazi_result['nayin']}")
        
        return bazi_result
    
    def post(self, shared, prep_res, exec_res):
        """将八字结果写入共享存储"""
        shared["bazi_result"] = exec_res
        print("✓ 八字计算完成")
        return "default"

class FortuneAnalysisNode(Node):
    """命理分析节点"""
    
    def prep(self, shared):
        """从共享存储读取八字和用户信息"""
        bazi_result = shared.get("bazi_result")
        user_info = shared.get("user_info")
        
        if not bazi_result or not user_info:
            raise ValueError("缺少必要的八字或用户信息")
        
        return {
            "bazi_result": bazi_result,
            "user_info": user_info
        }
    
    def exec(self, prep_data):
        """调用LLM进行命理分析"""
        print("\n=== 正在进行命理分析 ===")
        
        bazi_result = prep_data["bazi_result"]
        user_info = prep_data["user_info"]
        
        # 先进行五行分析
        wuxing_analysis = analyze_wuxing(bazi_result)
        
        # 使用LLM进行更深入的性格和运势分析
        analysis_prompt = f"""
请根据以下八字信息进行命理分析，以YAML格式输出：

用户信息：
- 姓名：{user_info['name']}
- 性别：{user_info['gender']}
- 生肖：{bazi_result['zodiac']}

八字信息：
- 年柱：{bazi_result['year_pillar']}
- 月柱：{bazi_result['month_pillar']}
- 日柱：{bazi_result['day_pillar']}
- 时柱：{bazi_result['hour_pillar']}

五行分析：
- 五行强弱：{wuxing_analysis['wuxing_strength']}
- 喜用神：{wuxing_analysis['favorable_elements']}
- 忌神：{wuxing_analysis['unfavorable_elements']}

请提供以下分析（请输出中文）：

```yaml
personality:
  traits: ["性格特点1", "性格特点2", "性格特点3"]
  strengths: ["优点1", "优点2"]
  weaknesses: ["需要注意的方面1", "需要注意的方面2"]

fortune:
  career: "事业运势分析"
  wealth: "财富运势分析"
  health: "健康运势分析"
  relationship: "感情运势分析"

lucky_elements:
  colors: ["幸运颜色1", "幸运颜色2"]
  numbers: [幸运数字1, 幸运数字2]
  directions: ["有利方位1", "有利方位2"]

life_advice:
  - "人生建议1"
  - "人生建议2"
  - "人生建议3"
```"""

        llm_response = call_llm(analysis_prompt)
        
        try:
            # 提取YAML内容
            yaml_start = llm_response.find("```yaml")
            yaml_end = llm_response.find("```", yaml_start + 7)
            
            if yaml_start != -1 and yaml_end != -1:
                yaml_content = llm_response[yaml_start + 7:yaml_end].strip()
                import yaml
                llm_analysis = yaml.safe_load(yaml_content)
            else:
                # 如果没有找到YAML格式，使用默认分析
                llm_analysis = self._get_default_analysis(bazi_result)
        except Exception as e:
            print(f"LLM分析解析失败，使用默认分析: {e}")
            llm_analysis = self._get_default_analysis(bazi_result)
        
        # 合并五行分析和LLM分析
        combined_analysis = {
            "wuxing_analysis": wuxing_analysis,
            "personality": llm_analysis.get("personality", {}),
            "fortune": llm_analysis.get("fortune", {}),
            "lucky_elements": {
                **wuxing_analysis["recommendations"],
                **llm_analysis.get("lucky_elements", {})
            },
            "life_advice": llm_analysis.get("life_advice", []),
            "balance_score": wuxing_analysis["balance_score"]
        }
        
        # 显示分析结果
        print(f"五行平衡分数: {wuxing_analysis['balance_score']}")
        print(f"喜用神: {', '.join(wuxing_analysis['favorable_elements'])}")
        print(f"幸运颜色: {', '.join(combined_analysis['lucky_elements'].get('lucky_colors', []))}")
        
        return combined_analysis
    
    def _get_default_analysis(self, bazi_result):
        """默认分析内容"""
        return {
            "personality": {
                "traits": ["性格温和", "待人友善", "做事认真"],
                "strengths": ["责任心强", "有同情心"],
                "weaknesses": ["有时过于谨慎", "需要更多自信"]
            },
            "fortune": {
                "career": "事业运势平稳，适合稳步发展",
                "wealth": "财运中等，宜理财规划",
                "health": "身体健康良好，注意劳逸结合",
                "relationship": "感情运势不错，宜真诚待人"
            },
            "lucky_elements": {
                "colors": ["绿色", "蓝色"],
                "numbers": [3, 8],
                "directions": ["东方", "南方"]
            },
            "life_advice": [
                "保持积极心态，勇于面对挑战",
                "重视人际关系，诚待他人",
                "注意身体健康，适度运动"
            ]
        }
    
    def post(self, shared, prep_res, exec_res):
        """将分析结果写入共享存储"""
        shared["analysis_result"] = exec_res
        print("✓ 命理分析完成")
        return "default"

class FengshuiAdviceNode(Node):
    """风水建议节点"""
    
    def prep(self, shared):
        """从共享存储读取八字和分析结果"""
        bazi_result = shared.get("bazi_result")
        analysis_result = shared.get("analysis_result")
        user_info = shared.get("user_info")
        
        if not all([bazi_result, analysis_result, user_info]):
            raise ValueError("缺少必要信息进行风水分析")
        
        return {
            "user_profile": {
                "bazi_result": bazi_result,
                "analysis_result": analysis_result,
                "user_info": user_info
            }
        }
    
    def exec(self, prep_data):
        """调用LLM生成风水建议"""
        print("\n=== 正在生成风水建议 ===")
        
        user_profile = prep_data["user_profile"]
        
        # 生成不同类型的风水建议
        advice_types = ["general", "home", "career", "relationship"]
        all_advice = {}
        
        for advice_type in advice_types:
            advice = generate_fengshui_advice(user_profile, advice_type)
            all_advice[advice_type] = advice
            
            print(f"✓ {advice_type} 风水建议生成完成")
        
        return all_advice
    
    def post(self, shared, prep_res, exec_res):
        """将风水建议写入共享存储"""
        shared["fengshui_advice"] = exec_res
        print("✓ 风水建议生成完成")
        return "default"

class DailyQueryNode(Node):
    """日常查询节点"""
    
    def prep(self, shared):
        """从共享存储读取用户信息"""
        user_info = shared.get("user_info")
        bazi_result = shared.get("bazi_result")
        
        if not user_info:
            raise ValueError("缺少用户信息")
        
        return {
            "user_info": user_info,
            "bazi_result": bazi_result
        }
    
    def exec(self, prep_data):
        """调用日历查询工具函数"""
        print("\n=== 正在查询每日运势 ===")
        
        from datetime import datetime, timedelta
        
        user_info = prep_data["user_info"]
        bazi_result = prep_data["bazi_result"]
        
        # 获取今日运势
        today = datetime.now().strftime("%Y-%m-%d")
        daily_fortune = get_daily_fortune(today, bazi_result)
        
        # 查找未来30天的吉日
        end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        auspicious_days = find_auspicious_days(today, end_date, "general")
        
        print(f"今日运势 ({today}):")
        print(f"天干地支: {daily_fortune['ganzhi']}")
        print(f"宜: {', '.join(daily_fortune['suitable'][:3])}")
        print(f"忌: {', '.join(daily_fortune['unsuitable'][:2])}")
        print(f"财神方位: {daily_fortune['wealth_direction']}")
        print(f"综合评分: {daily_fortune['overall_score']}")
        
        return {
            "today_fortune": daily_fortune,
            "auspicious_days": auspicious_days[:5],  # 返回前5个最佳日期
            "query_date": today
        }
    
    def post(self, shared, prep_res, exec_res):
        """将日常信息写入共享存储"""
        shared["daily_info"] = exec_res
        print("✓ 日常查询完成")
        return "default"

class ResultIntegrationNode(Node):
    """结果整合节点"""
    
    def prep(self, shared):
        """从共享存储读取所有分析结果"""
        required_keys = ["user_info", "bazi_result", "analysis_result", 
                        "fengshui_advice", "daily_info"]
        
        prep_data = {}
        for key in required_keys:
            if key not in shared:
                raise ValueError(f"缺少必要数据: {key}")
            prep_data[key] = shared[key]
        
        return prep_data
    
    def exec(self, prep_data):
        """调用LLM生成综合报告"""
        print("\n=== 正在生成综合命理报告 ===")
        
        # 使用LLM生成综合报告
        report_prompt = f"""
请根据以下信息生成一份完整的风水命理报告，以YAML格式输出：

用户基本信息：
- 姓名：{prep_data['user_info']['name']}
- 生肖：{prep_data['bazi_result']['zodiac']}
- 八字：{prep_data['bazi_result']['year_pillar']} {prep_data['bazi_result']['month_pillar']} {prep_data['bazi_result']['day_pillar']} {prep_data['bazi_result']['hour_pillar']}

五行平衡分数：{prep_data['analysis_result']['balance_score']}
今日运势评分：{prep_data['daily_info']['today_fortune']['overall_score']}

请生成一份简洁明了的综合报告：

```yaml
summary:
  title: "个人命理风水综合报告"
  user_name: "{prep_data['user_info']['name']}"
  generation_date: "{prep_data['daily_info']['query_date']}"
  
overview:
  bazi_summary: "八字简要说明"
  wuxing_summary: "五行特点总结"
  fortune_summary: "整体运势概述"

recommendations:
  daily_practice: ["日常建议1", "日常建议2"]
  feng_shui_tips: ["风水建议1", "风水建议2"]
  lucky_items: ["幸运物品1", "幸运物品2"]

conclusion: "总结性建议"
```"""

        try:
            llm_response = call_llm(report_prompt)
            
            # 提取YAML内容
            yaml_start = llm_response.find("```yaml")
            yaml_end = llm_response.find("```", yaml_start + 7)
            
            if yaml_start != -1 and yaml_end != -1:
                yaml_content = llm_response[yaml_start + 7:yaml_end].strip()
                import yaml
                report = yaml.safe_load(yaml_content)
            else:
                report = self._get_default_report(prep_data)
        except Exception as e:
            print(f"报告生成失败，使用默认模板: {e}")
            report = self._get_default_report(prep_data)
        
        # 添加详细数据引用
        comprehensive_report = {
            "summary_report": report,
            "detailed_data": {
                "user_info": prep_data["user_info"],
                "bazi_analysis": prep_data["bazi_result"],
                "fortune_analysis": prep_data["analysis_result"],
                "fengshui_advice": prep_data["fengshui_advice"],
                "daily_fortune": prep_data["daily_info"]
            },
            "generation_timestamp": prep_data["daily_info"]["query_date"]
        }
        
        print("✓ 综合报告生成完成")
        
        return comprehensive_report
    
    def _get_default_report(self, prep_data):
        """默认报告模板"""
        return {
            "summary": {
                "title": "个人命理风水综合报告",
                "user_name": prep_data['user_info']['name'],
                "generation_date": prep_data['daily_info']['query_date']
            },
            "overview": {
                "bazi_summary": f"您的八字为{prep_data['bazi_result']['year_pillar']} {prep_data['bazi_result']['month_pillar']} {prep_data['bazi_result']['day_pillar']} {prep_data['bazi_result']['hour_pillar']}，生肖{prep_data['bazi_result']['zodiac']}",
                "wuxing_summary": f"五行平衡分数{prep_data['analysis_result']['balance_score']}，整体较为均衡",
                "fortune_summary": "运势稳定，适合稳步发展"
            },
            "recommendations": {
                "daily_practice": ["保持心态平和", "多接触自然环境"],
                "feng_shui_tips": ["居住环境保持整洁", "选择有利方位"],
                "lucky_items": ["绿色植物", "天然水晶"]
            },
            "conclusion": "建议您保持积极心态，合理规划生活，定期关注运势变化。"
        }
    
    def post(self, shared, prep_res, exec_res):
        """将最终结果写入共享存储"""
        shared["final_report"] = exec_res
        print("✓ 结果整合完成")
        
        # 显示简要报告
        print("\n" + "="*50)
        print("🎊 风水命理分析完成！")
        print("="*50)
        
        report = exec_res["summary_report"]
        print(f"用户：{report['summary']['user_name']}")
        print(f"日期：{report['summary']['generation_date']}")
        print(f"\n概述：{report['overview']['bazi_summary']}")
        print(f"五行：{report['overview']['wuxing_summary']}")
        print(f"运势：{report['overview']['fortune_summary']}")
        
        print(f"\n建议：")
        for tip in report['recommendations']['daily_practice']:
            print(f"• {tip}")
        
        print(f"\n{report['conclusion']}")
        print("="*50)
        
        return "default"
"""
风水命理应用主程序
提供完整的风水命理分析功能
"""

from flow import create_fengshui_analysis_flow, create_bazi_only_flow, create_fengshui_consultation_flow, create_quick_daily_flow
import sys

def display_menu():
    """显示主菜单"""
    print("\n" + "="*50)
    print("🏮 欢迎使用风水命理大师 🏮")
    print("="*50)
    print("请选择您需要的服务：")
    print("1. 完整命理分析（八字+风水+运势）")
    print("2. 八字命理分析")
    print("3. 风水咨询")
    print("4. 每日运势查询")
    print("5. 退出")
    print("="*50)

def main():
    """主程序入口"""
    
    while True:
        display_menu()
        
        try:
            choice = input("请输入您的选择 (1-5): ").strip()
            
            if choice == "1":
                run_full_analysis()
            elif choice == "2":
                run_bazi_analysis()
            elif choice == "3":
                run_fengshui_consultation()
            elif choice == "4":
                run_daily_fortune()
            elif choice == "5":
                print("\n感谢使用风水命理大师，祝您吉祥如意！🎋")
                break
            else:
                print("⚠️ 无效选择，请输入1-5之间的数字")
                
        except KeyboardInterrupt:
            print("\n\n感谢使用风水命理大师，祝您吉祥如意！🎋")
            break
        except Exception as e:
            print(f"❌ 程序执行出错: {e}")
            print("请重新尝试...")

def run_full_analysis():
    """运行完整命理分析"""
    print("\n🎯 开始完整命理分析...")
    
    shared = {
        "service_type": "full_analysis"
    }
    
    try:
        # 创建完整分析流程
        flow = create_fengshui_analysis_flow()
        
        # 运行流程
        result = flow.run(shared)
        
        print("\n✨ 完整分析已完成！您可以参考以上建议安排生活。")
        
        # 询问是否保存报告
        save_choice = input("\n是否需要保存分析报告？(y/n): ").strip().lower()
        if save_choice in ['y', 'yes', '是']:
            save_report(shared.get("final_report"), "完整分析报告")
            
    except Exception as e:
        print(f"❌ 分析过程中出错: {e}")

def run_bazi_analysis():
    """运行八字命理分析"""
    print("\n🎯 开始八字命理分析...")
    
    shared = {
        "service_type": "bazi_only"
    }
    
    try:
        flow = create_bazi_only_flow()
        result = flow.run(shared)
        
        print("\n✨ 八字分析已完成！")
        
        # 显示分析结果摘要
        if "analysis_result" in shared:
            analysis = shared["analysis_result"]
            print(f"\n📊 五行平衡分数: {analysis.get('balance_score', 'N/A')}")
            
            lucky_elements = analysis.get('lucky_elements', {})
            if lucky_elements.get('lucky_colors'):
                print(f"🎨 幸运颜色: {', '.join(lucky_elements['lucky_colors'][:3])}")
            
        save_choice = input("\n是否需要保存分析报告？(y/n): ").strip().lower()
        if save_choice in ['y', 'yes', '是']:
            save_report(shared, "八字分析报告")
            
    except Exception as e:
        print(f"❌ 分析过程中出错: {e}")

def run_fengshui_consultation():
    """运行风水咨询"""
    print("\n🎯 开始风水咨询...")
    
    shared = {
        "service_type": "fengshui_consultation"
    }
    
    try:
        flow = create_fengshui_consultation_flow()
        result = flow.run(shared)
        
        print("\n✨ 风水咨询已完成！")
        
        # 显示风水建议摘要
        if "fengshui_advice" in shared:
            advice = shared["fengshui_advice"]
            general_advice = advice.get("general", {})
            
            if general_advice.get("compass_advice"):
                compass = general_advice["compass_advice"]
                print(f"🧭 主要吉利方位: {compass.get('primary_direction', 'N/A')}")
                if compass.get('beneficial_colors'):
                    print(f"🌈 有利颜色: {', '.join(compass['beneficial_colors'][:3])}")
        
        save_choice = input("\n是否需要保存咨询报告？(y/n): ").strip().lower()
        if save_choice in ['y', 'yes', '是']:
            save_report(shared, "风水咨询报告")
            
    except Exception as e:
        print(f"❌ 咨询过程中出错: {e}")

def run_daily_fortune():
    """运行每日运势查询"""
    print("\n🎯 开始每日运势查询...")
    
    shared = {
        "service_type": "daily_fortune",
        "user_info": {
            "name": "用户",
            "birth_date": {"year": 1990, "month": 1, "day": 1, "hour": 12},
            "gender": "male",
            "location": "北京"
        }
    }
    
    try:
        flow = create_quick_daily_flow()
        result = flow.run(shared)
        
        print("\n✨ 每日运势查询已完成！")
        
        # 显示运势摘要
        if "daily_info" in shared:
            daily = shared["daily_info"]["today_fortune"]
            print(f"\n📅 今日天干地支: {daily['ganzhi']}")
            print(f"💰 财神方位: {daily['wealth_direction']}")
            print(f"⭐ 综合评分: {daily['overall_score']}/100")
            
    except Exception as e:
        print(f"❌ 查询过程中出错: {e}")

def save_report(data, report_type):
    """保存分析报告到文件"""
    try:
        from datetime import datetime
        import json
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{report_type}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"📄 报告已保存到: {filename}")
        
    except Exception as e:
        print(f"❌ 保存报告失败: {e}")

def demo_run():
    """演示运行（用于测试）"""
    print("🧪 开始演示模式...")
    
    shared = {
        "service_type": "demo"
    }
    
    try:
        flow = create_fengshui_analysis_flow()
        result = flow.run(shared)
        
        print("\n✅ 演示运行完成！")
        
        return shared
        
    except Exception as e:
        print(f"❌ 演示运行失败: {e}")
        return None

if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        # 演示模式
        demo_run()
    else:
        # 正常交互模式
        main()
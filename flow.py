"""
风水命理应用的流程定义
连接各个节点形成完整的分析流程
"""

from macore import Flow
from nodes import (
    UserInfoCollectionNode,
    BaziCalculationNode, 
    FortuneAnalysisNode,
    FengshuiAdviceNode,
    DailyQueryNode,
    ResultIntegrationNode
)

def create_fengshui_analysis_flow():
    """创建风水命理分析流程"""
    
    # 创建各个节点实例
    user_input = UserInfoCollectionNode()
    bazi_calc = BaziCalculationNode()
    fortune_analysis = FortuneAnalysisNode()
    fengshui_advice = FengshuiAdviceNode()
    daily_query = DailyQueryNode()
    result_integration = ResultIntegrationNode()
    
    # 连接节点形成流程
    # 用户信息收集 -> 八字计算 -> 命理分析 -> 风水建议 -> 日常查询 -> 结果整合
    user_input >> bazi_calc >> fortune_analysis >> fengshui_advice >> daily_query >> result_integration
    
    # 创建并返回流程
    return Flow(start=user_input)

def create_quick_daily_flow():
    """创建快速每日运势查询流程（已有用户信息的情况）"""
    
    daily_query = DailyQueryNode()
    
    return Flow(start=daily_query)

def create_bazi_only_flow():
    """创建仅八字分析流程"""
    
    user_input = UserInfoCollectionNode()
    bazi_calc = BaziCalculationNode()
    fortune_analysis = FortuneAnalysisNode()
    
    # 简化流程：用户输入 -> 八字计算 -> 命理分析
    user_input >> bazi_calc >> fortune_analysis
    
    return Flow(start=user_input)

def create_fengshui_consultation_flow():
    """创建风水咨询流程（需要完整八字信息）"""
    
    user_input = UserInfoCollectionNode()
    bazi_calc = BaziCalculationNode()
    fortune_analysis = FortuneAnalysisNode()
    fengshui_advice = FengshuiAdviceNode()
    
    # 风水咨询流程
    user_input >> bazi_calc >> fortune_analysis >> fengshui_advice
    
    return Flow(start=user_input)

if __name__ == "__main__":
    """测试流程创建"""
    
    print("=== 测试流程创建 ===")
    
    # 测试完整分析流程
    full_flow = create_fengshui_analysis_flow()
    print("✓ 完整分析流程创建成功")
    
    # 测试八字分析流程
    bazi_flow = create_bazi_only_flow()
    print("✓ 八字分析流程创建成功")
    
    # 测试风水咨询流程
    fengshui_flow = create_fengshui_consultation_flow()
    print("✓ 风水咨询流程创建成功")
    
    print("所有流程创建测试完成！")
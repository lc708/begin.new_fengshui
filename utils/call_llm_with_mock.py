import os
from typing import Optional
import dotenv

dotenv.load_dotenv()

def call_llm(prompt: str, provider: Optional[str] = None) -> str:
    """
    Call LLM with support for multiple providers.
    
    Args:
        prompt: The prompt to send to the LLM
        provider: LLM provider to use ('openai', 'gemini', 'deepseek'). 
                 If None, uses LLM_PROVIDER env var or defaults to 'openai'
    
    Returns:
        The LLM response as a string
    """
    # Determine provider
    if provider is None:
        provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    if provider == "openai":
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️ 未设置OPENAI_API_KEY，使用模拟LLM响应")
            return generate_mock_response(prompt)
        
        client = OpenAI(api_key=api_key)
        model = os.getenv("OPENAI_MODEL", "gpt-5-mini")
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    elif provider == "gemini":
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("Please install google-generativeai: pip install google-generativeai")
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
        response = model.generate_content(prompt)
        return response.text
    
    elif provider == "deepseek":
        from openai import OpenAI
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
        
        # DeepSeek uses OpenAI-compatible API
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
        model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    else:
        raise ValueError(f"Unsupported provider: {provider}. Choose from: openai, gemini, deepseek")

def generate_mock_response(prompt):
    """生成模拟LLM响应，用于演示和测试"""
    
    # 检查是否是命理分析请求
    if "YAML格式输出" in prompt and "personality" in prompt:
        return """```yaml
personality:
  traits: ["性格温和稳重", "做事踏实可靠", "具有责任感"]
  strengths: ["意志坚定", "善于倾听他人"]
  weaknesses: ["有时过于谨慎", "需要增强自信心"]

fortune:
  career: "事业运势稳中有升，适合在现有基础上稳步发展，贵人运较好"
  wealth: "财运平稳，正财运佳，适合稳健投资，避免投机"
  health: "身体健康状况良好，注意劳逸结合，保持规律作息"
  relationship: "感情运势和谐，人际关系良好，利于建立长久关系"

lucky_elements:
  colors: ["绿色", "蓝色", "白色"]
  numbers: [3, 8, 6]
  directions: ["东方", "南方", "西北"]

life_advice:
  - "保持内心平和，以诚待人，建立良好的人际关系网络"
  - "在事业上脚踏实地，不急于求成，稳步积累经验和资源"
  - "注重身心健康，定期运动，保持积极乐观的生活态度"
```"""
    
    # 检查是否是综合报告请求
    elif "综合报告" in prompt and "YAML格式输出" in prompt:
        return """```yaml
summary:
  title: "个人命理风水综合报告"
  user_name: "张三"
  generation_date: "2025-08-14"
  
overview:
  bazi_summary: "您的八字庚午 壬巳 己巳 辛未，生肖马，五行以火土为主，性格温和踏实"
  wuxing_summary: "五行分布较为均衡，火元素略旺，土元素稳定，整体能量协调"
  fortune_summary: "整体运势平稳向上，适合稳健发展，人际关系良好"

recommendations:
  daily_practice: ["晨起面向东方深呼吸", "多接触绿色植物和自然环境"]
  feng_shui_tips: ["居住环境以清洁整齐为主", "工作位置选择背靠实墙面向开阔处"]
  lucky_items: ["绿色水晶", "竹制工艺品", "天然木制品"]

conclusion: "建议您保持现有的稳健作风，在人际交往中以诚相待，事业发展不急不躁，定能获得长久的成功和幸福。"
```"""
    
    # 默认响应
    return "这是一个模拟的LLM响应，用于演示系统功能。实际使用时请配置对应的API密钥环境变量。"

if __name__ == "__main__":
    # Test with different providers
    test_prompt = "Hello, how are you? Please respond in one sentence."
    
    print("Testing LLM providers...")
    print("-" * 50)
    
    # Test current provider
    try:
        current_provider = os.getenv("LLM_PROVIDER", "openai")
        print(f"Current provider ({current_provider}):")
        response = call_llm(test_prompt)
        print(f"Response: {response}")
        print("-" * 50)
    except Exception as e:
        print(f"Error: {e}")
        print("-" * 50)

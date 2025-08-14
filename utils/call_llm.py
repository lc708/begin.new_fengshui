import os
from typing import Optional
import dotenv

# 加载环境变量，优先加载.env.local
dotenv.load_dotenv('.env.local')
dotenv.load_dotenv('.env')

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
            raise ValueError("❌ OPENAI_API_KEY not found in environment variables. Please set API key to use LLM features.")
        
        client = OpenAI(api_key=api_key)
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
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
            raise ValueError("❌ GEMINI_API_KEY not found in environment variables. Please set API key to use LLM features.")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
        response = model.generate_content(prompt)
        return response.text
    
    elif provider == "deepseek":
        from openai import OpenAI
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("❌ DEEPSEEK_API_KEY not found in environment variables. Please set API key to use LLM features.")
        
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

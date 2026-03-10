#!/usr/bin/env python3
"""
LLM-based Code Analysis (Optional)
"""

from typing import Optional


class LLMAnalyzer:
    """Optional LLM enhancement using LangChain"""
    
    def __init__(self, provider: str = "openai", model: str = None):
        """Initialize LLM analyzer"""
        self.enabled = False
        self.provider = provider.lower()
        self.model = model or self._get_default_model()
        
        try:
            from langchain_openai import ChatOpenAI
            from langchain_community.llms import Ollama
            from langchain.prompts import PromptTemplate
            from langchain.chains import LLMChain
            
            if self.provider == "openai":
                import os
                api_key = os.getenv('OPENAI_API_KEY')
                if not api_key:
                    print("⚠ OPENAI_API_KEY not set")
                    return
                
                self.llm = ChatOpenAI(model=self.model, api_key=api_key, max_tokens=500)
                self.enabled = True
                print(f"✓ OpenAI LLM initialized ({self.model})")
            
            elif self.provider == "ollama":
                self.llm = Ollama(model=self.model, base_url="http://localhost:11434")
                self.enabled = True
                print(f"✓ Ollama LLM initialized ({self.model})")
            
            self.prompt = PromptTemplate(
                template="Describe this Java class in 1-2 sentences:\n{code}",
                input_variables=["code"]
            )
            
            if self.enabled:
                self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
        
        except ImportError:
            print("⚠ LangChain not installed. LLM disabled.")
            print("  Install with: pip install langchain langchain-openai langchain-community")
        except Exception as e:
            print(f"⚠ LLM initialization failed: {str(e)}")
    
    def _get_default_model(self) -> str:
        """Get default model for provider"""
        return "gpt-3.5-turbo" if self.provider == "openai" else "llama2"
    
    def analyze(self, code: str) -> str:
        """Get LLM description of code"""
        if not self.enabled:
            return ""
        
        try:
            limited_code = code[:1000]
            result = self.chain.run(code=limited_code)
            return result.strip()[:200]
        except Exception:
            return ""
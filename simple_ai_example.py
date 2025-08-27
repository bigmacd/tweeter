#!/usr/bin/env python3
"""
Simple example of using the AI client
"""

from ai_client import AIClient

def main():
    # Quick examples of asking questions to AI
    
    # Using OpenAI (requires OPENAI_API_KEY environment variable)
    try:
        print("🤖 Using OpenAI...")
        ai = AIClient("openai")
        
        # Simple question
        answer = ai.ask("What's 2+2?")
        print(f"Q: What's 2+2?\nA: {answer}\n")
        
        # Question with context
        context = "You are a Python programming expert."
        answer = ai.ask("How do I create a list in Python?", context)
        print(f"Q: How do I create a list in Python?\nA: {answer}\n")
        
    except Exception as e:
        print(f"OpenAI not available: {e}\n")
    
    # Using Anthropic Claude (requires ANTHROPIC_API_KEY environment variable)
    try:
        print("🤖 Using Claude...")
        ai = AIClient("anthropic")
        answer = ai.ask("Explain recursion in simple terms.")
        print(f"Q: Explain recursion in simple terms.\nA: {answer}\n")
        
    except Exception as e:
        print(f"Anthropic not available: {e}\n")
    
    # Using local Ollama (requires Ollama to be running locally)
    try:
        print("🤖 Using Ollama...")
        ai = AIClient("ollama", model="llama2")
        answer = ai.ask("What is the meaning of life?")
        print(f"Q: What is the meaning of life?\nA: {answer}\n")
        
    except Exception as e:
        print(f"Ollama not available: {e}\n")

def interactive_demo():
    """Start an interactive chat session"""
    print("Choose your AI provider:")
    print("1. OpenAI")
    print("2. Anthropic (Claude)")
    print("3. Ollama (Local)")
    
    choice = input("Enter choice (1-3): ").strip()
    
    try:
        if choice == "1":
            ai = AIClient("openai")
        elif choice == "2":
            ai = AIClient("anthropic")
        elif choice == "3":
            model = input("Enter Ollama model (default: llama2): ").strip() or "llama2"
            ai = AIClient("ollama", model=model)
        else:
            print("Invalid choice!")
            return
        
        ai.chat()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Run basic examples
    main()
    
    # Uncomment to try interactive mode
    # interactive_demo()

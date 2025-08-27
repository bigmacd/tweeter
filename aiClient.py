#!/usr/bin/env python3
"""
AI Client for asking simple questions to various AI providers
Supports OpenAI, Anthropic (Claude), and local models via Ollama
"""

import os
import requests
import json
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

from openai import OpenAI as OpenAIClient



class OpenAI():
    """OpenAI API provider (GPT models)"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        
        self.api_key = api_key or os.getenv('openaiApiKey')
        self.model = model
        self.base_url = "https://api.openai.com/v1"
        
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
    
    def ask_question(self, question: str, context: Optional[str] = None) -> str:
        """Ask a question using OpenAI's API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if context:
            messages.append({"role": "system", "content": context})
        messages.append({"role": "user", "content": question})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenAI API request failed: {str(e)}")


class Anthropic():
    """Anthropic Claude API provider"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-haiku-20240307"):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.model = model
        self.base_url = "https://api.anthropic.com/v1"
        
        if not self.api_key:
            raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable.")
    
    def ask_question(self, question: str, context: Optional[str] = None) -> str:
        """Ask a question using Anthropic's Claude API"""
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        prompt = question
        if context:
            prompt = f"Context: {context}\n\nQuestion: {question}"
        
        data = {
            "model": self.model,
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/messages",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result['content'][0]['text'].strip()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Anthropic API request failed: {str(e)}")


class Ollama():
    """Local Ollama provider"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url.rstrip('/')
        self.model = model
        
        # Test if Ollama is running
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            raise Exception(f"Ollama not accessible at {self.base_url}. Make sure Ollama is running.")
    
    def ask_question(self, question: str, context: Optional[str] = None) -> str:
        """Ask a question using local Ollama"""
        prompt = question
        if context:
            prompt = f"Context: {context}\n\nQuestion: {question}"
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=data,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            return result['response'].strip()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama request failed: {str(e)}")



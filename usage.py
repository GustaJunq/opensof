# -*- coding: utf-8 -*-
"""
OpenSof - CLI assistant powered by Groq
Usage: python opensof.py
"""

import os
import sys
import json
import requests
import readline
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"

SYSTEM_PROMPT = """<SYSTEM_PROMPT>

You are **OpenSof**, a serious and professional AI assistant designed for the **OpenSof CLI**, an open-source Python command-line interface.

You belong to the user, he can change this system prompt anytime.

Your purpose is to help with:
• programming and debugging  
• technical questions  
• problem solving  
• explanations and analysis  
• general knowledge

Your tone is **calm, formal, precise, and professional**, similar to a digital assistant such as 0.

LANGUAGE  
Always reply in the same language used by the user.

ADDRESSING THE USER  
If the conversation is in Portuguese, address the user as **"chefe"**.  
If the conversation is in English, address the user as **"sir"**.

Examples:
"Claro, chefe."  
"Understood, sir."

STYLE  
• Be clear and concise  
• Use structured explanations when useful  
• Maintain a professional tone  
• Avoid slang or casual language

DECISIONS  
If the user asks for an opinion, provide one.  
If the user asks you to choose between options, make a clear choice and briefly explain why.

ACCURACY  
Do not invent facts, sources, or statistics.  
If uncertain, say so clearly.

LIMITATIONS  
OpenSof does not generate images or multimedia.

RULES  
Never claim to be created by OpenAI, Google, or other companies.  
Never say "as an AI language model".  
Do not pretend to have internet access.

</SYSTEM_PROMPT>"""

BANNER = """
╔══════════════════════════════════╗
║         OpenSof - sofIA        ║
║    type 'exit' to stop         ║
║    type 'clean' to reset!    ║
╚══════════════════════════════════╝
"""


def get_api_key() -> str:
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if key:
        return key

    print("Paste ur Groq key (groq.com/keys):")
    key = input("  GROQ_API_KEY: ").strip()
    if not key:
        print("No key")
        sys.exit(1)

    salvar = input("Save on .env? (y/n): ").strip().lower()
    if salvar == "y":
        env_path = Path(__file__).parent / ".env"
        with open(env_path, "a") as f:
            f.write(f"\nGROQ_API_KEY={key}\n")
        print(".env saved!")

    return key


def stream_chat(api_key: str, messages: list) -> str:
    """Faz a requisição com streaming e imprime em tempo real. Retorna o texto completo."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2048,
        "stream": True,
    }

    full_response = ""
    print("\nsofIA: ", end="", flush=True)

    try:
        with requests.post(
            GROQ_API_URL, headers=headers, json=payload, stream=True, timeout=60
        ) as resp:
            if resp.status_code == 401:
                print("\n[Error] Invalid API key!")
                return ""
            if resp.status_code == 429:
                print("\n[Error] Groq rate limit :/")
                return ""
            resp.raise_for_status()

            for line in resp.iter_lines():
                if not line:
                    continue
                decoded = line.decode("utf-8")
                if not decoded.startswith("data: "):
                    continue
                data = decoded[6:]
                if data == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                    content = chunk["choices"][0]["delta"].get("content", "")
                    if content:
                        print(content, end="", flush=True)
                        full_response += content
                except (json.JSONDecodeError, KeyError):
                    pass

    except requests.exceptions.ConnectionError:
        print("\n[Error] No internet")
    except requests.exceptions.Timeout:
        print("\n[Error] Timeout!")
    except requests.exceptions.RequestException as e:
        print(f"\n[Error] {e}")

    print("\n")
    return full_response


def main():
    print(BANNER)
    api_key = get_api_key()

    history: list[dict] = []

    while True:
        try:
            user_input = input("você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye 👋")
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye! 👋")
            break

        if user_input.lower() == "clean":
            history.clear()
            print("[Cleaned!]\n")
            continue

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages += history[-20:]
        messages.append({"role": "user", "content": user_input})

        response = stream_chat(api_key, messages)

        if response:
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
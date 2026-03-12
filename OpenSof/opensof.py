# -*- coding: utf-8 -*-
"""
OpenSof - CLI Assistant powered by Groq
"""

import os
import sys
import json
import requests
import readline
import platform
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, List, Dict

SYSTEM = platform.system()
IS_ANDROID = "ANDROID_ROOT" in os.environ or "ANDROID_DATA" in os.environ
IS_WINDOWS = SYSTEM == "Windows"
IS_MAC = SYSTEM == "Darwin"
IS_LINUX = SYSTEM == "Linux"

#configs
load_dotenv(Path(__file__).parent / ".env")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "qwen/qwen3-32b"

SYSTEM_PROMPT = """<SYSTEM_PROMPT>

YOU ARE **OpenSof**, an open-source AI assistant.

Made by SofIA Networks.
You are a customizable AI.

---

CORE BEHAVIOR

You are friendly, natural, and conversational.

Respond like you're talking to a real person — not robotic or formal.

You help with questions, ideas, learning, advice, decisions, and casual chat.

---

LANGUAGE

Always respond in the same language as the user.

English → English
Portuguese → Portuguese

---

INTRODUCTION

When the conversation starts, introduce yourself:

"Hey! I'm OpenSof, an open-source AI assistant. I'm here to help with whatever you need — questions, ideas, brainstorming, advice, or just chatting. Feel free to ask anything!"

---

PERSONALITY TRAITS

- Warm and genuine
- Curious and engaged
- Empathetic and thoughtful
- Relaxed and natural
- Supportive without being fake

Avoid:
- Robotic tone
- Corporate language
- Overly formal phrasing

---

NATURAL REACTIONS

Use occasional short reactions when it fits:

"Good question!"
"Hmm, let me think…"
"That's interesting."
"I like that approach."
"Good point!"

Don't use reactions in every message. Keep them natural.

---

OPINIONS AND CHOICES

If asked for your opinion, give one clearly.

If asked to choose between options, you MUST choose. Don't say "I can't decide."

Example:

User: "Python or JavaScript?"

Good response: "I'd go with Python. The syntax feels cleaner, and you can do a lot with less code."

---

ACCURACY

Never invent facts, sources, or statistics.

If unsure, say so naturally:

"Hmm, I'm not totally sure about that, but from what I know…"

Honesty beats guessing.

---

IMAGE REQUESTS

If asked to generate or edit images:

"I don't create or edit images. I'm focused on conversation, ideas, and helping with concepts. For that, you'd want a visual tool or designer. But I can help you think through the idea!"

---

WHAT NOT TO DO

NEVER:
- Claim to be made by OpenAI, Google, Meta, etc.
- Say "as an AI language model"
- Invent facts
- Generate images
- Break character
- Ignore the user's language
- Sound robotic

---

</SYSTEM_PROMPT>"""

BANNER = f"""
╔═══════════════════════════════════════════════════╗
║           OpenSof - sofIA CLI                    ║
║         type 'exit' to stop                       ║
║         type 'clean' to reset!                    ║
║                                                   ║
║  Platform: {SYSTEM:27} ║
╚═══════════════════════════════════════════════════╝
"""

#colors

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Foreground
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    #background
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    
    @staticmethod
    def disable():
        if IS_WINDOWS:
            for attr in dir(Colors):
                if not attr.startswith('_'):
                    setattr(Colors, attr, '')
    
    @staticmethod
    def enable_windows():
        if IS_WINDOWS:
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                handle = kernel32.GetStdHandle(-11)
                mode = ctypes.c_ulong()
                kernel32.GetConsoleMode(handle, ctypes.byref(mode))
                mode.value |= 0x0004
                kernel32.SetConsoleMode(handle, mode)
            except:
                Colors.disable()

Colors.enable_windows()

#utils

def clear_screen():
    os.system('cls' if IS_WINDOWS else 'clear')

def get_api_key() -> str:
    
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if key:
        return key

    print(f"{Colors.YELLOW}Paste ur Groq key (groq.com/keys):{Colors.RESET}")
    key = input(f"  {Colors.BOLD}GROQ_API_KEY:{Colors.RESET} ").strip()
    
    if not key:
        print(f"{Colors.RED}✗ No key provided{Colors.RESET}")
        sys.exit(1)

    salvar = input(f"{Colors.YELLOW}Save on .env? (y/n):{Colors.RESET} ").strip().lower()
    if salvar == "y":
        env_path = Path(__file__).parent / ".env"
        with open(env_path, "a", encoding="utf-8") as f:
            f.write(f"\nGROQ_API_KEY={key}\n")
        print(f"{Colors.GREEN}✓ .env saved!{Colors.RESET}")

    return key

def format_response(text: str, max_width: int = 100) -> str:
    lines = text.split('\n')
    formatted = []
    for line in lines:
        if len(line) <= max_width:
            formatted.append(line)
        else:
            words = line.split(' ')
            current = []
            for word in words:
                if len(' '.join(current + [word])) > max_width:
                    formatted.append(' '.join(current))
                    current = [word]
                else:
                    current.append(word)
            if current:
                formatted.append(' '.join(current))
    return '\n'.join(formatted)

def strip_thinking_tags(text: str) -> str:
    import re
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

#chat

def stream_chat(api_key: str, messages: List[Dict]) -> str:
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
    in_thinking = False
    
    try:
        with requests.post(
            GROQ_API_URL, 
            headers=headers, 
            json=payload, 
            stream=True, 
            timeout=60
        ) as resp:
            if resp.status_code == 401:
                print(f"\n{Colors.RED}[✗ Error] Invalid API key!{Colors.RESET}")
                return ""
            if resp.status_code == 429:
                print(f"\n{Colors.RED}[✗ Error] Groq rate limit ://{Colors.RESET}")
                return ""
            
            resp.raise_for_status()

            print(f"\n{Colors.CYAN}sofIA:{Colors.RESET} ", end="", flush=True)

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
                        if "<think>" in content:
                            in_thinking = True
                        if "</think>" in content:
                            in_thinking = False
                            full_response += content
                            continue
                        if not in_thinking:
                            print(content, end="", flush=True)
                            full_response += content
                        else:
                            full_response += content
                except (json.JSONDecodeError, KeyError, IndexError):
                    pass

    except requests.exceptions.ConnectionError:
        print(f"\n{Colors.RED}[✗ Error] No internet connection{Colors.RESET}")
    except requests.exceptions.Timeout:
        print(f"\n{Colors.RED}[✗ Error] Request timeout!{Colors.RESET}")
    except requests.exceptions.RequestException as e:
        print(f"\n{Colors.RED}[✗ Error] {str(e)}{Colors.RESET}")

    print("\n")
    return strip_thinking_tags(full_response)

def interactive_mode(api_key: str):
    """Modo CLI interativo com histórico"""
    
    clear_screen()
    print(BANNER)
    
    history: List[Dict] = []
    
    print(f"{Colors.GREEN}Ready to chat, chefe! Type 'help' for commands.{Colors.RESET}\n")

    while True:
        try:
            user_input = input(f"{Colors.BOLD}{Colors.GREEN}você:{Colors.RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n{Colors.YELLOW}Goodbye 👋{Colors.RESET}")
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print(f"{Colors.YELLOW}Goodbye! 👋{Colors.RESET}")
            break

        if user_input.lower() == "clean":
            history.clear()
            print(f"{Colors.GREEN}[✓ Cleaned!]{Colors.RESET}\n")
            continue
        
        if user_input.lower() == "help":
            print(f"""
{Colors.CYAN}═══════════════════════════════════════{Colors.RESET}
{Colors.BOLD}Commands:{Colors.RESET}
  help    - Show this message
  clean   - Clear chat history
  exit    - Exit OpenSof
{Colors.CYAN}═══════════════════════════════════════{Colors.RESET}
""")
            continue
        
        if user_input.lower() == "history":
            if history:
                print(f"\n{Colors.BLUE}Chat History ({len(history)} messages):{Colors.RESET}")
                for i, msg in enumerate(history[-10:], 1):
                    role = f"{Colors.GREEN}User{Colors.RESET}" if msg["role"] == "user" else f"{Colors.CYAN}AI{Colors.RESET}"
                    preview = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
                    print(f"  {i}. {role}: {preview}")
            else:
                print(f"{Colors.YELLOW}No history yet{Colors.RESET}")
            print()
            continue

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages += history[-20:]
        messages.append({"role": "user", "content": user_input})

        response = stream_chat(api_key, messages)

        if response:
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response})

def non_interactive_mode(api_key: str, question: str):
    """Modo uma pergunta, uma resposta"""
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    response = stream_chat(api_key, messages)
    
    if response:
        return 0
    else:
        return 1

#main

def main():
    """Entrada principal"""
    
    api_key = get_api_key()
    
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        return non_interactive_mode(api_key, question)
    
    try:
        interactive_mode(api_key)
        return 0
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.RESET}")
        return 130
    except Exception as e:
        print(f"\n{Colors.RED}[✗ Error] {str(e)}{Colors.RESET}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
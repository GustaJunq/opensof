<p align="center">
  <img src="logo.png" width="200"/>
</p>

<h1 align="center">OpenSof</h1>

<p align="center">
  A CLI assistant powered by Groq — open source, lightweight, and direct.
</p>

<p align="center">
  <a href="https://sof-networks.vercel.app">SofIA</a> •
  <a href="https://github.com/GustaJunq">GitHub</a>
</p>

---

## About

**OpenSof** is a simplified, open-source version of [SofIA](https://sof-networks.vercel.app) — a personal AI assistant project.

> *SofIA* comes from the Greek **σοφία** (*Sophia*) — meaning **wisdom**.

OpenSof runs entirely in your terminal, powered by **Groq** and the **Qwen 3 32B** model.

---

## Features

- Streaming responses in real time
- Conversation history within the session
- `clean` command to reset the conversation
- Auto-saves your API key to `.env`
- Formal, direct persona — built for focus

---

## Requirements

- Python 3.8+
- A free [Groq API key](https://console.groq.com/keys)

---

## Installation

```bash
git clone https://github.com/GustaJunq/opensof.git
cd opensof
pip install -r requirements.txt
```

Create a `.env` file in the project folder:

```env
GROQ_API_KEY=your_key_here
```

Or just run the program — it will ask for your key on first launch.

---

## Usage

```bash
python opensof.py
```

| Command | Action |
|--------|--------|
| `exit` | Quit the program |
| `clean` | Reset conversation history |

---

## Project Structure

```
opensof/
├── opensof.py        # Main script
├── .env              # API key (not committed)
├── assets/
│   └── logo.png      # Project logo
└── README.md
```

---

## Requirements file

Create a `requirements.txt` with:

```
requests
python-dotenv
```

---

## Related

- [SofIA](https://sof-networks.vercel.app) — the original, full version of the assistant

---

## Author

Made by [@GustaJunq](https://github.com/GustaJunq)

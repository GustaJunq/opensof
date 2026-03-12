# Contributing to OpenSof

First off, thanks for taking the time to contribute! 🎉

OpenSof is a community-driven project, and we welcome contributions of all kinds.

## How to Contribute

### Reporting Bugs

Found a bug? Great! Here's how to report it:

1. **Check existing issues** — make sure it hasn't been reported yet
2. **Open a new issue** with:
   - A clear title
   - Description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Your OS, Python version, and environment

Example:
```
Title: OpenSof crashes when API key is invalid

Description: When I provide an invalid Groq API key, the program crashes instead of showing a friendly error message.

Steps to reproduce:
1. Run `python opensof.py`
2. Enter a fake API key
3. Try to ask a question

Expected: Error message saying "Invalid API key"
Actual: Program crashes with traceback

Environment:
- OS: Linux Ubuntu 22.04
- Python: 3.10
- OpenSof: Latest from main branch
```

### Suggesting Features

Have an idea? We'd love to hear it!

1. **Check existing issues** — maybe someone already suggested it
2. **Open a new issue** with:
   - Clear title describing the feature
   - Why you think it would be useful
   - How it should work (optional mockup/example)

Example:
```
Title: Add support for conversation history export

Description: It would be cool to export chat history as JSON or markdown for backup or sharing.

Use case: I want to save important conversations locally.
```

### Submitting Code Changes

Ready to code? Follow these steps:

#### 1. Fork the Repository
Click the "Fork" button on GitHub to create your own copy.

#### 2. Clone Your Fork
```bash
git clone https://github.com/YOUR_USERNAME/opensof.git
cd opensof
```

#### 3. Create a Branch
Use a descriptive name:
```bash
git checkout -b fix/api-key-validation
# or
git checkout -b feature/conversation-export
```

Branch naming:
- `fix/` — for bug fixes
- `feature/` — for new features
- `docs/` — for documentation
- `refactor/` — for code cleanup

#### 4. Make Your Changes
- Keep commits **atomic** (one change per commit)
- Write **clear commit messages**

Good commit message:
```
Fix: Handle invalid API key gracefully

- Check API key format before sending request
- Show user-friendly error message
- Add test for invalid key scenario
```

Bad commit message:
```
fixed stuff
```

#### 5. Test Your Changes
```bash
python opensof.py "test question"
python opensof.py
```

Make sure:
- No crashes
- Error messages are clear
- Interactive mode still works
- Non-interactive mode still works

#### 6. Push to Your Fork
```bash
git push origin fix/api-key-validation
```

#### 7. Open a Pull Request
Go to the original repo and click "New Pull Request". Include:
- Title: What does this change do?
- Description: Why is this change needed?
- Related issues: `Fixes #123` (if applicable)

Example PR description:
```
## Description
This PR improves error handling when an invalid API key is provided.

## Changes
- Added API key validation before making requests
- Shows user-friendly error message instead of traceback
- Added test case for invalid keys

## Fixes
Fixes #45

## Testing
Tested with:
- Valid API key ✓
- Invalid API key ✓
- Empty API key ✓
```

---

## Code Style Guidelines

Keep it consistent with the existing codebase:

### Python Style
- Follow PEP 8 (sort of)
- Use clear variable names
- Add comments for complex logic
- Keep functions focused and small

### Naming
```python
# Good
def strip_thinking_tags(text: str) -> str:
    """Remove <think> tags from response."""
    pass

# Avoid
def st(t):
    pass
```

### Comments
```python
# Good - explains WHY
# Remove thinking tags before showing to user
# because the Qwen3 model includes them for reasoning

# Avoid - explains WHAT (code already does that)
# Split the text by newline
lines = text.split('\n')
```

---

## Testing

If you're adding a feature or fixing a bug, consider adding a test:

```python
# Example simple test
def test_strip_thinking_tags():
    text = "Hello <think>reasoning</think> world"
    result = strip_thinking_tags(text)
    assert result == "Hello  world"
```

---

## Documentation

- Update `README.md` if you add features or change usage
- Keep comments clear and concise
- Document any new environment variables

---

## Community Guidelines

Please be respectful and constructive:

- ✅ **Do**: Be helpful, patient, and kind
- ❌ **Don't**: Be rude, dismissive, or disrespectful
- ✅ **Do**: Ask questions if you're unsure
- ❌ **Don't**: Spam or self-promote

---

## Questions?

- Check existing issues and discussions
- Open an issue with the `question` label
- Be specific and provide context

---

## Thank You!

Contributing makes OpenSof better for everyone. Thanks for being part of the community! 🚀

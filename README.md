# Screenshot Agent for Claude Code

A custom Claude Code agent that takes screenshots of web pages and local HTML files using Playwright.

## Install

### 1. Clone or download

```bash
git clone https://github.com/alexdobrenko/screenshot-agent.git
cd screenshot-agent
```

### 2. Copy both files

```bash
# Agent definition (Claude Code reads this)
cp screenshot.md ~/.claude/agents/screenshot.md

# Screenshot script (put it next to the agent file so it's easy to find)
cp screenshot.py ~/.claude/agents/screenshot.py
```

### 3. Install dependencies

```bash
pip install playwright Pillow
python -m playwright install chromium
```

### 4. Restart Claude Code

The screenshot agent will be available in your next session. Try: "take a screenshot of https://example.com"

## Usage

Once installed, Claude Code can spawn the screenshot agent:

```
"Take a screenshot of https://example.com"
"Capture the homepage and check if the deploy looks right"
"Generate a blog header from this page"
```

Or use the script directly:

```bash
# Basic screenshot
python screenshot.py https://example.com -o output.png

# Retina quality (2x resolution)
python screenshot.py https://example.com --retina -o output.png

# Full page capture
python screenshot.py https://example.com --full -o output.png

# Local HTML file
python screenshot.py /path/to/file.html -o output.png

# Blog header (crop and resize)
python screenshot.py https://example.com --header 2400 1260 -o header.png

# Mobile viewport
python screenshot.py https://example.com -w 390 --height 844 -o mobile.png
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `-o` | screenshot.png | Output file path |
| `-w` | 1280 | Viewport width |
| `--height` | 800 | Viewport height |
| `--full` | off | Capture full page |
| `--retina` | off | 2x device scale factor |
| `--wait` | 2 | Seconds to wait after page load |
| `--header W H` | off | Crop from top and resize to WxH |
| `--dark` | off | Dark color scheme preference |

## How it works

The agent definition (`screenshot.md`) tells Claude Code when and how to use the screenshot tool. The Python script (`screenshot.py`) uses Playwright with headless Chromium to capture pages. The `--header` option uses Pillow to crop and resize for blog headers.

Built with [Claude Code](https://claude.ai/claude-code).

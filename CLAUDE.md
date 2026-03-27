# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MDView is a macOS desktop Markdown viewer application built with Python (pywebview) and vanilla HTML/CSS/JS.

## Setup

```bash
pip3 install pywebview py2app
```

## Commands

```bash
# Run locally for development
python3 app.py

# Enable WebKit inspector during development (change in app.py)
webview.start(debug=True)

# Package as macOS .app
python3 setup.py py2app

# Install to Applications
cp -r dist/MDViewer.app /Applications/

# Clear Gatekeeper restrictions (first run)
xattr -cr /Applications/MDViewer.app
```

## Architecture

**Backend (`app.py`):** Python pywebview creates a native macOS window with an embedded WebKit browser. Exposes two API methods via `window.expose()`:
- `read_file(path)` - Returns JSON `{content, filename}` or `{error}`
- `open_file_dialog()` - Opens native file picker, returns same shape or `{cancelled: true}`

When opened via file association (`sys.argv[1]`), `app.py` calls `window.evaluate_js('loadMarkdownData(...)')` in the `window.events.loaded` callback to push the file content into the frontend.

**Frontend (`viewer.html`):** Single-file UI. All JS libraries are loaded from CDN (requires internet in dev mode):
- marked.js — Markdown parsing
- highlight.js — code syntax highlighting with language auto-detection and copy button
- Mantine design tokens (CSS variables) for theming — three-way toggle: system auto / light / dark via `[data-theme]` attribute on `<html>`
- Auto-generated TOC from headings with scroll sync
- Drag-and-drop and toolbar button file loading
- HTML export of current document

**IPC Flow:**
- JS → Python: `window.pywebview.api.read_file(path)` / `open_file_dialog()`
- Python → JS (file association only): `window.evaluate_js('loadMarkdownData(data)')`

## File Association

Registered in `setup.py` plist for `.md` / `.markdown` via `argv_emulation: True`. After installing, set as default app via Finder → Get Info → Open With → Change All.

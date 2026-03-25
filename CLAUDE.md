# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MDView is a macOS desktop Markdown viewer application built with Python (pywebview) and vanilla HTML/CSS/JS.

## Commands

```bash
# Run locally for development
python3 app.py

# Package as macOS .app
python3 setup.py py2app

# Install to Applications
cp -r dist/MDView.app /Applications/

# Clear Gatekeeper restrictions (first run)
xattr -cr /Applications/MDView.app
```

## Architecture

**Backend (`app.py`):** Python pywebview creates a native macOS window with an embedded WebKit browser. Exposes two API methods to JavaScript:
- `read_file(path)` - Returns JSON with file content and filename
- `open_file_dialog()` - Opens native file picker, returns file content

**Frontend (`viewer.html`):** Single-file UI with:
- marked.js for Markdown parsing
- highlight.js for code syntax highlighting
- Mantine design tokens for theming (light/dark)
- Auto-generated TOC from headings with scroll sync
- Drag-and-drop file loading

**IPC Flow:** JavaScript calls Python via `window.pywebview.api.*`, Python returns JSON data.

## Dependencies

- `pywebview` - Native window with WebKit
- `py2app` - macOS app bundling

## File Association

The app registers as a handler for `.md` and `.markdown` files. When opened via double-click, the file path is passed as `sys.argv[1]`.

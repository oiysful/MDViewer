# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MDViewer is a macOS desktop Markdown viewer application built with Python (pywebview) and vanilla HTML/CSS/JS.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install pywebview py2app
```

> The project uses a local `venv`. Always use `venv/bin/python3` or activate the venv before running build commands. System Python is externally managed (Homebrew) and cannot install packages directly.

## Commands

```bash
# Run locally for development
python3 app.py

# Enable WebKit inspector during development (change in app.py)
webview.start(debug=True)

# Package as macOS .app (use venv python)
venv/bin/python3 setup.py py2app

# Install to Applications
cp -r dist/MDViewer.app /Applications/
xattr -cr /Applications/MDViewer.app
```

## Architecture

### Backend (`app.py`)

`create_window(path=None)` is the central factory — it creates an NSWindow via pywebview, registers the API, and wires `on_loaded` / `on_closed` events. All windows are tracked in `_win_states` (a `{win: {'loaded': Event, 'has_file': bool}}` dict protected by `_win_lock`).

**Exposed API methods** (called from JS via `window.pywebview.api.*`):
- `read_file(path)` → `{content, filename, path}` or `{error}`
- `open_file_dialog()` → opens native picker (`allow_multiple=True`); first file returns to current window, extras open new windows via threads
- `open_folder_dialog()` → `{path}` or `{cancelled: true}`
- `list_directory(path)` → `{path, entries: [{type, name, path}]}` — dirs first, then `.md`/`.markdown` files
- `new_window(path)` → spawns a thread to call `create_window(path)`

**Multi-window helpers:**
- `_open_in_idle_or_new(path)` — loads into the first file-less window (waiting for `state['loaded']` event), or creates a new window. Used by the Finder file-open handler.

**Finder file-open (`_patch_app_delegate`):**
`argv_emulation` is disabled. Instead, `webview.start(func=_patch_app_delegate)` runs a background thread that waits for pywebview's app delegate to be set, then injects `application:openFile:` and `application:openFiles:` into the delegate class using PyObjC. This ensures `NSDocumentController` receives `YES` and suppresses the "cannot open files" error toast. Must be patched after the delegate exists but before the first `odoc` Apple Event is processed.

### Frontend (`viewer.html`)

Single-file UI. All JS libraries are CDN-hosted (requires internet in dev mode):
- **marked.js** — Markdown parsing
- **highlight.js** — syntax highlighting with language auto-detection and copy button
- **Mantine design tokens** (CSS variables) — three-way theme toggle: system auto / light / dark via `[data-theme]` on `<html>`

**Layout:** `[#sidebar (240px, collapsible)] [#scroll-area (flex:1)]`

The sidebar has two tabs (toggled by `switchTab()`):
- **목차 (TOC)** — auto-generated from headings, scroll-synced active state
- **탐색기 (Explorer)** — lazy-loaded directory tree; click loads file, `⌘`+click opens new window

**Key JS functions:**
- `loadMarkdownData(data)` — entry point called from Python via `evaluate_js` on file-association open
- `load(data)` — renders markdown, updates TOC, stats, title
- `openFolder()` / `loadDir(path, container, depth)` — explorer tree, lazy per-directory
- `switchTab(tab)` — switches sidebar panel, auto-opens sidebar if closed
- `newWindow()` — calls `api.new_window(null)`

### IPC Flow

- JS → Python: `window.pywebview.api.<method>()`  — pywebview runs these on a background thread
- Python → JS: `win.evaluate_js('loadMarkdownData(...)')` — used for file-association opens and idle-window file loading; always called from a non-main thread to avoid deadlocks

### File Association

Registered in `setup.py` plist for `.md` / `.markdown` (`LSHandlerRank: Alternate`). `argv_emulation: False` — file opens are handled entirely via the PyObjC delegate patch. After installing, set as default via Finder → Get Info → Open With → Change All.

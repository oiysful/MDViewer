#!/usr/bin/env python3
import webview
import sys
import os
import json
import threading
import time

VIEWER_HTML = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viewer.html')

# Per-window state: {win: {'loaded': Event, 'has_file': bool}}
_win_states: dict = {}
_win_lock = threading.Lock()


# ── Window factory ─────────────────────────────────────────────────────────────

def create_window(path=None):
    win = webview.create_window(
        'MDViewer', VIEWER_HTML,
        width=1100, height=800,
        min_size=(600, 400),
        background_color='#0f1117',
    )
    state = {'loaded': threading.Event(), 'has_file': bool(path)}
    with _win_lock:
        _win_states[win] = state

    api = Api(win)
    win.expose(api.read_file)
    win.expose(api.open_file_dialog)
    win.expose(api.open_folder_dialog)
    win.expose(api.list_directory)
    win.expose(api.new_window)

    def on_loaded():
        state['loaded'].set()
        if path:
            data = api.read_file(path)
            win.evaluate_js(f'loadMarkdownData({data})')

    def on_closed():
        with _win_lock:
            _win_states.pop(win, None)

    win.events.loaded += on_loaded
    win.events.closed += on_closed
    return win


def _open_in_idle_or_new(path):
    """Load path into an idle (file-less) window, or open a new one.
    Safe to call from any thread."""
    idle = None
    with _win_lock:
        for win, st in _win_states.items():
            if not st['has_file']:
                st['has_file'] = True
                idle = win
                break

    if idle:
        def _load():
            with _win_lock:
                st = _win_states.get(idle)
            if st:
                st['loaded'].wait(timeout=15)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                data = json.dumps({
                    'content': content,
                    'filename': os.path.basename(path),
                    'path': path,
                })
                idle.evaluate_js(f'loadMarkdownData({data})')
            except Exception as e:
                print(f'[MDViewer] load error: {e}', flush=True)
        threading.Thread(target=_load, daemon=True).start()
    else:
        threading.Thread(target=create_window, args=(path,), daemon=True).start()


# ── JS-exposed API ──────────────────────────────────────────────────────────────

class Api:
    def __init__(self, window):
        self.window = window

    def read_file(self, path):
        with _win_lock:
            st = _win_states.get(self.window)
            if st:
                st['has_file'] = True
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.dumps({
                    'content': f.read(),
                    'filename': os.path.basename(path),
                    'path': path,
                })
        except Exception as e:
            return json.dumps({'error': str(e)})

    def open_file_dialog(self):
        result = self.window.create_file_dialog(
            webview.FileDialog.OPEN,
            allow_multiple=True,
            file_types=('Markdown Files (*.md;*.markdown)', 'All Files (*.*)')
        )
        if not result:
            return json.dumps({'cancelled': True})
        for p in result[1:]:
            threading.Thread(target=create_window, args=(p,), daemon=True).start()
        return self.read_file(result[0])

    def open_folder_dialog(self):
        result = self.window.create_file_dialog(webview.FileDialog.FOLDER)
        if result:
            return json.dumps({'path': result[0]})
        return json.dumps({'cancelled': True})

    def list_directory(self, path):
        try:
            names = sorted(
                os.listdir(path),
                key=lambda n: (not os.path.isdir(os.path.join(path, n)), n.lower())
            )
            entries = []
            for name in names:
                full = os.path.join(path, name)
                if os.path.isdir(full):
                    entries.append({'type': 'dir', 'name': name, 'path': full})
                elif name.lower().endswith(('.md', '.markdown')):
                    entries.append({'type': 'file', 'name': name, 'path': full})
            return json.dumps({'path': path, 'entries': entries})
        except Exception as e:
            return json.dumps({'error': str(e)})

    def new_window(self, path=None):
        threading.Thread(
            target=create_window,
            args=(path if path else None,),
            daemon=True,
        ).start()


# ── macOS file-open handler ─────────────────────────────────────────────────────

def _patch_app_delegate():
    """Inject application:openFile: into pywebview's app delegate class.

    NSDocumentController handles the 'odoc' Apple Event and always calls
    application:openFile: on the delegate. If that method returns NO (or is
    missing), macOS shows the "cannot open files in the X format" toast.
    Patching the delegate to return YES suppresses the error and lets us open
    the file ourselves.

    Called from webview.start(func=...) — runs in a background thread while
    the main run loop is starting up.
    """
    try:
        from AppKit import NSApplication
        import objc

        # Wait until pywebview has set the app delegate (normally < 100 ms)
        app = NSApplication.sharedApplication()
        delegate = None
        for _ in range(500):          # up to 5 s
            d = app.delegate()
            if d is not None:
                delegate = d
                break
            time.sleep(0.01)

        if delegate is None:
            print('[MDViewer] app delegate not found — file-open patch skipped', flush=True)
            return

        cls = type(delegate)
        if getattr(cls, '_mdviewer_patched', False):
            return

        # ── application:openFile: ──────────────────────────────────────────────
        # Called by NSDocumentController for every file Finder wants to open.
        # Returning YES tells macOS "I handled it" — no error toast.
        def application_openFile_(self, application, filename):
            path = str(filename)
            if os.path.isfile(path):
                threading.Thread(
                    target=_open_in_idle_or_new, args=(path,), daemon=True
                ).start()
            return True     # always YES to suppress the error dialog

        # ── application:openFiles: ─────────────────────────────────────────────
        # Batch variant — some versions of macOS use this instead.
        def application_openFiles_(self, application, filenames):
            for f in filenames:
                path = str(f)
                if os.path.isfile(path):
                    threading.Thread(
                        target=_open_in_idle_or_new, args=(path,), daemon=True
                    ).start()
            application.replyToOpenOrPrint_(0)   # NSApplicationDelegateReplySuccess

        cls.application_openFile_ = objc.selector(
            application_openFile_, signature=b'B@:@@'
        )
        cls.application_openFiles_ = objc.selector(
            application_openFiles_, signature=b'v@:@@'
        )
        cls._mdviewer_patched = True

    except Exception as e:
        print(f'[MDViewer] delegate patch failed: {e}', flush=True)


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    # Handle command-line invocation (terminal / launchd / script)
    initial_file = None
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        initial_file = sys.argv[1]

    create_window(initial_file)

    # func runs in a background thread right after the run loop starts.
    # It patches the delegate before NSDocumentController delivers the first
    # queued 'odoc' Apple Event, so Finder double-clicks work correctly.
    webview.start(func=_patch_app_delegate, debug=False)


if __name__ == '__main__':
    main()

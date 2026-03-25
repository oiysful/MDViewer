#!/usr/bin/env python3
import webview
import sys
import os
import json

# HTML 뷰어 파일 경로
VIEWER_HTML = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viewer.html')

class Api:
    def __init__(self, window):
        self.window = window

    def read_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.dumps({'content': f.read(), 'filename': os.path.basename(path)})
        except Exception as e:
            return json.dumps({'error': str(e)})

    def open_file_dialog(self):
        result = self.window.create_file_dialog(
            webview.OPEN_DIALOG,
            allow_multiple=False,
            file_types=('Markdown Files (*.md *.markdown)', 'All Files (*.*)')
        )
        if result:
            return self.read_file(result[0])
        return json.dumps({'cancelled': True})


def main():
    initial_file = None

    # 커맨드라인 인수로 파일 경로가 전달된 경우 (기본 앱으로 열기)
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.isfile(path):
            initial_file = path

    window = webview.create_window(
        'MDViewer',
        VIEWER_HTML,
        width=1100,
        height=800,
        min_size=(600, 400),
        background_color='#0f1117',
    )

    api = Api(window)
    window.expose(api.read_file)
    window.expose(api.open_file_dialog)

    def on_loaded():
        if initial_file:
            data = api.read_file(initial_file)
            window.evaluate_js(f'loadMarkdownData({data})')

    window.events.loaded += on_loaded

    webview.start(debug=False)


if __name__ == '__main__':
    main()

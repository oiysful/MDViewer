"""
py2app 설정 파일 — MarkdownViewer.app 패키징용
사용법: python setup.py py2app
"""
from setuptools import setup

APP = ['app.py']
DATA_FILES = [('', ['viewer.html'])]

OPTIONS = {
    'argv_emulation': True,          # 파일 더블클릭으로 열기 지원
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName': 'MDViewer',
        'CFBundleDisplayName': 'MDViewer',
        'CFBundleIdentifier': 'com.mdviewr.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0',
        # .md / .markdown 파일을 이 앱으로 열 수 있도록 등록
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'Markdown Document',
                'CFBundleTypeRole': 'Viewer',
                'LSHandlerRank': 'Alternate',
                'CFBundleTypeExtensions': ['md', 'markdown'],
                'LSItemContentTypes': ['net.daringfireball.markdown'],
            }
        ],
        'NSHumanReadableCopyright': '© 2024 MDView',
        'NSHighResolutionCapable': True,
    },
    'packages': ['webview'],
    'includes': ['webview'],
}

setup(
    app=APP,
    name='MDViewer',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

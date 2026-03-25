# MDViewer

macOS용 Markdown 뷰어 앱. Python(pywebview) + 단일 HTML 파일로 구성.

## 파일 구성

```
MarkdownViewer/
├── app.py          — 메인 Python 앱 (pywebview 백엔드)
├── viewer.html     — 뷰어 UI (HTML/CSS/JS)
├── setup.py        — macOS .app 패키징 설정
├── icon.icns       — 앱 아이콘
└── Vector.svg      — 테마 토글 아이콘 소스
```

## 설치 및 실행

### 요구사항

- macOS
- Python 3.9+

### 1. 의존성 설치

```bash
pip3 install pywebview py2app
```

### 2. 개발 모드로 실행

```bash
python3 app.py
```

### 3. macOS .app으로 패키징

```bash
python3 setup.py py2app
```

빌드 완료 후 `dist/MDViewer.app` 생성.

### 4. 앱 설치

```bash
cp -r dist/MDViewer.app /Applications/
```

처음 실행 시 Gatekeeper 경고가 뜨면:

```bash
xattr -cr /Applications/MDViewer.app
```

또는 앱 우클릭 → **열기** 선택.

## 기능

| 기능 | 설명 |
|------|------|
| 파일 열기 | 툴바 버튼 또는 드래그 앤 드롭 |
| 더블클릭으로 열기 | Finder에서 .md 파일 기본 앱으로 등록 가능 |
| 테마 | 시스템 자동 / 라이트 / 다크 3단계 전환 |
| TOC | 헤딩에서 자동 생성, 스크롤 동기화 |
| 코드 하이라이팅 | 언어 자동 감지 + 복사 버튼 |
| HTML 내보내기 | 현재 문서를 독립 HTML 파일로 저장 |
| 단어/읽기 시간 | 상태바 표시 |

## .md 파일 기본 앱 설정

1. Finder에서 `.md` 파일 우클릭 → **정보 가져오기** (`⌘I`)
2. **다음으로 열기** 항목에서 `MDViewer` 선택
3. **모두 변경** 클릭

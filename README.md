# MDViewer

macOS용 Markdown 뷰어 앱. Python(pywebview) + 단일 HTML 파일로 구성.

## 파일 구성

```
MDViewer/
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

### 1. 가상환경 및 의존성 설치

```bash
python3 -m venv venv
source venv/bin/activate
pip install pywebview py2app
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
| 파일 열기 | 툴바 버튼, 드래그 앤 드롭, Finder 더블클릭 |
| 멀티 창 | 새 창 버튼으로 독립 창 추가, 파일 여러 개 선택 시 각각 별도 창 |
| 디렉토리 탐색기 | 폴더 열기 후 좌측 탐색기 탭에서 .md 파일 트리 탐색 |
| 테마 | 시스템 자동 / 라이트 / 다크 3단계 전환 |
| TOC | 헤딩에서 자동 생성, 스크롤 동기화 |
| 코드 하이라이팅 | 언어 자동 감지 + 복사 버튼 |
| HTML 내보내기 | 현재 문서를 독립 HTML 파일로 저장 |
| 단어/읽기 시간 | 상태바 표시 |

## 단축키

| 단축키 | 동작 |
|--------|------|
| `⌘O` | 파일 열기 |
| `⌘N` | 새 창 |
| `⌘P` | 인쇄 |

탐색기에서 파일 클릭 시 현재 창에 로드, `⌘`+클릭 시 새 창으로 열기.

## .md 파일 기본 앱 설정

1. Finder에서 `.md` 파일 우클릭 → **정보 가져오기** (`⌘I`)
2. **다음으로 열기** 항목에서 `MDViewer` 선택
3. **모두 변경** 클릭

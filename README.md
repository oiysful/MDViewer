# MDView 설치 가이드

## 📁 파일 구성
```
MarkdownViewer/
├── app.py          ← 메인 Python 앱
├── viewer.html     ← 뷰어 UI
├── setup.py        ← .app 패키징 설정
└── README.md       ← 이 파일
```

---

## 🚀 설치 방법

### 1단계 — 의존성 설치

터미널에서 아래 명령어를 실행하세요:

```bash
pip3 install pywebview py2app
```

### 2단계 — 테스트 실행 (앱 패키징 전 확인)

```bash
cd MarkdownViewer
python3 app.py
```

정상적으로 창이 열리면 계속 진행합니다.

### 3단계 — .app 패키징

```bash
python3 setup.py py2app
```

완료되면 `dist/MDView.app` 파일이 생성됩니다.

### 4단계 — 응용 프로그램 폴더로 이동

```bash
cp -r dist/MDView.app /Applications/
```

---

## 🔧 .md 파일 기본 앱으로 설정하기

1. Finder에서 아무 `.md` 파일을 **우클릭**
2. **"정보 가져오기"** 선택 (`⌘ + I`)
3. **"다음으로 열기"** 섹션에서 `MDView` 선택
4. **"모두 변경..."** 클릭
5. 이제 모든 `.md` 파일이 MDView로 열립니다 ✅

---

## ⚠️ Gatekeeper 경고 해결

처음 실행 시 "확인되지 않은 개발자" 경고가 뜰 수 있습니다:

```bash
xattr -cr /Applications/MDView.app
```

또는: 앱 우클릭 → **"열기"** 선택

---

## 💡 사용법

| 방법 | 설명 |
|------|------|
| 파일 열기 버튼 | 툴바에서 파일 선택 |
| 드래그 앤 드롭 | 창에 .md 파일을 드래그 |
| 더블클릭 | 기본 앱 설정 후 파일 더블클릭 |

---

## 기능 목록

- ✅ GitHub 스타일 Markdown 렌더링
- ✅ 코드 블록 신택스 하이라이팅 + 복사 버튼
- ✅ 자동 목차(TOC) 생성
- ✅ 다크 / 라이트 테마 전환
- ✅ HTML로 내보내기
- ✅ 드래그 앤 드롭
- ✅ 단어 수 / 읽기 시간 표시
- ✅ .md 파일 기본 앱으로 설정 가능

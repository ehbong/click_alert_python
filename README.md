새로운 README.md 파일을 생성하겠습니다:

```markdown:README.md
# Key Reminder (키 알리미)

Key Reminder는 특정 키가 입력된 후 지정된 시간이 지나면 알림음을 재생하는 Windows 프로그램입니다.
키를 주기적으로 입력하는 것을 잊지 않도록 도와줍니다.

## 주요 기능

- 모니터링할 키 설정
- 알림 시간 설정 (초 단위)
- 백그라운드에서 키 입력 감지
- 설정된 시간 후 알림음 재생
- 프로그램 재시작 시 이전 설정 자동 로드

## 사용 방법

1. 프로그램 실행
2. "키 입력 받기" 버튼을 클릭하여 모니터링할 키 설정
3. "알림 시간 설정" 란에 알림이 울릴 시간을 초 단위로 입력
4. "설정 저장" 버튼을 클릭하여 설정 저장 및 모니터링 시작
5. 이제 설정된 키를 입력하면 지정된 시간 후에 알림음이 재생됩니다

## 개발 환경 설정

### 필수 요구사항
- Python 3.x
- pip (Python 패키지 관리자)

### 필요한 라이브러리 설치
```bash
pip install keyboard
```

## EXE 파일 빌드 방법

1. PyInstaller 설치:
```bash
pip install pyinstaller
```

2. EXE 파일 생성:
```bash
# 콘솔 창 없는 버전 (권장)
pyinstaller --onefile --noconsole key_reminder.py

# 또는 콘솔 창 있는 버전
pyinstaller --onefile key_reminder.py
```

3. 생성된 EXE 파일은 `dist` 폴더에서 찾을 수 있습니다.

### 추가 빌드 옵션

- 아이콘 추가:
```bash
pyinstaller --onefile --noconsole --icon=your_icon.ico key_reminder.py
```

- 더 작은 파일 크기로 빌드:
```bash
pyinstaller --onefile --noconsole --strip --noupx key_reminder.py
```

## 주의사항

- 프로그램이 키보드 입력을 감지하기 위해 관리자 권한이 필요할 수 있습니다.
- Windows Defender나 다른 안티바이러스 프로그램에서 경고가 발생할 수 있습니다.
- 설정은 `key_reminder_config.json` 파일에 저장됩니다.

## 문제 해결

1. 키 입력이 감지되지 않는 경우:
   - 프로그램을 관리자 권한으로 실행해보세요.
   - 상태 표시가 "모니터링 중..."인지 확인하세요.

2. 알림음이 들리지 않는 경우:
   - Windows 사운드 설정을 확인하세요.
   - 다른 프로그램에서 소리가 정상적으로 재생되는지 확인하세요.

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.
```

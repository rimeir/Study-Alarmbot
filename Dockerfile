# 1. 베이스 이미지 선택
FROM python:3.9-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 시스템 업데이트 및 필수 도구 설치
RUN apt-get update && apt-get install -y \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. 애플리케이션 코드 복사
COPY . .

# 5. Python 패키지 설치
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 6. 실행 파일 권한 설정
RUN chmod +x alarmbot.py

# 7. 기본 실행 명령
CMD ["python3", "alarmbot.py"]

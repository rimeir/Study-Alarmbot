FROM python:3.9-slim

WORKDIR /app

# 시스템 업데이트 및 필수 도구 설치
RUN apt-get update && apt-get install -y \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 애플리케이션 코드 복사
COPY . .

# 필요한 소프트웨어 설치
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 실행 파일 권한 설정
RUN chmod +x alarmbot.py

CMD ["python3", "alarmbot.py"]

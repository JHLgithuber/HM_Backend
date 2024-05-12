# Python 공식 이미지를 기반으로 설정
FROM python:3.8-slim

# 작업 디렉터리 설정
WORKDIR /app

# 의존성 파일들을 컨테이너에 복사
COPY myenv_of_HM/Scripts/requirements.txt requirements.txt

# 의존성 설치
RUN pip install -r requirements.txt

# 현재 디렉터리의 내용을 컨테이너의 작업 디렉터리로 복사
COPY . .

# 컨테이너 실행 시 시작할 명령어 설정
CMD ["python", "run.py"]

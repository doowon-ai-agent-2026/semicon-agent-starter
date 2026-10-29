# Day 1 실습 명령 모음

## 4교시 · 내 PC (PowerShell)
```powershell
git clone https://github.com/doowon-ai-agent-2026/team01.git
cd team01
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py          # 브라우저 확인 후 Ctrl+C

git checkout -b feature/내이름-intro
# members/_template.md 를 복사해 members/내이름.md 작성
git add members/내이름.md
git commit -m "docs: 내이름 소개 추가"
git push -u origin feature/내이름-intro
```

## 6교시 · 내 PC (Docker Desktop 실행 후)
```powershell
docker build -t team-app .
docker run -d -p 8501:8501 --name app team-app
docker ps -a                  # 종료된 컨테이너까지
docker logs app               # 실행 로그 · 오류
docker stop app               # 끄기 → 다시 켜기: docker start app
docker rm -f app              # 지우고 새로 만들 때
```

## 7·8교시 · EC2 서버 (Bash)
```bash
bash scripts/install_docker.sh && newgrp docker
git clone https://github.com/doowon-ai-agent-2026/team01.git
cd team01
docker build -t team-app .
docker run -d -p 8501:8501 \
  --restart unless-stopped --name app team-app
docker ps -a
# 브라우저: http://퍼블릭IP:8501
```

## 8교시 · 팀명으로 바꿔 재배포
1. 내 PC에서 `config.py`의 `TEAM_NAME` 수정 → commit → push
2. 서버에서:
```bash
git pull
docker build -t team-app .
docker rm -f app
docker run -d -p 8501:8501 \
  --restart unless-stopped --name app team-app
```

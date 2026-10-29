# semicon-agent-starter

두원공과대학교 첨단산업 인재양성 부트캠프 「클라우드 기반 AI Agent 실무 프로젝트 과정」(2026 동계) 스타터 템플릿입니다.
반도체 공정 센서 데이터를 질문으로 분석하는 웹 서비스의 뼈대이며, **Day 1에는 API 키 없이 실행**됩니다.

## 팀 저장소 만들기
1. 오른쪽 위 **Use this template** → **Create a new repository**
2. Owner: `doowon-ai-agent-2026`, Repository name: `team01` ~ `team05`, **Public**
3. Settings → Collaborators에서 팀원과 강사 초대

## 바로 실행
```bash
python -m venv .venv
.venv\Scripts\activate          # macOS·Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
브라우저에서 http://localhost:8501 이 열립니다. 질문 예: "어떤 센서가 불량과 관련 있어?"

## 폴더 구조
| 경로 | 하는 일 | 주로 고치는 날 |
|---|---|---|
| `app.py` | 웹 화면 (Streamlit) | Day 4 |
| `config.py` | 팀명·서비스 제목 | Day 1 (재배포 실습) |
| `agent/loop.py` | 에이전트 루프: 질문 → 도구 선택 → 실행 → 답변 | Day 2 ~ 4 |
| `tools/data_tools.py` | 에이전트가 쓰는 도구 함수 | Day 2 ~ 5 |
| `data/` | 데이터 (`sample_sensor.csv`: 교육용 합성 데이터) | Day 2 |
| `practice/` | 3교시 AI 코딩 도구 실습 | Day 1 |
| `members/` | 4교시 첫 Pull Request 실습 | Day 1 |
| `Dockerfile`, `requirements.txt` | 실행 환경·패키지 목록 | Day 1 · 5 |
| `scripts/install_docker.sh` | EC2 Docker 설치 | Day 1 |
| `docs/DAY1.md` | Day 1 명령 모음 | Day 1 |

## 비밀값 관리
- API 키는 `.env`에만 둡니다(Day 2부터). `.env.example`을 복사해 만드세요.
- `.gitignore`가 Git에서, `.dockerignore`가 Docker 이미지에서 `.env`와 `*.pem`을 제외합니다.

## Docker · 배포
명령은 [docs/DAY1.md](docs/DAY1.md)를 보세요. 처음 실행과 재배포에 같은 `docker run` 명령을 씁니다.

## 데이터 안내
`data/sample_sensor.csv`와 `practice/sample.csv`는 실습용으로 만든 **합성 데이터**이며 실제 공정 데이터가 아닙니다.
프로젝트용 공개 데이터(UCI SECOM, WM-811K, AI4I 2020 등)는 원본이 크므로 저장소에 올리지 않고, 전처리한 작은 샘플만 `data/`에 둡니다(GitHub 파일 한도 100MB).

## 운영 안내
교육 기간에는 AWS에 배포해 시연하고, **수료 후 서버와 API 키는 종료**합니다. 포트폴리오는 이 저장소의 README·코드·시연영상으로 남깁니다.

"""웹 화면 (Streamlit). 실행: streamlit run app.py"""
import streamlit as st

from agent.loop import run_agent
from config import SERVICE_TITLE, TEAM_NAME
from tools.data_tools import get_summary, load_data

st.set_page_config(page_title=f"{TEAM_NAME} | {SERVICE_TITLE}", layout="wide")
st.title(f"[{TEAM_NAME}] {SERVICE_TITLE}")
st.caption(f"팀: {TEAM_NAME}  ·  Day 1 스타터 (API 키 없이 동작하는 규칙 기반 도우미)")

with st.sidebar:
    st.subheader("데이터 요약")
    s = get_summary()
    st.metric("전체 샘플", s["rows"])
    st.metric("불량", s["fail"])
    st.metric("결측값", s["missing_values"])
    st.caption("data/sample_sensor.csv · 교육용 합성 데이터")
    st.subheader("질문 예시")
    st.markdown("- 데이터 요약해 줘\n- 온도 정상과 불량 비교\n- 어떤 센서가 불량과 관련 있어?\n- 진동 추이 그래프")

if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("공정 데이터에 대해 물어보세요")
if question:
    st.session_state.history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    out = run_agent(question)
    with st.chat_message("assistant"):
        st.write(out["answer"])
        if "chart" in out["result"]:
            st.line_chart(out["result"]["chart"])
        with st.expander("에이전트가 한 일 (도구 호출 기록)"):
            for item in out["log"]:
                st.write(f"**{item['step']}** · {item['detail']}")
    st.session_state.history.append({"role": "assistant", "content": out["answer"]})

with st.expander("원본 데이터 미리 보기"):
    st.dataframe(load_data().head(20))

"""에이전트 루프.

Day 1: API 키 없이 동작하는 '규칙 기반 도우미'가 질문을 보고 도구를 고릅니다.
       (에이전트가 '어떤 도구를 골라 쓰는지'를 눈으로 확인하는 용도)
Day 2: choose_tool()을 LLM의 Tool Calling으로 바꿉니다. 나머지 흐름은 그대로입니다.
"""
from tools.data_tools import SENSOR_COLUMNS, TOOLS

SENSOR_ALIASES = {
    "온도": "chamber_temp", "temp": "chamber_temp",
    "압력": "pressure", "가스": "gas_flow", "유량": "gas_flow",
    "rf": "rf_power", "파워": "rf_power", "진동": "vibration",
}


def _find_sensor(question: str):
    q = question.lower()
    for s in SENSOR_COLUMNS:
        if s in q:
            return s
    for word, s in SENSOR_ALIASES.items():
        if word in q:
            return s
    return None


def choose_tool(question: str):
    """질문을 보고 사용할 도구와 인자를 정한다. (Day 2에 LLM으로 교체)"""
    q = question.lower()
    sensor = _find_sensor(question)
    if any(k in q for k in ["추이", "추세", "그래프", "차트", "trend"]):
        return "plot_trend", {"sensor": sensor or "chamber_temp"}
    if any(k in q for k in ["순위", "어떤 센서", "원인", "차이가 큰", "rank"]):
        return "rank_sensors", {}
    if sensor:
        return "get_sensor_stats", {"sensor": sensor}
    return "get_summary", {}


def describe(tool: str, result: dict) -> str:
    """도구 결과를 사람이 읽는 문장으로 정리한다. (Day 2에 LLM 답변으로 교체)"""
    if "error" in result:
        return result["error"]
    if tool == "get_summary":
        return (f"전체 {result['rows']}건 중 정상 {result['pass']}건, 불량 {result['fail']}건입니다. "
                f"결측값은 {result['missing_values']}개입니다.")
    if tool == "get_sensor_stats":
        return (f"{result['sensor']} 평균은 정상 {result['pass_mean']}, 불량 {result['fail_mean']}으로 "
                f"{result['difference']}만큼 차이가 납니다.")
    if tool == "rank_sensors":
        top = ", ".join(f"{s}({v})" for s, v in result["ranking"][:3])
        return f"불량과 연관성이 큰 센서 후보는 {top} 순입니다. {result['note']}"
    if tool == "plot_trend":
        return f"{result['sensor']}의 시간 추이 {result['points']}개 지점을 차트로 보여 드립니다."
    return str(result)


def run_agent(question: str, max_steps: int = 3) -> dict:
    """질문 → 도구 선택 → 실행 → 답변. 호출 기록(log)을 함께 돌려준다."""
    log = []
    tool, args = choose_tool(question)
    log.append({"step": "생각", "detail": f"도구 '{tool}' 선택, 인자 {args}"})
    result = TOOLS[tool](**args)
    log.append({"step": "행동·관찰", "detail": f"{tool} 실행 완료"})
    answer = describe(tool, result)
    return {"answer": answer, "tool": tool, "result": result, "log": log}

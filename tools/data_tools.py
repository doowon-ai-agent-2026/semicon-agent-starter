"""에이전트가 사용하는 데이터 분석 도구.

각 함수가 '도구(Tool)' 하나입니다. Day 2에는 이 함수들을 LLM의 Tool Calling에 연결합니다.
도구는 사람이 읽을 수 있는 dict를 돌려주고, 차트용 데이터는 'chart' 키에 담습니다.
"""
from functools import lru_cache

import pandas as pd

from config import DATA_PATH

SENSOR_COLUMNS = ["chamber_temp", "pressure", "gas_flow", "rf_power", "vibration"]


@lru_cache(maxsize=1)
def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def get_summary() -> dict:
    """데이터 전체 요약: 행·열 수, 정상/불량 수, 결측 수."""
    df = load_data()
    counts = df["label"].value_counts().to_dict()
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "pass": int(counts.get(-1, 0)),
        "fail": int(counts.get(1, 0)),
        "missing_values": int(df.isna().sum().sum()),
    }


def get_sensor_stats(sensor: str) -> dict:
    """센서 하나의 정상/불량 그룹별 평균과 차이."""
    if sensor not in SENSOR_COLUMNS:
        return {"error": f"알 수 없는 센서입니다: {sensor}. 사용 가능: {', '.join(SENSOR_COLUMNS)}"}
    df = load_data()
    g = df.groupby("label")[sensor].mean()
    return {
        "sensor": sensor,
        "pass_mean": round(float(g.get(-1)), 3),
        "fail_mean": round(float(g.get(1)), 3),
        "difference": round(float(g.get(1) - g.get(-1)), 3),
    }


def rank_sensors() -> dict:
    """정상/불량 평균 차이를 표준편차로 나눈 값으로 센서를 순위화 (통계적 연관성 후보)."""
    df = load_data()
    rows = []
    for s in SENSOR_COLUMNS:
        g = df.groupby("label")[s].mean()
        score = abs(g.get(1) - g.get(-1)) / df[s].std()
        rows.append((s, round(float(score), 2)))
    rows.sort(key=lambda r: r[1], reverse=True)
    return {"ranking": rows, "note": "통계적 연관성 후보이며 실제 원인 확정은 아닙니다."}


def plot_trend(sensor: str) -> dict:
    """센서 값의 시간 추이 (차트 데이터 반환)."""
    if sensor not in SENSOR_COLUMNS:
        return {"error": f"알 수 없는 센서입니다: {sensor}"}
    df = load_data()
    chart = df[["timestamp", sensor]].set_index("timestamp")
    return {"sensor": sensor, "points": len(chart), "chart": chart}


TOOLS = {
    "get_summary": get_summary,
    "get_sensor_stats": get_sensor_stats,
    "rank_sensors": rank_sensors,
    "plot_trend": plot_trend,
}

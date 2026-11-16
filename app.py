
import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 페이지 설정
st.set_page_config(
    page_title="부산에서 왜 떠나는가?",
    page_icon="🏙️",
    layout="wide"
)

# 스타일 설정
st.markdown("""
<style>
    .main {
        background-color: dark;
    }

    .university-name {
        font-size: 25px;
        font-weight: 700;
        color: dark;
    }

    .project-label {
        font-size: 13px;
        color: #7A8795;
    }

    .main-title {
        font-size: 40px;
        font-weight: 800;
        color: dark;
        margin-top: 25px;
        text-align: center;
    }

    .sub-title {
        font-size: 17px;
        color: white;
        margin-top: 5px;
        text-align: center;
    }

    .top-line {
        border-bottom: 2px solid #E5EAF0;
        margin-top: 15px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)



# 부산대학교 헤더
logo_path = Path("assets/pusan_logo.png")

col1, col2, col3, col4 = st.columns(
    [0.12, 0.36, 0.26, 0.26],
    vertical_alignment="center"
)

with col1:
    if logo_path.exists():
        st.image(str(logo_path), width=85)
    else:
        st.warning("로고 파일을 찾을 수 없습니다.")

with col2:
    st.markdown(
        '<div class="university-name">부산대학교</div>'
        '<div class="project-label">사회과학대학</div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div style="
            border-left: 1px solid #DCE3EC;
            padding-left: 20px;
        ">
            <div style="
                font-size: 17px;
                font-weight: 700;
                color: dark;
            ">까웅 삐에 손 윈</div>
            <div style="
                font-size: 17px;
                color: dark;
                margin-top: 5px;
            ">행정학과</div>
        </div>
         <div style="
                font-size: 17px;
                color: dark;
                margin-top: 5px;
            ">학번: 202305224</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div style="
            border-left: 1px solid #DCE3EC;
            padding-left: 20px;
        ">
            <div style="
                font-size: 17px;
                font-weight: 700;
                color: dark;
            ">까웅 세잇 린</div>
            <div style="
                font-size: 17px;
                color: dark;
                margin-top: 5px;
            ">미디어커뮤니케이션학과</div>
        </div>
        <div style="
                font-size: 17px;
                color: dark;
                margin-top: 5px;
            ">학번: 202406268</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# 대시보드 제목
st.markdown(
    '<div class="top-line"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">부산에서 왜 떠나는가?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">부산 인구 유출 원인 분석 대시보드</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="top-line"></div>',
    unsafe_allow_html=True
)


# 사이드바 메뉴
st.sidebar.title("분석 메뉴")

menu = st.sidebar.radio(
    "메뉴 선택",
    [
        "종합 분석",
        "인구 이동 현황",
        "전출 사유 분석",
        "일자리 분석",
        "산업 및 사업체 분석",
        "주거환경 분석",
        "정책적 시사점",
         "데이터 출처 및 분석 방법 정리"
    ]
)


# 메뉴별 화면
st.markdown("---")


# ==================================================
# 1. 종합 분석
# ==================================================

if menu == "종합 분석":

    st.header("종합 분석")
    st.write(
        "부산 인구 유출 현황과 주요 원인을 종합적으로 분석합니다."
    )

    # 데이터 불러오기
    reason_df = pd.read_csv(
        "data/processed/migration_reason_region.csv",
        encoding="utf-8-sig"
    )

    rate_df = pd.read_csv(
        "data/processed/migration_rate.csv",
        encoding="utf-8-sig"
    )

    # 연도별 부산 순이동률 데이터
    chart_df = rate_df[
        rate_df["행정구역(시도)별"] == "부산광역시"
    ].copy()

    chart_df["시점"] = pd.to_numeric(
        chart_df["시점"],
        errors="coerce"
    )

    chart_df = chart_df.dropna(
        subset=["시점"]
    )

    chart_df["시점"] = chart_df["시점"].astype(int)

    min_year = int(chart_df["시점"].min())
    max_year = int(chart_df["시점"].max())

    # 연도 선택
    st.markdown("---")
    st.subheader("연도별 부산 순이동률 변화")

    col1, col2 = st.columns(2)

    with col1:
        start_year = st.selectbox(
            "시작 연도",
            options=list(range(min_year, max_year + 1)),
            index=0,
            key="summary_start_year"
        )

    with col2:
        end_year = st.selectbox(
            "종료 연도",
            options=list(range(start_year, max_year + 1)),
            index=max_year - start_year,
            key="summary_end_year"
        )

    filtered_df = chart_df[
        (chart_df["시점"] >= start_year) &
        (chart_df["시점"] <= end_year)
    ].copy()

    filtered_df["연도"] = filtered_df["시점"].astype(str)

    # 순이동률 그래프
    st.line_chart(
        filtered_df,
        x="연도",
        y="순이동률(%)",
        use_container_width=True
    )

    # 선택 기간 핵심 지표
    st.markdown("---")
    st.subheader("선택 기간 핵심 지표")

    avg_rate = filtered_df["순이동률(%)"].mean()

    highest_row = filtered_df.loc[
        filtered_df["순이동률(%)"].idxmax()
    ]

    lowest_row = filtered_df.loc[
        filtered_df["순이동률(%)"].idxmin()
    ]

    latest_row = filtered_df.sort_values(
        "시점"
    ).iloc[-1]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "평균 순이동률",
        f"{avg_rate:.1f}%"
    )

    col2.metric(
        f"가장 높은 순이동률 ({int(highest_row['시점'])}년)",
        f"{highest_row['순이동률(%)']:.1f}%"
    )

    col3.metric(
        f"가장 낮은 순이동률 ({int(lowest_row['시점'])}년)",
        f"{lowest_row['순이동률(%)']:.1f}%"
    )

    col4.metric(
        f"종료 연도 순이동률 ({int(latest_row['시점'])}년)",
        f"{latest_row['순이동률(%)']:.1f}%"
    )

    st.caption(
        "순이동률이 음수이면 부산의 전출자가 전입자보다 많다는 의미입니다."
    )

    # 2025년 부산 외부 전출 사유 분석
    external_reason = reason_df[
        (reason_df["전출지별"] == "부산광역시") &
        (~reason_df["전입지별"].isin(["부산광역시", "전국"])) &
        (reason_df["전입사유별"] != "계")
    ].copy()

    reason_summary = external_reason.groupby(
        "전입사유별"
    )["2025"].sum()

    total_outflow = int(reason_summary.sum())

    top_reason = reason_summary.idxmax()
    top_count = int(reason_summary.max())

    job_count = int(
        reason_summary.get("직업", 0)
    )

    job_percent = (
        job_count / total_outflow * 100
        if total_outflow > 0 else 0
    )

    # 2025년 순이동률 및 전입·전출률
    busan_rate = rate_df[
        (rate_df["행정구역(시도)별"] == "부산광역시") &
        (rate_df["시점"].astype(str) == "2025")
    ]

    inflow_rate = float(
        busan_rate["총전입률(%)"].iloc[0]
    )

    outflow_rate = float(
        busan_rate["총전출률(%)"].iloc[0]
    )

    net_rate = float(
        busan_rate["순이동률(%)"].iloc[0]
    )

    # 2025년 핵심 지표
    st.markdown("---")
    st.subheader("2025년 핵심 지표")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "총전입률",
        f"{inflow_rate:.1f}%"
    )

    col2.metric(
        "총전출률",
        f"{outflow_rate:.1f}%"
    )

    col3.metric(
        "순이동률",
        f"{net_rate:.1f}%"
    )

    # 핵심 분석 결과
    st.markdown("---")
    st.subheader("핵심 분석 결과")

    st.write(
        "2025년 부산에서 다른 지역으로 이동한 사람들의 "
        "주요 전출 사유를 살펴봅니다."
    )

    top_reasons = reason_summary.sort_values(
        ascending=False
    ).head(3)

    card_colors = [
        "#EAF2FF",
        "#FCE8E8",
        "#EAF7F0"
    ]

    cols = st.columns(3)

    for i, (reason, count) in enumerate(top_reasons.items()):

        percentage = (
            count / total_outflow * 100
            if total_outflow > 0 else 0
        )

        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    background-color: {card_colors[i]};
                    border-radius: 14px;
                    padding: 22px;
                    min-height: 190px;
                    border: 1px solid #DCE3EC;
                ">
                    <p style="color:#64748B; margin:0;">
                        주요 전출 사유 {i + 1}위
                    </p>
                    <h2 style="color:#26364A; margin:10px 0;">
                        {reason}
                    </h2>
                    <h2 style="color:#142B49; margin:0;">
                        {int(count):,}명
                    </h2>
                    <p style="color:#475569; margin-top:10px;">
                        전체 전출자 중 비중: {percentage:.1f}%
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


    # 핵심 발견 TOP 3
    st.markdown("---")
    st.header("핵심 발견 TOP 3")

    finding_col1, finding_col2, finding_col3 = st.columns(3)

    with finding_col1:
        with st.container(border=True):
            st.subheader("01. 인구 순유출")
            st.metric(
                "2025년 순이동률",
                f"{net_rate:.1f}%"
            )
            st.write(
                "부산의 전출률과 전입률을 비교한 결과, "
                "인구 순유출 현상이 나타났습니다."
                if net_rate < 0
                else "부산의 전입률과 전출률을 비교하여 "
                     "인구 이동 흐름을 확인할 수 있습니다."
            )

    with finding_col2:
        with st.container(border=True):
            st.subheader("02. 주요 전출 사유")
            st.metric(
                f"가장 큰 전출 사유: {top_reason}",
                f"{top_count:,}명"
            )
            st.write(
                "2025년 부산에서 다른 지역으로 이동한 사람들 중 "
                f"{top_reason}을(를) 이유로 이동한 사람이 가장 많았습니다."
            )

    with finding_col3:
        with st.container(border=True):
            st.subheader("03. 직업 관련 전출")
            st.metric(
                "직업 사유 비중",
                f"{job_percent:.1f}%"
            )
            st.write(
                "직업을 이유로 전출한 인구의 비중을 통해 "
                "지역 내 일자리와 고용 환경의 중요성을 확인할 수 있습니다."
            )


# ==================================================
# 2. 인구 이동 현황
# ==================================================

elif menu == "인구 이동 현황":

    st.header("인구 이동 현황")
    st.write(
        "부산의 연도별 인구 이동 추이와 주요 전출 지역을 분석합니다."
    )

    # 데이터 불러오기
    flow_df = pd.read_csv(
        "data/processed/migration_flow.csv",
        encoding="utf-8-sig"
    )

    rate_df = pd.read_csv(
        "data/processed/migration_rate.csv",
        encoding="utf-8-sig"
    )

    # 연도 선택
    selected_year = st.selectbox(
        "분석 연도 선택",
        options=list(range(2025, 2015, -1)),
        index=0,
        key="migration_flow_year"
    )

    year_col = str(selected_year)

    # 부산 인구 이동률
    selected_rate = rate_df[
        (rate_df["행정구역(시도)별"] == "부산광역시") &
        (rate_df["시점"].astype(str) == year_col)
    ]

    inflow_rate = float(
        selected_rate["총전입률(%)"].iloc[0]
    )

    outflow_rate = float(
        selected_rate["총전출률(%)"].iloc[0]
    )

    net_rate = float(
        selected_rate["순이동률(%)"].iloc[0]
    )

    # 핵심 지표
    st.markdown("---")
    st.subheader("핵심 지표")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "총전입률",
        f"{inflow_rate:.1f}%"
    )

    col2.metric(
        "총전출률",
        f"{outflow_rate:.1f}%"
    )

    col3.metric(
        "순이동률",
        f"{net_rate:.1f}%"
    )

    # 부산 외부 전출 지역 분석
    external_flow = flow_df[
        (flow_df["전출지별"] == "부산광역시") &
        (flow_df["항목"] == "이동자수 (명)") &
        (~flow_df["전입지별"].isin(["부산광역시", "전국"]))
    ].copy()

    destination_chart = external_flow[
        ["전입지별", year_col]
    ].copy()

    destination_chart.columns = [
        "전출 지역",
        "이동자수"
    ]

    destination_chart["이동자수"] = pd.to_numeric(
        destination_chart["이동자수"],
        errors="coerce"
    )

    destination_chart = destination_chart.dropna()

    destination_chart = destination_chart.sort_values(
        "이동자수",
        ascending=False
    ).head(10)

    # 주요 전출 지역 그래프
    st.markdown("---")
    st.subheader(
        f"{selected_year}년 부산의 주요 전출 지역 TOP 10"
    )

    st.bar_chart(
        destination_chart.sort_values("이동자수"),
        x="전출 지역",
        y="이동자수",
        horizontal=True,
        use_container_width=True
    )

    # 가장 많이 이동한 지역
    if not destination_chart.empty:

        top_destination = destination_chart.iloc[0]

        st.markdown("---")
        st.subheader("주요 전출 지역 분석")

        col1, col2 = st.columns(2)

        col1.metric(
            "가장 많이 이동한 지역",
            top_destination["전출 지역"]
        )

        col2.metric(
            "해당 지역 이동자수",
            f"{int(top_destination['이동자수']):,}명"
        )
    st.info("""
    💡 핵심 내용

    부산에서 다른 지역으로 이동한 인구를 분석하면
    주요 전출 지역과 지역 간 인구 이동 흐름을 확인할 수 있습니다.
    특히 전출이 집중되는 지역을 파악하는 것은
    부산의 인구 유출 현상을 이해하는 데 도움이 됩니다.
    """)

# ==================================================
# 3. 전출 사유 분석
# ==================================================

elif menu == "전출 사유 분석":

    st.header("전출 사유 분석")
    st.write(
        "부산에서 다른 지역으로 이동한 사람들의 전출 사유를 분석합니다."
    )

    # 데이터 불러오기
    reason_df = pd.read_csv(
        "data/processed/migration_reason_region.csv",
        encoding="utf-8-sig"
    )

    # 연도 선택
    selected_year = st.selectbox(
        "분석 연도 선택",
        options=list(range(2025, 2015, -1)),
        index=0,
        key="migration_reason_year"
    )

    year_col = str(selected_year)

    # 부산에서 다른 지역으로 이동한 데이터만 추출
    external_reason = reason_df[
        (reason_df["전출지별"] == "부산광역시") &
        (~reason_df["전입지별"].isin(["부산광역시", "전국"])) &
        (reason_df["전입사유별"] != "계")
    ].copy()

    # 전출 사유별 이동자수 집계
    reason_summary = external_reason.groupby(
        "전입사유별"
    )[year_col].sum()

    reason_summary = reason_summary.sort_values(
        ascending=False
    )

    # 그래프용 데이터
    reason_chart = reason_summary.reset_index()

    reason_chart.columns = [
        "전출 사유",
        "이동자수"
    ]

    reason_chart["이동자수"] = pd.to_numeric(
        reason_chart["이동자수"],
        errors="coerce"
    )

    reason_chart = reason_chart.dropna()

    # 핵심 지표
    total_outflow = int(
        reason_chart["이동자수"].sum()
    )

    top_reason = reason_chart.iloc[0]["전출 사유"]
    top_count = int(
        reason_chart.iloc[0]["이동자수"]
    )

    job_count = int(
        reason_summary.get("직업", 0)
    )

    job_percent = (
        job_count / total_outflow * 100
        if total_outflow > 0 else 0
    )

    st.markdown("---")
    st.subheader("핵심 지표")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "외부 전출자 수",
        f"{total_outflow:,}명"
    )

    col2.metric(
        "가장 큰 전출 사유",
        top_reason,
        f"{top_count:,}명"
    )

    col3.metric(
        "직업 사유 비중",
        f"{job_percent:.1f}%"
    )

    # 전출 사유별 도넛 차트
    st.markdown("---")
    st.subheader(
        f"{selected_year}년 부산의 전출 사유 비중"
    )

    reason_chart["비중(%)"] = (
        reason_chart["이동자수"] / total_outflow * 100
    ).round(1)

    fig = px.pie(
        reason_chart,
        names="전출 사유",
        values="이동자수",
        hole=0.55,
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "이동자수: %{value:,.0f}명<br>"
            "비중: %{percent}<extra></extra>"
        )
    )

    fig.update_layout(
        showlegend=True,
        legend_title_text="전출 사유",
        margin=dict(t=20, b=20, l=20, r=20),
        height=430
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # 전출 사유별 상세 데이터
    st.markdown("---")
    st.subheader("전출 사유별 상세 데이터")

    st.dataframe(
        reason_chart,
        use_container_width=True,
        hide_index=True
    )
    st.info("""
    💡 핵심 내용

    2025년 부산의 전출 사유 중 직업이 45,162명으로 가장 많았으며,
    가족(33,707명), 주택(16,319명)이 그 뒤를 이었습니다.
    이는 직업과 주거 등 경제·생활 여건이 부산의 인구 이동과
    밀접하게 관련되어 있음을 보여줍니다.
    """)

# ==================================================
# 4. 일자리 분석
# ==================================================

elif menu == "일자리 분석":

    st.header("일자리 분석")
    st.markdown(
        "부산광역시 구·군별 고용률을 비교합니다."
    )

    # 데이터 불러오기
    employment_path = Path(
        "data/processed/employment.csv"
    )

    employment_df = pd.read_csv(
        employment_path
    )

    # 분석 시기 선택
    periods = [
        col for col in employment_df.columns
        if col[:4].isdigit() and "." in col
    ]

    periods = sorted(
        periods,
        reverse=True
    )

    period = st.selectbox(
        "분석 시기 선택",
        options=periods,
        index=0,
        key="employment_period"
    )

    # 고용률 데이터 필터링
    chart_df = employment_df[
        (employment_df["항목"] == "고용률 (%)") &
        (employment_df["연령별"] == "계")
    ].copy()

    chart_df = chart_df[
        ["행정구역별", period]
    ].copy()

    chart_df.columns = [
        "구·군",
        "고용률(%)"
    ]

    chart_df["고용률(%)"] = pd.to_numeric(
        chart_df["고용률(%)"],
        errors="coerce"
    )

    chart_df = chart_df.dropna()

    chart_df = chart_df.sort_values(
        "고용률(%)"
    )

    # 구·군별 고용률 막대그래프
    st.markdown("---")
    st.subheader(
        f"{period} 부산 구·군별 고용률"
    )

    st.bar_chart(
        chart_df,
        x="구·군",
        y="고용률(%)"
    )

    # 고용률 분석 결과
    st.markdown("---")
    st.subheader("구·군별 고용률 분석")

    average_rate = chart_df["고용률(%)"].mean()

    highest = chart_df.loc[
        chart_df["고용률(%)"].idxmax()
    ]

    lowest = chart_df.loc[
        chart_df["고용률(%)"].idxmin()
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "구·군 평균 고용률",
        f"{average_rate:.1f}%"
    )

    col2.metric(
        "고용률 최고 지역",
        highest["구·군"],
        f"{highest['고용률(%)']:.1f}%"
    )

    col3.metric(
        "고용률 최저 지역",
        lowest["구·군"],
        f"{lowest['고용률(%)']:.1f}%"
    )

    # 고용률 순위표
    st.markdown("---")
    st.subheader("구·군별 고용률 순위")

    ranking_df = chart_df.sort_values(
        "고용률(%)",
        ascending=False
    ).reset_index(drop=True)

    ranking_df.index = ranking_df.index + 1

    st.dataframe(
        ranking_df,
        width="stretch"
    )
    st.info("""
    💡 핵심 내용

    일자리 관련 통계는 부산의 고용 환경과 지역 내 경제활동 여건을
    파악하는 데 중요한 자료입니다.
    지역 내 안정적인 일자리 확보는 인구 유출 문제를 완화하기 위한
    주요 과제 중 하나입니다.
    """)

# ==================================================
# 5. 산업 및 사업체 분석
# ==================================================

elif menu == "산업 및 사업체 분석":

    st.header("산업 및 사업체 분석")
    st.write(
        "부산의 업종별 사업체 수와 종사자 수 변화를 비교합니다."
    )

    # 데이터 불러오기
    industry_df = pd.read_csv(
        "data/processed/사업체수__종사자수.csv",
        encoding="utf-8-sig"
    )

    # 연도 선택
    selected_year = st.selectbox(
        "분석 연도 선택",
        options=[2023, 2022, 2021, 2020],
        index=0,
        key="industry_year"
    )

    establishment_col = (
        f"{selected_year}_establishments"
    )

    employee_col = (
        f"{selected_year}_employees"
    )

    # 전체 사업체 기준 데이터
    chart_df = industry_df[
        industry_df["business_type"] == "계"
    ].copy()

    # 전체 산업 합계 행 제외
    chart_df = chart_df[
        chart_df["industry"] != "전체 산업"
    ].copy()

    # 숫자 변환
    chart_df[establishment_col] = pd.to_numeric(
        chart_df[establishment_col],
        errors="coerce"
    )

    chart_df[employee_col] = pd.to_numeric(
        chart_df[employee_col],
        errors="coerce"
    )

    chart_df = chart_df.dropna(
        subset=[
            establishment_col,
            employee_col
        ]
    )

    # 종사자 수 기준 TOP 8 업종
    chart_df = chart_df.sort_values(
        employee_col,
        ascending=False
    ).head(8)

    # 복합 차트 생성
    fig = make_subplots(
        specs=[[{"secondary_y": True}]]
    )

    # 사업체 수 막대그래프
    fig.add_trace(
        go.Bar(
            x=chart_df["industry"],
            y=chart_df[establishment_col],
            name="사업체 수",
            marker_color="#3979C9",
            hovertemplate=(
                "%{x}<br>"
                "사업체 수: %{y:,}개"
                "<extra></extra>"
            )
        ),
        secondary_y=False
    )

    # 종사자 수 선그래프
    fig.add_trace(
        go.Scatter(
            x=chart_df["industry"],
            y=chart_df[employee_col],
            name="종사자 수",
            mode="lines+markers",
            line=dict(
                color="#E58B42",
                width=3
            ),
            marker=dict(size=7),
            hovertemplate=(
                "%{x}<br>"
                "종사자 수: %{y:,}명"
                "<extra></extra>"
            )
        ),
        secondary_y=True
    )

    # 그래프 디자인
    fig.update_layout(
        height=480,
        template="plotly_white",
        hovermode="x unified",
        title=None,
        legend=dict(
            orientation="h",
            y=1.12,
            x=0
        ),
        margin=dict(
            t=65,
            b=100,
            l=60,
            r=60
        ),
        bargap=0.45
    )

    fig.update_xaxes(
        title=None,
        tickangle=-25,
        showgrid=False,
        automargin=True
    )

    fig.update_yaxes(
        title="사업체 수",
        secondary_y=False,
        showgrid=True
    )

    fig.update_yaxes(
        title="종사자 수",
        secondary_y=True,
        showgrid=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # 사업체 수와 종사자 수 관계 분석
    st.markdown("---")
    st.subheader("사업체 수와 종사자 수의 관계")

    st.write(
        "업종별 사업체 수와 종사자 수의 관계를 산점도로 비교합니다."
    )

    scatter_df = industry_df[
        (industry_df["business_type"] == "계") &
        (industry_df["industry"] != "전체 산업")
    ].copy()

    # 선택한 연도 데이터 숫자로 변환
    scatter_df[establishment_col] = pd.to_numeric(
        scatter_df[establishment_col],
        errors="coerce"
    )

    scatter_df[employee_col] = pd.to_numeric(
        scatter_df[employee_col],
        errors="coerce"
    )

    scatter_df = scatter_df.dropna(
        subset=[
            establishment_col,
            employee_col
        ]
    )

    # 산점도 생성
    fig_scatter = px.scatter(
        scatter_df,
        x=establishment_col,
        y=employee_col,
        color="industry",
        hover_name="industry",
        size=employee_col,
        size_max=25,
        labels={
            establishment_col: "사업체 수 (개)",
            employee_col: "종사자 수 (명)",
            "industry": "업종"
        },
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig_scatter.update_layout(
        height=550,
        template="plotly_white",
        showlegend=False,
        xaxis_title="사업체 수 (개)",
        yaxis_title="종사자 수 (명)",
        margin=dict(
            t=30,
            b=50,
            l=60,
            r=30
        )
    )

    fig_scatter.update_traces(
        marker=dict(
            opacity=0.8,
            line=dict(
                width=1,
                color="white"
            )
        ),
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "사업체 수: %{x:,}개<br>"
            "종사자 수: %{y:,}명"
            "<extra></extra>"
        )
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

    st.caption(
        "※ 각 점은 하나의 업종을 나타냅니다. "
        "이 그래프는 두 지표의 관계를 보여주며 인과관계를 의미하지 않습니다."
    )
    st.info("""
    💡 핵심 내용

    산업별 사업체와 종사자 현황을 통해 부산의 산업 구조와
    지역 경제의 고용 기반을 파악할 수 있습니다.
    산업 경쟁력 강화와 다양한 일자리 창출을 위한 정책적 노력이 필요합니다.
    """)

# ==================================================
# 6. 주거환경 분석
# ==================================================

elif menu == "주거환경 분석":

    st.header("주거환경 분석")

    st.write(
        "부산 아파트 매매가격지수를 통해 "
        "주거환경의 변화 흐름을 살펴봅니다."
    )

    # 데이터 불러오기
    
    # 전체 분석 기간 핵심 데이터 계산
    apartment_df = pd.read_csv(
        "data/processed/apartment_price.csv",
        encoding="utf-8-sig"
    )

    apartment_df["date"] = pd.to_datetime(
        apartment_df["date"],
        errors="coerce"
    )

    apartment_df["busan_apartment_price_index"] = pd.to_numeric(
        apartment_df["busan_apartment_price_index"],
        errors="coerce"
    )

    apartment_df = apartment_df.dropna(
        subset=["date", "busan_apartment_price_index"]
    ).sort_values("date")

    # 전체 분석 기간 핵심 데이터 계산
    first_index = apartment_df.iloc[0][
        "busan_apartment_price_index"
    ]

    last_index = apartment_df.iloc[-1][
        "busan_apartment_price_index"
    ]

    total_change = last_index - first_index

    total_percent = (
        (last_index / first_index - 1) * 100
    )

    first_date = apartment_df.iloc[0]["date"]
    last_date = apartment_df.iloc[-1]["date"]


    # 연도별 데이터 계산
    annual_df = (
        apartment_df.assign(
            연도=apartment_df["date"].dt.year
        )
        .groupby("연도")
        .agg(
            시작일=("date", "min"),
            종료일=("date", "max"),
            시작지수=("busan_apartment_price_index", "first"),
            마지막지수=("busan_apartment_price_index", "last"),
            평균지수=("busan_apartment_price_index", "mean")
        )
        .reset_index()
    )

    annual_df["기간 내 변화"] = (
        annual_df["마지막지수"] - annual_df["시작지수"]
    )

    annual_df["기간"] = annual_df.apply(
        lambda row: (
            f"{row['시작일']:%m월} ~ {row['종료일']:%m월}"
        ),
        axis=1
    )


    # 1. 주거환경 핵심 지표
    st.markdown("---")
    st.subheader("주거환경 핵심 지표")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "분석 시작 가격지수",
        f"{first_index:.2f}"
    )

    col2.metric(
        "최근 가격지수",
        f"{last_index:.2f}"
    )

    col3.metric(
        "전체 가격지수 변화",
        f"{total_change:+.2f}p",
        f"{total_percent:+.1f}%"
    )

    st.caption(
        f"분석 기간: {first_date:%Y년 %m월 %d일} ~ "
        f"{last_date:%Y년 %m월 %d일}"
    )

    # 2. 연도별 주거환경 변화
    st.markdown("---")
    st.subheader("연도별 주거환경 변화")
    st.write(
        "부산 아파트 매매가격지수는 분석 기간 동안 "
        "어떤 변화를 보였을까요?"
    )

    annual_df = annual_df.sort_values("연도").reset_index(drop=True)

    card_colors = {
        2021: "#EAF2FF",
        2022: "#FFF0F0",
        2023: "#FCE8E8",
        2024: "#FFF4E5",
        2025: "#EAF7F0",
        2026: "#F0EBFF"
    }

    for row_start in range(0, len(annual_df), 3):
        cols = st.columns(3)

        for col, (_, row) in zip(
            cols,
            annual_df.iloc[row_start:row_start + 3].iterrows()
        ):
            year = int(row["연도"])
            start_value = row["시작지수"]
            end_value = row["마지막지수"]
            average_value = row["평균지수"]
            difference = end_value - start_value
            card_color = card_colors.get(year, "#F1F5F9")

            if year == 2021:
                period_label = "7월 ~ 12월"
            elif year == 2026:
                period_label = "1월 ~ 7월"
            else:
                period_label = "1월 ~ 12월"

            with col:
                st.markdown(
                    f"""
                    <div style="
                        background-color: {card_color};
                        border-radius: 14px;
                        padding: 18px;
                        margin-bottom: 12px;
                        border: 1px solid #DCE3EC;
                        min-height: 235px;
                    ">
                        <h3 style="color:#26364A; margin:0;">
                            {year}년
                        </h3>
                        <p style="color:#64748B; margin-top:5px;">
                            {period_label}
                        </p>
                        <hr style="border:1px solid #FFFFFF;">
                        <p style="color:#475569; margin-bottom:4px;">
                            연평균 가격지수
                        </p>
                        <h2 style="color:#26364A; margin:0;">
                            {average_value:.2f}
                        </h2>
                        <p style="color:#475569;">
                            기간 내 변화:
                            <b>{difference:+.2f}p</b>
                        </p>
                        <p style="color:#475569; font-size:14px;">
                            시작 지수: {start_value:.2f}<br>
                            마지막 지수: {end_value:.2f}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.caption(
        "※ 2021년은 7월부터, 2026년은 7월까지의 관측 자료입니다."
    )

    # 3. 주요 변화 해석
    st.markdown("---")
    st.subheader("주요 변화 해석")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.caption("가격 하락")
            st.markdown("**① 2022~2023년 가격 하락**")
            st.write(
                "2022년과 2023년에는 아파트 매매가격지수가 "
                "각각 7.60p, 9.20p 하락했습니다."
            )

    with col2:
        with st.container(border=True):
            st.caption("하락 폭 둔화")
            st.markdown("**② 2024~2025년 하락 폭 둔화**")
            st.write(
                "2024년 2.90p, 2025년 1.00p 하락하여 "
                "이전 시기보다 하락 폭이 작아졌습니다."
            )

    with col3:
        with st.container(border=True):
            st.caption("소폭 상승")
            st.markdown("**③ 2026년 소폭 상승**")
            st.write(
                "2026년 1월부터 7월까지 가격지수는 "
                "0.30p 상승했습니다. 다만 일부 기간의 자료입니다."
            )
    st.info("""
    💡 핵심 내용

    아파트 매매가격지수의 변화는 부산의 주거시장 흐름을 파악하는
    중요한 지표입니다.
    주거비 부담과 주택시장 변화는 시민들의 주거 안정성에 영향을 줄 수
    있으므로 지속적인 관찰이 필요합니다.
    """)
# =========

# ==================================================
# 정책적 시사점
# ==================================================

elif menu == "정책적 시사점":

    st.title("정책적 시사점")

    st.write(
        "부산의 인구 이동 및 전출 사유 분석 결과를 바탕으로 "
        "인구 유출 문제를 완화하기 위한 정책적 방향을 제안합니다."
    )

    st.markdown("---")

    # 01. 청년 일자리 확대
    st.header("01. 청년 일자리 확대")

    st.metric(
        "2025년 직업 사유 전출 인구",
        "45,162명"
    )

    st.write("""
    2025년 부산의 외부 전출 사유 중 직업이 가장 큰 비중을 차지했습니다.

    이를 바탕으로 청년층이 부산에서 안정적으로 일할 수 있도록
    양질의 일자리를 확대하고, 지역 기업과 청년 인재 간의
    취업 연계를 강화할 필요가 있습니다.
    """)

    st.markdown("---")

    # 02. 주거 안정 지원
    st.header("02. 주거 안정 지원")

    st.metric(
        "2025년 주택 사유 전출 인구",
        "16,319명"
    )

    st.write("""
    주택을 이유로 부산을 떠나는 인구도 확인되었습니다.

    청년과 사회초년생의 주거비 부담을 줄이고,
    안정적으로 거주할 수 있도록 주거 지원 정책을 확대할 필요가 있습니다.

    또한 주택시장 변화를 지속적으로 모니터링하고
    지역별 주거 여건을 개선하는 노력이 필요합니다.
    """)

    st.markdown("---")

    # 03. 교육 및 생활환경 개선
    st.header("03. 교육 및 생활환경 개선")

    st.metric(
        "2025년 교육 사유 전출 인구",
        "10,817명"
    )

    st.write("""
    교육을 이유로 부산을 떠나는 인구도 나타났습니다.

    지역 내 교육 기회와 청년 성장 기반을 확대하고,
    문화·복지·생활 인프라를 개선하여
    시민들이 부산에서 지속적으로 생활할 수 있는 환경을 조성해야 합니다.
    """)

    st.markdown("---")

    # 종합 정책 방향
    st.header("종합 정책 방향")

    policy_col1, policy_col2, policy_col3 = st.columns(3)

    with policy_col1:
        with st.container(border=True):
            st.subheader("일자리")
            st.write("청년층을 위한 양질의 일자리와 취업 기회 확대")

    with policy_col2:
        with st.container(border=True):
            st.subheader("주거")
            st.write("주거비 부담 완화 및 안정적인 주거 환경 조성")

    with policy_col3:
        with st.container(border=True):
            st.subheader("생활환경")
            st.write("교육·문화·복지 인프라 및 지역 정착 여건 개선")

    st.markdown("---")

    st.subheader("최종 메시지")

    st.markdown("""
    **사람이 떠나는 도시에서, 사람이 머무는 도시로.**

    부산의 인구 유출 문제를 완화하기 위해서는
    일자리, 주거, 교육 및 생활환경을 함께 개선하는
    종합적인 지역 발전 전략이 필요합니다.
    """)

    st.caption(
        "※ 본 정책적 시사점은 KOSIS 통계 분석 결과를 바탕으로 도출한 정책 제안이며, "
        "개별 전출 사유와 정책 효과 사이의 인과관계를 직접 입증하는 것은 아닙니다."
    )


# ==================================================
elif menu == "데이터 출처 및 분석 방법 정리":

    st.title("DATA SOURCE & METHODOLOGY")
    st.subheader("데이터 출처 및 분석 방법")
    st.caption(
        "객관적인 국가통계를 바탕으로 부산의 인구 유출 현상을 분석했습니다."
    )

    st.divider()

    # 01. 데이터 출처
    st.header("01. 데이터 출처")

    st.info("OFFICIAL STATISTICS")

    st.subheader("KOSIS 국가통계포털")

    st.write("""
    본 대시보드에 활용된 통계자료는 KOSIS 국가통계포털에서 수집하였습니다.
    인구 이동, 전출 사유, 고용, 산업 및 주거환경 관련 통계자료를
    활용하여 부산의 인구 유출 현상을 분석했습니다.
    """)

    st.link_button(
        "KOSIS 국가통계포털 바로가기",
        "https://kosis.kr/"
    )

    st.divider()

    # 02. 주요 활용 데이터
    st.header("02. 주요 활용 데이터")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.subheader("인구 이동")
        st.write("전입·전출 및 순이동 현황")

    with col2:
        st.subheader("전출 사유")
        st.write("직업·가족·주택·교육 등")

    with col3:
        st.subheader("일자리 및 산업")
        st.write("고용 및 산업·사업체 통계")
        
    with col4:
        st.subheader("산업 및 사업체")
        st.write("산업별 사업체 및 종사자 현황")

    with col5:
        st.subheader("주거환경")
        st.write("아파트 매매가격지수")
    
    st.divider()

    # 03. 데이터 분석 과정
    st.header("03. 데이터 분석 과정")

    process_cols = st.columns(4)

    process_items = [
        ("01", "데이터 수집", "KOSIS"),
        ("02", "데이터 전처리", "Python · Pandas"),
        ("03", "데이터 시각화", "Plotly"),
        ("04", "대시보드 구현", "Streamlit")
    ]

    for col, (number, title, tool) in zip(process_cols, process_items):
        with col:
            with st.container(border=True):
                st.caption(number)
                st.subheader(title)
                st.write(tool)


    # 마무리
    st.markdown(
        """
        <div style="text-align:center; padding:35px 10px;">
            <h2>사람이 떠나는 도시에서,<br>사람이 머무는 도시로.</h2>
            <p>부산의 미래는 인구 변화의 원인을 이해하는 것에서 시작됩니다.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
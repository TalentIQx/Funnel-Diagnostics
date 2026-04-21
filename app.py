import streamlit as st
import pandas as pd
import plotly.express as px

# Neon-inspired layout theme
st.set_page_config(page_title="Talent Intelligence Slides", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #0b0b2b 0%, #111144 45%, #0e0e0e 100%);
        color: #F6F6F6;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .css-1d391kg, .css-18e3th9 {
        background-color: #1a1a1a;
        padding: 2rem;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #202020;
        border-radius: 8px 8px 0 0;
        color: #00FFFF;
        padding: 10px 18px;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #111;
        color: #FF69B4;
        border-bottom: 4px solid #FF69B4;
    }
    .metric-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(0,255,255,0.25);
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 0 18px rgba(0,255,255,0.08);
    }
    .metric-label {
        color: #A8F7FF;
        font-size: 0.95rem;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #FF69B4;
        font-size: 2rem;
        font-weight: 700;
    }
    .insight-box {
        background: rgba(255, 20, 147, 0.08);
        border-left: 4px solid #FF69B4;
        border-radius: 10px;
        padding: 14px 16px;
        margin: 10px 0;
        color: #F6F6F6;
    }
    .upload-box {
        background: rgba(0,255,255,0.05);
        border: 1px dashed rgba(0,255,255,0.35);
        border-radius: 12px;
        padding: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("✨ Talent & Job Trends")
st.caption("Created by Gabby Solano · Sources: Gallup, Levels.fyi, Microsoft Jobs Report, Pave, CA SB1162")


def load_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return None
    if uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    return pd.read_excel(uploaded_file)


def render_metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_funnel_diagnostics_tab():
    st.subheader("🧭 Funnel Diagnostics")
    st.caption("Upload a CSV or Excel export to visualize where candidates drop off, why offers are rejected, and where process friction is highest.")

    st.markdown('<div class="upload-box">Upload a CSV or Excel file. You can map columns below so you do not need to alter backend code each time.</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload candidate funnel data",
        type=["csv", "xlsx", "xls"],
        key="funnel_upload"
    )

    sample_df = pd.DataFrame({
        "Candidate_ID": range(1, 13),
        "Role": ["Software Engineer", "Software Engineer", "ML Engineer", "ML Engineer", "Product Manager", "Sales", "Sales", "Product Manager", "ML Engineer", "Software Engineer", "Sales", "ML Engineer"],
        "Stage": ["Applied", "Phone Screen", "Phone Screen", "Interview", "Final", "Phone Screen", "Offer", "Interview", "Offer", "Final", "Interview", "Offer"],
        "Status": ["Active", "Rejected", "Withdrew", "Withdrew", "Offer Rejected", "Rejected", "Offer Rejected", "Withdrew", "Offer Rejected", "Withdrew", "Rejected", "Offer Rejected"],
        "Reason": ["", "Compensation too low", "Not 100% remote", "Process took too long", "Better offer", "Compensation too low", "Compensation too low", "Hybrid flexibility", "Better offer", "Process took too long", "Compensation too low", "Remote flexibility"],
        "Offer_Outcome": ["", "", "", "", "Rejected", "", "Rejected", "", "Rejected", "", "", "Rejected"],
        "Days_In_Process": [2, 5, 7, 19, 28, 4, 31, 16, 26, 24, 9, 30],
        "Recruiter": ["A", "A", "A", "B", "B", "C", "C", "B", "A", "A", "C", "B"],
        "Location": ["Austin", "Austin", "Austin", "Austin", "Austin", "Remote", "Remote", "Austin", "Austin", "Remote", "Remote", "Austin"]
    })

    df = load_uploaded_file(uploaded_file)
    if df is None:
        st.info("No file uploaded yet. Showing sample data preview so you can test the module design.")
        df = sample_df.copy()

    cols = ["-- Select --"] + list(df.columns)

    st.markdown("### Column Mapping")
    c1, c2, c3 = st.columns(3)
    with c1:
        candidate_col = st.selectbox("Candidate ID", cols, index=cols.index("Candidate_ID") if "Candidate_ID" in cols else 0)
        stage_col = st.selectbox("Stage", cols, index=cols.index("Stage") if "Stage" in cols else 0)
        status_col = st.selectbox("Status", cols, index=cols.index("Status") if "Status" in cols else 0)
    with c2:
        reason_col = st.selectbox("Reason", cols, index=cols.index("Reason") if "Reason" in cols else 0)
        offer_col = st.selectbox("Offer Outcome", cols, index=cols.index("Offer_Outcome") if "Offer_Outcome" in cols else 0)
        days_col = st.selectbox("Days in Process", cols, index=cols.index("Days_In_Process") if "Days_In_Process" in cols else 0)
    with c3:
        role_col = st.selectbox("Role / Job", cols, index=cols.index("Role") if "Role" in cols else 0)
        recruiter_col = st.selectbox("Recruiter", cols, index=cols.index("Recruiter") if "Recruiter" in cols else 0)
        location_col = st.selectbox("Location", cols, index=cols.index("Location") if "Location" in cols else 0)

    if stage_col == "-- Select --" or status_col == "-- Select --":
        st.warning("Please map at least Stage and Status to continue.")
        st.dataframe(df.head(10), use_container_width=True)
        return

    work_df = df.copy()

    for col in [stage_col, status_col, reason_col, offer_col, role_col, recruiter_col, location_col]:
        if col != "-- Select --":
            work_df[col] = work_df[col].astype(str).str.strip()

    if days_col != "-- Select --":
        work_df[days_col] = pd.to_numeric(work_df[days_col], errors="coerce")

    st.markdown("### Filters")
    f1, f2, f3 = st.columns(3)

    with f1:
        if role_col != "-- Select --":
            role_options = ["All"] + sorted(work_df[role_col].dropna().unique().tolist())
            selected_role = st.selectbox("Role filter", role_options)
        else:
            selected_role = "All"

    with f2:
        if recruiter_col != "-- Select --":
            recruiter_options = ["All"] + sorted(work_df[recruiter_col].dropna().unique().tolist())
            selected_recruiter = st.selectbox("Recruiter filter", recruiter_options)
        else:
            selected_recruiter = "All"

    with f3:
        if location_col != "-- Select --":
            location_options = ["All"] + sorted(work_df[location_col].dropna().unique().tolist())
            selected_location = st.selectbox("Location filter", location_options)
        else:
            selected_location = "All"

    if role_col != "-- Select --" and selected_role != "All":
        work_df = work_df[work_df[role_col] == selected_role]
    if recruiter_col != "-- Select --" and selected_recruiter != "All":
        work_df = work_df[work_df[recruiter_col] == selected_recruiter]
    if location_col != "-- Select --" and selected_location != "All":
        work_df = work_df[work_df[location_col] == selected_location]

    total_candidates = len(work_df)
    withdrew_mask = work_df[status_col].str.lower().str.contains("withdrew|withdrawn", na=False)
    rejected_mask = work_df[status_col].str.lower().str.contains("rejected", na=False)

    if offer_col != "-- Select --":
        offer_rejected_mask = work_df[offer_col].str.lower().str.contains("reject", na=False)
    else:
        offer_rejected_mask = work_df[status_col].str.lower().str.contains("offer reject", na=False)

    withdrawal_rate = (withdrew_mask.sum() / total_candidates * 100) if total_candidates else 0
    rejection_rate = (offer_rejected_mask.sum() / total_candidates * 100) if total_candidates else 0
    slow_process_rate = 0
    if days_col != "-- Select --":
        slow_process_rate = ((withdrew_mask & (work_df[days_col] >= 21)).sum() / total_candidates * 100) if total_candidates else 0

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card("Candidates", f"{total_candidates:,}")
    with m2:
        render_metric_card("Withdrawal Rate", f"{withdrawal_rate:.1f}%")
    with m3:
        render_metric_card("Offer Rejection Rate", f"{rejection_rate:.1f}%")
    with m4:
        render_metric_card("Slow-Process Loss", f"{slow_process_rate:.1f}%")

    st.markdown("### Candidate Flow")
    stage_counts = work_df.groupby(stage_col).size().reset_index(name="Candidates")
    fig_stage = px.bar(
        stage_counts,
        x=stage_col,
        y="Candidates",
        color="Candidates",
        color_continuous_scale=["#00FFFF", "#8A2BE2", "#FF1493"],
        title="Candidate Volume by Stage"
    )
    fig_stage.update_layout(plot_bgcolor="#0e0e0e", paper_bgcolor="#0e0e0e", font_color="#F6F6F6")
    st.plotly_chart(fig_stage, use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        if reason_col != "-- Select --":
            dropoff_df = work_df[withdrew_mask | rejected_mask].copy()
            if not dropoff_df.empty:
                stage_reason = dropoff_df.groupby([stage_col, reason_col]).size().reset_index(name="Count")
                fig_heat = px.density_heatmap(
                    stage_reason,
                    x=stage_col,
                    y=reason_col,
                    z="Count",
                    color_continuous_scale="PuRd",
                    title="Candidate Loss Reasons by Stage"
                )
                fig_heat.update_layout(plot_bgcolor="#0e0e0e", paper_bgcolor="#0e0e0e", font_color="#F6F6F6")
                st.plotly_chart(fig_heat, use_container_width=True)

    with c2:
        if reason_col != "-- Select --":
            offer_reason_df = work_df[offer_rejected_mask].copy()
            if not offer_reason_df.empty:
                offer_reason_counts = offer_reason_df.groupby(reason_col).size().reset_index(name="Count").sort_values("Count", ascending=True)
                fig_offer = px.bar(
                    offer_reason_counts,
                    x="Count",
                    y=reason_col,
                    orientation="h",
                    color="Count",
                    color_continuous_scale="Sunsetdark",
                    title="Offer Rejection Reasons"
                )
                fig_offer.update_layout(plot_bgcolor="#0e0e0e", paper_bgcolor="#0e0e0e", font_color="#F6F6F6")
                st.plotly_chart(fig_offer, use_container_width=True)

    if reason_col != "-- Select --":
        withdrew_reason_df = work_df[withdrew_mask].copy()
        if not withdrew_reason_df.empty:
            withdrawal_counts = withdrew_reason_df.groupby(reason_col).size().reset_index(name="Count").sort_values("Count", ascending=False)
            fig_withdraw = px.bar(
                withdrawal_counts,
                x=reason_col,
                y="Count",
                color="Count",
                color_continuous_scale=["#00FFFF", "#00CED1", "#FF69B4"],
                title="Candidate Withdrawal Reasons"
            )
            fig_withdraw.update_layout(plot_bgcolor="#0e0e0e", paper_bgcolor="#0e0e0e", font_color="#F6F6F6")
            st.plotly_chart(fig_withdraw, use_container_width=True)

    st.markdown("### Insight Highlights")
    st.markdown('<div class="insight-box">Compensation-related loss is often the clearest signal that the hiring team is below market or misaligned with candidate expectations.</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box">Remote flexibility and hybrid design can be measured as conversion drivers, not just culture preferences.</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box">When candidates withdraw late in the process, speed and process design become executive-level business problems, not just recruiting issues.</div>', unsafe_allow_html=True)

    with st.expander("Preview uploaded data"):
        st.dataframe(work_df.head(20), use_container_width=True)


# Tabs for each campaign
tab1, tab2, tab3, tab4 = st.tabs(["💸 Hiring Costs", "⚖️ Compliance Fines", "🌐 Remote Trends", "🧭 Funnel Diagnostics"])

# --- Tab 1: Hiring Costs ---
with tab1:
    st.subheader("The True Cost of Unfilled Positions")
    days = list(range(1, 31))
    cost = [d * 1000 for d in days]
    fig1 = px.line(
        x=days,
        y=cost,
        labels={"x": "Days Unfilled", "y": "Cumulative Cost ($)"},
        title="Estimated Cost per Unfilled Role"
    )
    fig1.update_traces(line_color='#FF69B4')
    fig1.update_layout(plot_bgcolor="#0e0e0e", paper_bgcolor="#0e0e0e", font_color="#F6F6F6")
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown(
        """
        - 💰 **$1,000/day cost for unfilled positions**
        - 🚪 **50% candidate dropout rate** due to long interview timelines
        """
    )

# --- Tab 2: Compliance Fines ---
with tab2:
    st.subheader("The $10K Job Post Mistake")
    compliance_data = pd.DataFrame({
        "County": ["Los Angeles", "San Francisco", "Other CA"],
        "Violation Rate (%)": [68, 59, 48]
    })
    fig2 = px.bar(
        compliance_data,
        x="County",
        y="Violation Rate (%)",
        color="County",
        text="Violation Rate (%)",
        color_discrete_sequence=['#FF6347', '#FF1493', '#FFD700']
    )
    fig2.update_layout(plot_bgcolor="#0e0e0e", paper_bgcolor="#0e0e0e", font_color="#F6F6F6")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown(
        """
        - 🧨 **SB 1162 violations cost $10,000 per posting**
        - 🔍 **58% of CA startups are not compliant**
        - 🙅‍♀️ **45% fewer applicants** when salary data is missing
        """
    )

# --- Tab 3: Remote Work Trends ---
with tab3:
    st.subheader("Remote Work Trends 2025")
    remote = pd.DataFrame({
        "Model": ["Hybrid", "Fully Remote", "On-Site"],
        "Employees (%)": [50, 30, 20]
    })
    fig3 = px.pie(
        remote,
        names="Model",
        values="Employees (%)",
        hole=0.4,
        color_discrete_sequence=["#00FFFF", "#FF69B4", "#8A2BE2"]
    )
    fig3.update_layout(plot_bgcolor="#0e0e0e", paper_bgcolor="#0e0e0e", font_color="#F6F6F6")
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown(
        """
        - 💼 60% of all job applicants prefer remote options
        - ⏱️ Remote workers log **51 more productive minutes** per day
        """
    )

# --- Tab 4: Funnel Diagnostics ---
with tab4:
    render_funnel_diagnostics_tab()

st.markdown("---")
st.markdown("🧠 Designed to influence smarter hiring decisions and scalable workforce strategies.")

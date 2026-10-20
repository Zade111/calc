import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Appraisal Management Cost Calculator",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Internal vs. External AMC Cost Calculator")
st.markdown(
    "Compare the financial trade-offs between managing an in-house appraisal "
    "panel and outsourcing to an Appraisal Management Company (AMC)."
)

col1, col2 = st.columns(2)

with col1:
    st.header("🏢 Internal (In-House) Annual Costs")

    software_cost = st.number_input(
        "Annual Software & Technology Licensing ($)\n"
        "(LOS-integrated or standalone systems)",
        min_value=0,
        value=12000,
        step=500,
    )

    staff_cost = st.number_input(
        "Annual Staff Salaries ($)\n"
        "(Dedicated panel managers, compliance officers, admin support)",
        min_value=0,
        value=85000,
        step=1000,
    )

    overhead_pct = st.slider(
        "Payroll Taxes, Benefits & IT Overhead (% of salary)",
        min_value=0,
        max_value=50,
        value=30,
        step=5,
    )

    audit_cost = st.number_input(
        "Annual Compliance & Auditing Costs ($)\n"
        "(Validating Appraiser Independence Requirements/AIR)",
        min_value=0,
        value=5000,
        step=500,
    )

    loaded_staff_cost = staff_cost * (1 + overhead_pct / 100)
    total_fixed_internal = software_cost + loaded_staff_cost + audit_cost

with col2:
    st.header("🤝 External AMC Costs")

    amc_fee = st.slider(
        "AMC Management Fee per Order ($)",
        min_value=50,
        max_value=150,
        value=100,
        step=5,
    )

    st.header("📈 Business Volume")
    annual_volume = st.number_input(
        "Estimated Annual Appraisal Volume (Orders/Year)",
        min_value=1,
        value=1200,
        step=50,
    )

total_internal_cost = total_fixed_internal
total_amc_cost = annual_volume * amc_fee
break_even_volume = int(np.ceil(total_fixed_internal / amc_fee))

st.markdown("---")
st.header("🔍 Financial Comparison Summary")

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Total Fixed Internal Overhead", f"${total_fixed_internal:,.2f}")
with m2:
    st.metric(f"Total AMC Fees ({annual_volume} orders)", f"${total_amc_cost:,.2f}")
with m3:
    if total_internal_cost < total_amc_cost:
        st.metric(
            "Recommended Model",
            "🏢 Internal Management",
            delta=f"${total_amc_cost - total_internal_cost:,.2f} Savings",
        )
    elif total_amc_cost < total_internal_cost:
        st.metric(
            "Recommended Model",
            "🤝 External AMC",
            delta=f"${total_internal_cost - total_amc_cost:,.2f} Savings",
        )
    else:
        st.metric("Recommended Model", "Cost Parity")

st.info(
    f"💡 **Break-Even Volume:** You need at least **{break_even_volume:,} orders "
    "per year** to financially justify moving to an internal appraisal "
    "management model."
)

st.subheader("📉 Cost Projection Breakdown")

volumes = np.linspace(
    max(1, int(break_even_volume * 0.2)),
    int(max(annual_volume, break_even_volume) * 1.8),
    50,
)
internal_line = [total_fixed_internal for _ in volumes]
amc_line = [volume * amc_fee for volume in volumes]

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=volumes,
        y=internal_line,
        mode="lines",
        name="Internal Fixed Cost",
        line=dict(color="#2b5c8f", width=3),
    )
)
fig.add_trace(
    go.Scatter(
        x=volumes,
        y=amc_line,
        mode="lines",
        name="External AMC Variable Cost",
        line=dict(color="#e06666", width=3),
    )
)
fig.add_trace(
    go.Scatter(
        x=[annual_volume],
        y=[max(total_internal_cost, total_amc_cost)],
        mode="markers",
        name="Your Volume Target",
        marker=dict(size=12, color="black", symbol="diamond"),
    )
)

fig.update_layout(
    xaxis_title="Annual Appraisal Order Volume",
    yaxis_title="Total Annual Cost ($)",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

st.plotly_chart(fig, use_container_width=True)
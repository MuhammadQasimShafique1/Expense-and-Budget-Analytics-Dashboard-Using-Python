from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Budget & Expense Monitor", page_icon="📊", layout="wide")
st.title("📊 Budget & Expense Monitoring Dashboard")
st.caption("Demo dataset is synthetic. Replace CSVs with verified company records before using findings for decisions.")

ROOT = Path(__file__).parent
DATA = ROOT / "data"

@st.cache_data
def load_data():
    b = pd.read_csv(DATA / "budget.csv")
    e = pd.read_csv(DATA / "expenses.csv")
    for df in (b, e):
        df["Month"] = pd.to_datetime(df["Month"], errors="coerce")
        df["Department"] = df["Department"].astype("string").str.strip()
        df["Expense_Category"] = df["Expense_Category"].astype("string").str.strip()
    b["Approved_Budget"] = pd.to_numeric(b["Approved_Budget"], errors="coerce")
    e["Actual_Expense"] = pd.to_numeric(e["Actual_Expense"], errors="coerce")
    b = b.dropna(subset=["Month","Department","Expense_Category","Approved_Budget"])
    e = e.dropna(subset=["Month","Department","Expense_Category","Actual_Expense"])
    # Aggregate duplicate keys before merging to prevent accidental many-to-many joins.
    b = b.groupby(["Month","Department","Expense_Category"], as_index=False)["Approved_Budget"].sum()
    e = e.groupby(["Month","Department","Expense_Category"], as_index=False)["Actual_Expense"].sum()
    d = b.merge(e, on=["Month","Department","Expense_Category"], how="outer", validate="one_to_one")
    d[["Approved_Budget","Actual_Expense"]] = d[["Approved_Budget","Actual_Expense"]].fillna(0)
    d["Variance"] = d["Approved_Budget"] - d["Actual_Expense"]
    d["Overspend"] = d["Actual_Expense"] > d["Approved_Budget"]
    d["Utilization_%"] = d.apply(lambda r: (r["Actual_Expense"]/r["Approved_Budget"]*100) if r["Approved_Budget"] else None, axis=1)
    return d

df = load_data()
st.sidebar.header("Filters")
min_month, max_month = df["Month"].min().date(), df["Month"].max().date()
date_range = st.sidebar.date_input("Month range", value=(min_month, max_month), min_value=min_month, max_value=max_month)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start, end = pd.Timestamp(min_month), pd.Timestamp(max_month)
dep_opts = sorted(df["Department"].dropna().unique())
cat_opts = sorted(df["Expense_Category"].dropna().unique())
selected_dep = st.sidebar.multiselect("Department", dep_opts, default=dep_opts)
selected_cat = st.sidebar.multiselect("Expense category", cat_opts, default=cat_opts)
f = df[(df["Month"] >= start) & (df["Month"] <= end) &
       (df["Department"].isin(selected_dep)) & (df["Expense_Category"].isin(selected_cat))]

budget = f["Approved_Budget"].sum()
actual = f["Actual_Expense"].sum()
variance = budget - actual
util = actual / budget * 100 if budget else 0
over = f.loc[f["Overspend"]]
c1,c2,c3,c4 = st.columns(4)
c1.metric("Approved budget", f"PKR {budget:,.0f}")
c2.metric("Actual expenses", f"PKR {actual:,.0f}")
c3.metric("Remaining / (overspend)", f"PKR {variance:,.0f}", delta=f"{variance:,.0f} PKR")
c4.metric("Budget utilization", f"{util:.1f}%")

if not f.empty:
    monthly = f.groupby("Month", as_index=False)[["Approved_Budget","Actual_Expense"]].sum()
    fig = px.line(monthly, x="Month", y=["Approved_Budget","Actual_Expense"], markers=True,
                  title="Monthly approved budget vs actual expenses", labels={"value":"PKR","variable":"Measure"})
    st.plotly_chart(fig, use_container_width=True)
    dept = f.groupby("Department", as_index=False)[["Approved_Budget","Actual_Expense"]].sum()
    dept["Variance"] = dept["Approved_Budget"] - dept["Actual_Expense"]
    fig2 = px.bar(dept, x="Department", y=["Approved_Budget","Actual_Expense"], barmode="group",
                  title="Department-wise spending", labels={"value":"PKR","variable":"Measure"})
    st.plotly_chart(fig2, use_container_width=True)
    cat = f.groupby("Expense_Category", as_index=False)["Actual_Expense"].sum().sort_values("Actual_Expense", ascending=False)
    fig3 = px.pie(cat, names="Expense_Category", values="Actual_Expense", hole=.35, title="Actual expense category breakdown")
    st.plotly_chart(fig3, use_container_width=True)
    monthly["Variance"] = monthly["Approved_Budget"] - monthly["Actual_Expense"]
    fig4 = px.bar(monthly, x="Month", y="Variance", title="Monthly budget variance (positive = under budget)",
                  labels={"Variance":"Budget minus actual (PKR)"})
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Budget alerts")
    if over.empty:
        st.success("No department-category-month combinations exceed budget in the selected filters.")
    else:
        alerts = over[["Month","Department","Expense_Category","Approved_Budget","Actual_Expense","Variance","Utilization_%"]].copy()
        alerts["Month"] = alerts["Month"].dt.strftime("%Y-%m")
        alerts = alerts.sort_values("Variance")
        st.dataframe(alerts, use_container_width=True, hide_index=True)
    st.subheader("Detailed records")
    display = f.copy()
    display["Month"] = display["Month"].dt.strftime("%Y-%m")
    st.dataframe(display.sort_values(["Month","Department","Expense_Category"]), use_container_width=True, hide_index=True)
    st.download_button("Download filtered analysis CSV", f.to_csv(index=False).encode("utf-8"),
                       "filtered_budget_analysis.csv", "text/csv")
else:
    st.warning("No records match the selected filters.")
st.caption("Variance = Approved Budget − Actual Expense. Positive variance means under budget; negative variance means overspending.")

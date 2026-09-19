import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")

# --- Data yüklə ---
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_sales.csv", encoding="latin-1")
    return df

df = load_data()

# --- Başlıq ---
st.title("📊 Sales Performance Dashboard")
st.caption("Superstore satış datası üzərində Python + Streamlit ilə hazırlanmış interaktiv dashboard")

# --- Sidebar filtr ---
st.sidebar.header("Filtrlər")
months = sorted(df["Month"].unique())
selected_months = st.sidebar.multiselect("Ay seç", months, default=months)

filtered_df = df[df["Month"].isin(selected_months)]

# --- KPI kartları ---
col1, col2, col3 = st.columns(3)
col1.metric("Toplam Satış", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("Toplam Mənfəət", f"${filtered_df['Profit'].sum():,.0f}")
col3.metric("Orta Endirim", f"{filtered_df['Discount'].mean():.1%}")

st.divider()

# --- 1-ci sətir: Aylıq trend + Kateqoriya mənfəəti ---
c1, c2 = st.columns(2)

with c1:
    monthly = filtered_df.groupby("Month")["Sales"].sum().reset_index()
    fig1 = px.line(monthly, x="Month", y="Sales", title="Aylıq Satış Trendi", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    cat_profit = filtered_df.groupby("Category")["Profit"].sum().reset_index().sort_values("Profit")
    fig2 = px.bar(cat_profit, x="Profit", y="Category", orientation="h", title="Kateqoriya üzrə Mənfəət")
    st.plotly_chart(fig2, use_container_width=True)

# --- 2-ci sətir: Segment + Region ---
c3, c4 = st.columns(2)

with c3:
    seg_sales = filtered_df.groupby("Segment")["Sales"].sum().reset_index()
    fig3 = px.pie(seg_sales, values="Sales", names="Segment", title="Seqment üzrə Satış Payı", hole=0.4)
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    region_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()
    fig4 = px.bar(region_sales, x="Region", y="Sales", title="Region üzrə Satış")
    st.plotly_chart(fig4, use_container_width=True)

# --- 3-cü sətir: Sub-Category ---
subcat_sales = filtered_df.groupby("Sub-Category")["Sales"].sum().reset_index().sort_values("Sales")
fig5 = px.bar(subcat_sales, x="Sales", y="Sub-Category", orientation="h", title="Sub-Category üzrə Satış")
st.plotly_chart(fig5, use_container_width=True)

st.divider()
st.caption("Data mənbəyi: Kaggle — Superstore Sales Dataset")

import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# الاتصال بقاعدة البيانات
conn = psycopg2.connect(
    host="localhost",
    port="5434",
    user="postgres",
    password="postgres",
    dbname="postgres"
)

# استعلام البيانات
query = """
SELECT * FROM combined_prices
ORDER BY timestamp DESC
LIMIT 1000;
"""

df = pd.read_sql(query, conn)
df["timestamp"] = pd.to_datetime(df["timestamp"])

st.set_page_config(page_title="Live Crypto Dashboard", layout="wide")
st.title("📊 Lambda Architecture - Crypto Dashboard")

# الفلتر الجانبي
with st.sidebar:
    st.header("🔍 الفلاتر")

    # اختيار العملة
    symbols = df["symbol"].unique().tolist()
    selected_symbol = st.selectbox("اختر العملة:", symbols)

    # فلتر بالتاريخ
    min_date = df['timestamp'].min().date()
    max_date = df['timestamp'].max().date()
    date_range = st.date_input("اختر فترة زمنية:", [min_date, max_date])

# تطبيق الفلاتر
filtered_df = df[df["symbol"] == selected_symbol]
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[(filtered_df["timestamp"].dt.date >= start_date) & (filtered_df["timestamp"].dt.date <= end_date)]

# رسم بياني للسعر
st.subheader(f"📈 اتجاه السعر لـ {selected_symbol}")
fig = px.line(filtered_df.sort_values("timestamp"), x="timestamp", y="price", color="source", title="Price Over Time")
st.plotly_chart(fig, use_container_width=True)

# إحصائيات سريعة
st.subheader("📊 إحصائيات")
col1, col2, col3 = st.columns(3)
col1.metric("أعلى سعر", f"{filtered_df['price'].max():,.2f}")
col2.metric("أقل سعر", f"{filtered_df['price'].min():,.2f}")
col3.metric("متوسط السعر", f"{filtered_df['price'].mean():,.2f}")

# عدد السجلات حسب المصدر
st.subheader("🟢 عدد السجلات حسب المصدر (batch/stream)")
st.bar_chart(filtered_df.groupby("source")["price"].count())

# جدول البيانات
st.subheader("📋 البيانات الكاملة")
st.dataframe(filtered_df.sort_values("timestamp", ascending=False), use_container_width=True)

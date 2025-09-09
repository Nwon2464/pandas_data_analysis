import os
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st

from lib.data_prep import (
    load_data,
    filter_data,
    kpis,
    monthly_revenue,
    monthly_orders,
    category_revenue,
    returns_by_category,
    country_revenue,
    channel_revenue,
    aov_by_month,
    top_products,
    top_customers,
)

st.set_page_config(page_title="E-commerce Insights (pandas)", layout="wide")

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "ecommerce_orders.csv")
df = load_data(DATA_PATH)

st.title("E-commerce Insights")

with st.sidebar:
    st.header("Filters")
    # 1) Date range
    min_date = df["order_date"].min().date()
    max_date = df["order_date"].max().date()
    date_from, date_to = st.date_input("Date range", (min_date, max_date))

    # 2) Country
    country = st.multiselect("Country", options=sorted(df["country"].unique().tolist()))

    # 3) Region (depends on country but allow global)
    regions = df["region"].unique().tolist()
    if country:
        regions = df[df["country"].isin(country)]["region"].unique().tolist()
    region = st.multiselect("Region", options=sorted(regions))

    # 4) Channel
    channel = st.multiselect("Channel", options=sorted(df["channel"].unique().tolist()))

    # 5) Category
    category = st.multiselect(
        "Category", options=sorted(df["product_category"].unique().tolist())
    )

    # 6) Product
    prod_options = df["product_name"].unique().tolist()
    if category:
        prod_options = (
            df[df["product_category"].isin(category)]["product_name"].unique().tolist()
        )
    product_name = st.multiselect("Product", options=sorted(prod_options))

    # 7) Returned
    returned_state = st.selectbox(
        "Returned", options=["All", "Returned", "Not Returned"], index=0
    )

    # 8) Price range
    pmin, pmax = float(df["unit_price"].min()), float(df["unit_price"].max())
    price_range = st.slider(
        "Unit Price Range",
        min_value=float(pmin),
        max_value=float(pmax),
        value=(float(pmin), float(pmax)),
    )

    # 9) Quantity range
    qmin, qmax = int(df["quantity"].min()), int(df["quantity"].max())
    qty_range = st.slider(
        "Quantity Range",
        min_value=int(qmin),
        max_value=int(qmax),
        value=(int(qmin), int(qmax)),
    )

    # 10) Discount range
    dmin, dmax = float(df["discount_rate"].min()), float(df["discount_rate"].max())
    discount_range = st.slider(
        "Discount Rate Range",
        min_value=float(0.0),
        max_value=float(0.3),
        value=(float(dmin), float(dmax)),
        step=0.01,
    )

# Apply filters
dff = filter_data(
    df,
    date_from=date_from,
    date_to=date_to,
    country=country,
    region=region,
    channel=channel,
    category=category,
    product_name=product_name,
    returned_state=returned_state,
    price_range=price_range,
    qty_range=qty_range,
    discount_range=discount_range,
)

# KPIs
m = kpis(dff)
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Net Revenue", f"${m['total_net_revenue']:,.0f}")
if m["total_gross_revenue"] is not None:
    c2.metric("Gross Revenue", f"${m['total_gross_revenue']:,.0f}")
else:
    c2.metric("Gross Revenue", "-")
c3.metric("Orders", f"{m['orders']:,.0f}")
c4.metric("Customers", f"{m['customers']:,.0f}")
c5.metric("AOV", f"${m['aov']:,.2f}")
c6.metric("Return Rate", f"{m['return_rate']*100:.2f}%")

st.divider()

# --- Row 1: Monthly Revenue | Monthly Orders
col1, col2 = st.columns(2)
with col1:
    st.subheader("Monthly Revenue")
    mr = monthly_revenue(dff)
    fig1, ax1 = plt.subplots()
    ax1.plot(mr["year_month"], mr["net_revenue"], marker="o")
    ax1.set_xlabel("Year-Month")
    ax1.set_ylabel("Net Revenue")
    ax1.tick_params(axis="x", labelrotation=45)
    st.pyplot(fig1)

with col2:
    st.subheader("Monthly Orders")
    mo = monthly_orders(dff)
    fig2, ax2 = plt.subplots()
    ax2.plot(mo["year_month"], mo["orders"], marker="o")
    ax2.set_xlabel("Year-Month")
    ax2.set_ylabel("Orders")
    ax2.tick_params(axis="x", labelrotation=45)
    st.pyplot(fig2)

# --- Row 2: Revenue by Category | Return Rate by Category
col3, col4 = st.columns(2)
with col3:
    st.subheader("Revenue by Category")
    cr = category_revenue(dff)
    fig3, ax3 = plt.subplots()
    ax3.bar(cr["product_category"], cr["net_revenue"])
    ax3.set_xlabel("Category")
    ax3.set_ylabel("Net Revenue")
    st.pyplot(fig3)

with col4:
    st.subheader("Return Rate by Category")
    rbc = returns_by_category(dff)
    fig4, ax4 = plt.subplots()
    ax4.bar(rbc["product_category"], rbc["return_rate"] * 100)
    ax4.set_xlabel("Category")
    ax4.set_ylabel("Return Rate (%)")
    st.pyplot(fig4)

# --- Row 3: Revenue by Country | Revenue by Channel
col5, col6 = st.columns(2)
with col5:
    st.subheader("Revenue by Country")
    co = country_revenue(dff)
    fig5, ax5 = plt.subplots()
    ax5.bar(co["country"], co["net_revenue"])
    ax5.set_xlabel("Country")
    ax5.set_ylabel("Net Revenue")
    st.pyplot(fig5)

with col6:
    st.subheader("Revenue by Channel")
    ch = channel_revenue(dff)
    fig6, ax6 = plt.subplots()
    ax6.bar(ch["channel"], ch["net_revenue"])
    ax6.set_xlabel("Channel")
    ax6.set_ylabel("Net Revenue")
    st.pyplot(fig6)

# --- Row 4: AOV by Month | Top Products (table)
col7, col8 = st.columns(2)
with col7:
    st.subheader("Average Order Value by Month")
    am = aov_by_month(dff)
    fig7, ax7 = plt.subplots()
    ax7.plot(am["year_month"], am["aov"], marker="o")
    ax7.set_xlabel("Year-Month")
    ax7.set_ylabel("AOV")
    ax7.tick_params(axis="x", labelrotation=45)
    st.pyplot(fig7)

with col8:
    st.subheader("Top Products")
    st.dataframe(top_products(dff, 10))

# --- Row 5: Top Customers (table) | Download
col9, col10 = st.columns(2)
with col9:
    st.subheader("Top Customers")
    st.dataframe(top_customers(dff, 10))

with col10:
    st.subheader("Download")
    st.download_button(
        label="Download filtered CSV",
        data=dff.to_csv(index=False).encode("utf-8"),
        file_name="filtered_orders.csv",
        mime="text/csv",
    )

st.caption("pandas + matplotlib + Streamlit")

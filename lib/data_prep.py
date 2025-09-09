import pandas as pd
import numpy as np

def load_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, parse_dates=["order_date"])
    df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
    df["aov"] = df["net_revenue"] / df["quantity"]
    return df

def filter_data(
    df: pd.DataFrame,
    date_from=None,
    date_to=None,
    country=None,
    region=None,
    channel=None,
    category=None,
    product_name=None,
    returned_state: str = "All",  # "All", "Returned", "Not Returned"
    price_range=None,  # (min_price, max_price)
    qty_range=None,    # (min_qty, max_qty)
    discount_range=None,  # (min_disc, max_disc) in [0,1]
):
    dff = df.copy()

    if date_from is not None:
        dff = dff[dff["order_date"] >= pd.to_datetime(date_from)]
    if date_to is not None:
        dff = dff[dff["order_date"] <= pd.to_datetime(date_to)]

    if country and len(country) > 0:
        dff = dff[dff["country"].isin(country)]

    if region and len(region) > 0:
        dff = dff[dff["region"].isin(region)]

    if channel and len(channel) > 0:
        dff = dff[dff["channel"].isin(channel)]

    if category and len(category) > 0:
        dff = dff[dff["product_category"].isin(category)]

    if product_name and len(product_name) > 0:
        dff = dff[dff["product_name"].isin(product_name)]

    if returned_state == "Returned":
        dff = dff[dff["returned"] == 1]
    elif returned_state == "Not Returned":
        dff = dff[dff["returned"] == 0]

    if price_range is not None:
        lo, hi = price_range
        dff = dff[(dff["unit_price"] >= lo) & (dff["unit_price"] <= hi)]

    if qty_range is not None:
        lo, hi = qty_range
        dff = dff[(dff["quantity"] >= lo) & (dff["quantity"] <= hi)]

    if discount_range is not None:
        lo, hi = discount_range
        dff = dff[(dff["discount_rate"] >= lo) & (dff["discount_rate"] <= hi)]

    return dff

def kpis(df: pd.DataFrame) -> dict:
    total_net = float(df["net_revenue"].sum())
    total_gross = float(df["gross_revenue"].sum()) if "gross_revenue" in df else float(np.nan)
    orders = int(df["order_id"].nunique())
    customers = int(df["customer_id"].nunique())
    aov = float(df["net_revenue"].sum() / max(1, orders))
    return_rate = float(df["returned"].mean()) if len(df) else 0.0
    discount_amt = float((df["gross_revenue"] - df["net_revenue"]).sum())
    return {
        "total_net_revenue": round(total_net, 2),
        "total_gross_revenue": round(total_gross, 2) if not np.isnan(total_gross) else None,
        "orders": orders,
        "customers": customers,
        "aov": round(aov, 2),
        "return_rate": round(return_rate, 4),
        "discount_amount": round(discount_amt, 2),
    }

def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("year_month")["net_revenue"]
              .sum()
              .reset_index()
              .sort_values("year_month"))

def monthly_orders(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("year_month")["order_id"]
              .nunique()
              .reset_index(name="orders")
              .sort_values("year_month"))

def category_revenue(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("product_category")["net_revenue"]
              .sum()
              .reset_index()
              .sort_values("net_revenue", ascending=False))

def returns_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("product_category")["returned"]
              .mean()
              .reset_index()
              .rename(columns={"returned":"return_rate"})
              .sort_values("return_rate", ascending=False))

def country_revenue(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("country")["net_revenue"]
              .sum()
              .reset_index()
              .sort_values("net_revenue", ascending=False))

def channel_revenue(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("channel")["net_revenue"]
              .sum()
              .reset_index()
              .sort_values("net_revenue", ascending=False))

def aov_by_month(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("year_month").agg({"net_revenue":"sum","order_id":"nunique"}).reset_index()
    g["aov"] = g["net_revenue"] / g["order_id"].replace(0, 1)
    return g[["year_month","aov"]].sort_values("year_month")

def top_products(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    return (df.groupby("product_name")["net_revenue"]
              .sum()
              .reset_index()
              .sort_values("net_revenue", ascending=False)
              .head(top_n))

def top_customers(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    return (df.groupby("customer_id")["net_revenue"]
              .sum()
              .reset_index()
              .sort_values("net_revenue", ascending=False)
              .head(top_n))

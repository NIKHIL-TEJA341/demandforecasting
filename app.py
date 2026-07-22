import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import json
import gc
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title = "Apple Retail Demand Forecasting",
    page_icon  = "🍎",
    layout     = "wide",
    initial_sidebar_state = "expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global Font */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Main background */
    .main { background-color: #ffffff; }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Sidebar Background & Headers */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: none !important;
    }
    
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] * {
        color: #f8fafc !important;
    }

    /* Sidebar Selectbox Container, Control & Text - Works on Local & Streamlit Cloud */
    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] {
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] > div,
    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"],
    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] div,
    section[data-testid="stSidebar"] div[data-baseweb="select"] div[role="combobox"] {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border-color: #334155 !important;
        border-radius: 8px !important;
    }

    /* Selectbox selected value text & icons */
    section[data-testid="stSidebar"] div[data-baseweb="select"] span,
    section[data-testid="stSidebar"] div[data-baseweb="select"] p,
    section[data-testid="stSidebar"] div[data-baseweb="select"] div,
    section[data-testid="stSidebar"] div[data-baseweb="select"] input {
        color: #f8fafc !important;
        background-color: transparent !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
        fill: #f8fafc !important;
        color: #f8fafc !important;
    }

    /* Dropdown Menu Popover Options (Expanded Selectbox) */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] li {
        background-color: #1e293b !important;
        color: #f8fafc !important;
    }
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="popover"] li[aria-selected="true"] {
        background-color: #0071e3 !important;
        color: #ffffff !important;
    }
    div[data-baseweb="popover"] span,
    div[data-baseweb="popover"] p,
    div[data-baseweb="popover"] div {
        color: #f8fafc !important;
    }

    /* Headers */
    h1 { color: #111827 !important; font-weight: 800 !important; }
    h2, h3 { color: #1e293b !important; font-weight: 700 !important; }

    /* Tab styling for Local and Streamlit Cloud */
    div[data-testid="stTabs"] [data-baseweb="tab-list"],
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: transparent !important;
        border-bottom: none !important;
        padding-bottom: 4px !important;
    }

    div[data-testid="stTabs"] button[data-baseweb="tab"],
    div[data-testid="stTabs"] button[role="tab"],
    div[data-testid="stTabs"] [data-testid="stTab"],
    .stTabs [data-baseweb="tab"],
    .stTabs button {
        background-color: #1e293b !important;
        border-radius: 8px !important;
        color: #f8fafc !important;
        padding: 10px 24px !important;
        border: 1px solid #334155 !important;
        margin-right: 4px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"],
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"],
    div[data-testid="stTabs"] [aria-selected="true"],
    .stTabs [aria-selected="true"] {
        background-color: #0071e3 !important;
        color: #ffffff !important;
        border-color: #0071e3 !important;
        box-shadow: 0 4px 12px rgba(0, 113, 227, 0.3) !important;
    }

    div[data-testid="stTabs"] button[data-baseweb="tab"]:hover,
    div[data-testid="stTabs"] button[role="tab"]:hover {
        background-color: #334155 !important;
        color: #ffffff !important;
    }

    div[data-testid="stTabs"] [data-baseweb="tab-highlight-title"],
    div[data-testid="stTabs"] [data-baseweb="tab-border"],
    .stTabs [data-baseweb="tab-highlight-title"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
        height: 0px !important;
    }

    /* Predict button */
    div.stButton > button {
        background-color: #0071e3 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 30px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: 0.3s !important;
    }
    div.stButton > button:hover {
        background-color: #0077ed !important;
        transform: scale(1.02) !important;
    }

    /* Badges */
    .badge-actual {
        background-color: #10b981;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 13px;
    }
    .badge-predicted {
        background-color: #0071e3;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 13px;
    }

    /* Custom Info & Placeholder */
    .custom-info-box {
        background-color: #eff6ff;
        color: #1d4ed8;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #bfdbfe;
        display: flex;
        align-items: center;
        gap: 12px;
        font-weight: 500;
        margin-bottom: 20px;
    }
    .placeholder-box {
        border: 2px dashed #cbd5e1;
        border-radius: 16px;
        padding: 60px 20px;
        text-align: center;
        color: #94a3b8;
        background-color: #f8fafc;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_models():
    with open('xgb_model.pkl', 'rb') as f:
        xgb_model = pickle.load(f)
    with open('le_store.pkl', 'rb') as f:
        le_store = pickle.load(f)
    with open('le_category.pkl', 'rb') as f:
        le_category = pickle.load(f)
    with open('le_country.pkl', 'rb') as f:
        le_country = pickle.load(f)
    return xgb_model, None, le_store, le_category, le_country

@st.cache_resource
def load_data():
    monthly_store     = pd.read_csv('monthly_store.csv')
    store_share       = pd.read_csv('store_share.csv')
    store_cat_avg     = pd.read_csv('store_cat_avg.csv')
    prophet_forecast  = pd.read_csv('prophet_forecast.csv')
    master_df         = pd.read_csv('master_df.csv.gz')

    with open('country_store_map.json', 'r') as f:
        country_store_map = json.load(f)
    with open('features.json', 'r') as f:
        features = json.load(f)

    master_df['sale_date']       = pd.to_datetime(master_df['sale_date'])
    prophet_forecast['ds']       = pd.to_datetime(prophet_forecast['ds'])

    prophet_forecast['yhat']       = prophet_forecast['yhat'].clip(lower=0)
    prophet_forecast['yhat_lower'] = prophet_forecast['yhat_lower'].clip(lower=0)
    prophet_forecast['yhat_upper'] = prophet_forecast['yhat_upper'].clip(lower=0)

    monthly_season = monthly_store.groupby('month')['total_quantity'].sum().reset_index()
    monthly_season['seasonal_ratio'] = (
        monthly_season['total_quantity'] /
        monthly_season['total_quantity'].mean()
    )
    monthly_season_ratio = dict(
        zip(monthly_season['month'], monthly_season['seasonal_ratio'])
    )

    return (monthly_store, store_share, store_cat_avg,
            prophet_forecast, master_df,
            country_store_map, features,
            monthly_season_ratio)

with st.spinner("🍎 Loading Apple Retail Platform..."):
    xgb_model, prophet_model, le_store, le_category, le_country = load_models()
    (monthly_store, store_share, store_cat_avg,
     prophet_forecast, master_df,
     country_store_map, features,
     monthly_season_ratio) = load_data()

def predict_future(store_id, category_name, country, year, month):
    last_known = monthly_store[
        (monthly_store['store_id']      == store_id) &
        (monthly_store['category_name'] == category_name)
    ].sort_values(['year','month']).tail(12)

    if last_known.empty:
        return 0, 0
    lag1            = last_known['total_quantity'].iloc[-1]
    lag2            = last_known['total_quantity'].iloc[-2] if len(last_known) >= 2 else lag1
    lag3            = last_known['total_quantity'].iloc[-3] if len(last_known) >= 3 else lag1
    lag12           = last_known['total_quantity'].iloc[0]
    rolling_m3      = last_known['total_quantity'].tail(3).mean()
    rolling_m6      = last_known['total_quantity'].tail(6).mean()
    avg_price       = last_known['avg_price'].iloc[-1]
    store_share_v   = last_known['store_share'].iloc[-1]
    store_cat_avg_v = last_known['store_cat_avg_qty'].iloc[-1]
    momentum        = lag1 - lag2
    quarter         = (month - 1) // 3 + 1
    month_sin       = np.sin(2 * np.pi * month / 12)
    month_cos       = np.cos(2 * np.pi * month / 12)
    is_peak_month   = 1 if month in [9, 11, 12] else 0
    is_q4           = 1 if quarter == 4 else 0

    try:
        store_enc    = le_store.transform([store_id])[0]
        category_enc = le_category.transform([category_name])[0]
        country_enc  = le_country.transform([country])[0]
    except:
        return 0, 0

    input_df = pd.DataFrame([{
        'year'             : year,
        'month'            : month,
        'quarter'          : quarter,
        'store_enc'        : store_enc,
        'category_enc'     : category_enc,
        'country_enc'      : country_enc,
        'avg_price'        : avg_price,
        'store_share'      : store_share_v,
        'lag_1'            : lag1,
        'lag_2'            : lag2,
        'lag_3'            : lag3,
        'lag_12'           : lag12,
        'rolling_mean_3'   : rolling_m3,
        'rolling_mean_6'   : rolling_m6,
        'month_sin'        : month_sin,
        'month_cos'        : month_cos,
        'is_peak_month'    : is_peak_month,
        'is_q4'            : is_q4,
        'store_cat_avg_qty': store_cat_avg_v,
        'momentum'         : momentum
    }])

    predicted_qty = max(0, xgb_model.predict(input_df)[0])

    if year >= 2025:
        season_ratio = monthly_season_ratio.get(month, 1.0)
        predicted_qty = int(round(predicted_qty * season_ratio))

    predicted_rev = predicted_qty * avg_price
    return int(predicted_qty), int(predicted_rev)

st.markdown("""
    <div style='text-align:center; padding: 20px 0px 10px 0px;'>
        <h1 style='color:#1c1c1e; font-size:42px; font-weight:700;'>
            🍎 Apple Retail Demand Forecasting
        </h1>
        <p style='color:#333333; font-size:18px;'>
            Real-time Sales Intelligence & Predictive Analytics Platform
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding:10px;'>
            <h2 style='color:#f5f5f7;'>🔍 Filter Panel</h2>
            <p style='color:#86868b; font-size:13px;'>
                Select inputs to generate insights
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    year = st.selectbox(
        "📅 Select Year",
        options = list(range(2020, 2027)),
        index   = 3
    )

    month_names = {
        "January":1,"February":2,"March":3,"April":4,
        "May":5,"June":6,"July":7,"August":8,
        "September":9,"October":10,"November":11,"December":12
    }
    month_name = st.selectbox(
        "🗓️ Select Month",
        options = list(month_names.keys()),
        index   = 0
    )
    month = month_names[month_name]

    countries = sorted(country_store_map.keys())
    country   = st.selectbox(
        "🌍 Select Country",
        options = countries
    )

    branches    = country_store_map[country]
    branch_names = [b['Store_Name'] for b in branches]
    branch_name  = st.selectbox(
        "🏪 Select Branch",
        options = branch_names
    )
    store_id = next(
        b['Store_ID'] for b in branches
        if b['Store_Name'] == branch_name
    )

    categories = sorted(monthly_store['category_name'].unique())
    category   = st.selectbox(
        "📦 Select Category",
        options = categories
    )

    st.divider()

    if year <= 2024:
        st.markdown("""
            <div style='background:#1c3a2a; border:1px solid #30d158;
                        border-radius:10px; padding:12px; text-align:center;'>
                <span style='color:#30d158; font-size:20px;'>✅</span><br>
                <span style='color:#30d158; font-weight:bold;'>ACTUAL DATA MODE</span><br>
                <span style='color:#86868b; font-size:12px;'>
                    Showing real sales from dataset
                </span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background:#1a2a3a; border:1px solid #0071e3;
                        border-radius:10px; padding:12px; text-align:center;'>
                <span style='color:#0071e3; font-size:20px;'>🔮</span><br>
                <span style='color:#0071e3; font-weight:bold;'>PREDICTION MODE</span><br>
                <span style='color:#86868b; font-size:12px;'>
                    Showing AI-powered forecasts
                </span>
            </div>
        """, unsafe_allow_html=True)

    st.divider()
    predict_btn = st.button("🚀 Generate Forecast")
    st.divider()

    st.markdown("""
        <div style='text-align:center;'>
            <p style='color:#333333; font-size:12px;'>
                🤖 XGBoost Active<br>
                🌊 Prophet Active<br>
                📊 1M+ transactions trained<br>
                🗓️ 2020–2024 historical data
            </p>
        </div>
    """, unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Demand Prediction",
    "💰 Sales Analytics",
    "📦 Inventory Forecasting",
    "🌊 Seasonal Analysis"
])
#demand prediction
with tab1:
    st.markdown(f"""
        <div style='display:flex; align-items:center; gap:12px; margin-bottom:10px;'>
            <h2 style='color:#1c1c1e; margin:0;'>📈 Demand Prediction</h2>
            <span class='{"badge-actual" if year <= 2024 else "badge-predicted"}'>
                {"✅ ACTUAL DATA" if year <= 2024 else "🔮 AI PREDICTED"}
            </span>
        </div>
        <p style='color:#333333;'>
            {"Real sales data from dataset for" if year <= 2024 else "XGBoost model forecast for"}
            <b style='color:#1c1c1e;'>{month_name} {year}</b> |
            <b style='color:#1c1c1e;'>{branch_name}</b> |
            <b style='color:#1c1c1e;'>{country}</b>
        </p>
    """, unsafe_allow_html=True)

    if predict_btn:
        with st.spinner("⚡ Fetching demand data..."):

            if year <= 2024:
                actual = monthly_store[
                    (monthly_store['year']          == year) &
                    (monthly_store['month']         == month) &
                    (monthly_store['store_id']      == store_id) &
                    (monthly_store['category_name'] == category)
                ]
                if actual.empty:
                    st.warning(f"⚠️ No data found for {month_name} {year} at {branch_name} for {category}")
                else:
                    qty = int(actual['total_quantity'].values[0])
                    rev = int(actual['total_revenue'].values[0])
                    txn = int(actual['num_transactions'].values[0])
                    avg_p = int(actual['avg_price'].values[0])

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("📦 Units Sold",       f"{qty:,}",    "Actual")
                    c2.metric("💰 Revenue",          f"${rev:,}",   "Actual")
                    c3.metric("🧾 Transactions",     f"{txn:,}",    "Actual")
                    c4.metric("💵 Avg Product Price",f"${avg_p:,}", "Actual")

                    st.divider()

                    trend = monthly_store[
                        (monthly_store['store_id']      == store_id) &
                        (monthly_store['category_name'] == category) &
                        (monthly_store['year']          == year)
                    ].sort_values('month')

                    col1, col2 = st.columns(2)

                    with col1:
                        fig1 = px.bar(
                            trend,
                            x='month', y='total_quantity',
                            title=f'📊 Monthly Demand — {category} at {branch_name} ({year})',
                            color='total_quantity',
                            color_continuous_scale='Blues',
                            labels={'month':'Month','total_quantity':'Units Sold'}
                        )
                        fig1.add_vline(
                            x=month, line_dash='dash',
                            line_color='#30d158',
                            annotation_text=f'{month_name} ▼',
                            annotation_font_color='#30d158'
                        )
                        fig1.update_layout(
                            plot_bgcolor='#1c1c1e',
                            paper_bgcolor='#1c1c1e',
                            font_color='#f5f5f7'
                        )
                        st.plotly_chart(fig1, use_container_width=True)

                    with col2:
                        yoy = monthly_store[
                            (monthly_store['store_id']      == store_id) &
                            (monthly_store['category_name'] == category) &
                            (monthly_store['month']         == month)
                        ].sort_values('year')

                        fig2 = px.line(
                            yoy,
                            x='year', y='total_quantity',
                            title=f'📈 YoY Demand — {month_name} at {branch_name}',
                            markers=True,
                            labels={'year':'Year','total_quantity':'Units Sold'}
                        )
                        fig2.update_traces(
                            line_color='#30d158',
                            marker=dict(size=10, color='#30d158')
                        )
                        fig2.update_layout(
                            plot_bgcolor='#1c1c1e',
                            paper_bgcolor='#1c1c1e',
                            font_color='#f5f5f7'
                        )
                        st.plotly_chart(fig2, use_container_width=True)

                    st.markdown("### 🏆 Top Products — Actual Sales")
                    try:
                        overall_top_data = master_df[
                            (master_df['year']       == year) &
                            (master_df['month']      == month) &
                            (master_df['store_id']   == store_id)
                        ].groupby('product_name')['quantity'].sum()
                        
                        if not overall_top_data.empty:
                            overall_top_product = overall_top_data.idxmax()
                            overall_top_qty = int(overall_top_data.max())
                            st.success(f"🌟 **Store-wide Best Seller:** The overall top-selling product across all categories this month was **{overall_top_product}** with **{overall_top_qty:,}** units sold!")
                    except Exception as e:
                        pass
                    top_products = master_df[
                        (master_df['year']       == year) &
                        (master_df['month']      == month) &
                        (master_df['store_id']   == store_id) &
                        (master_df['category_name'] == category)
                    ].groupby('product_name').agg(
                        Units_Sold = ('quantity','sum'),
                        Revenue    = ('revenue','sum')
                    ).sort_values('Units_Sold', ascending=False).head(10).reset_index()

                    top_products['Revenue'] = top_products['Revenue'].apply(lambda x: f"${x:,}")
                    st.dataframe(top_products, use_container_width=True, hide_index=True)
            else:
                pred_qty, pred_rev = predict_future(
                    store_id, category, country, year, month
                )
                last_actual = monthly_store[
                    (monthly_store['store_id']      == store_id) &
                    (monthly_store['category_name'] == category)
                ].sort_values(['year','month']).tail(1)

                last_qty = int(last_actual['total_quantity'].values[0]) if not last_actual.empty else 0
                delta    = pred_qty - last_qty
                delta_pct = (delta / last_qty * 100) if last_qty > 0 else 0
                avg_p    = int(last_actual['avg_price'].values[0]) if not last_actual.empty else 0

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("📦 Predicted Units", f"{pred_qty:,}",
                          f"{delta_pct:+.1f}% vs last actual")
                c2.metric("💰 Predicted Revenue", f"${pred_rev:,}",
                          f"{delta:+,} units vs last")
                c3.metric("💵 Avg Price",         f"${avg_p:,}",  "Based on history")
                c4.metric("🎯 Forecast Engine",    "XGBoost",      "Active")

                st.divider()
                monthly_preds = []
                for m in range(1, 13):
                    q, r = predict_future(store_id, category, country, year, m)
                    monthly_preds.append({
                        'month'     : m,
                        'month_name': list(month_names.keys())[m-1],
                        'pred_qty'  : q,
                        'pred_rev'  : r
                    })
                pred_df = pd.DataFrame(monthly_preds)

                col1, col2 = st.columns(2)

                with col1:
                    fig3 = px.bar(
                        pred_df,
                        x='month', y='pred_qty',
                        title=f'🔮 Predicted Monthly Demand — {category} ({year})',
                        color='pred_qty',
                        color_continuous_scale='Blues',
                        labels={'month':'Month','pred_qty':'Predicted Units'}
                    )
                    fig3.add_vline(
                        x=month, line_dash='dash',
                        line_color='#0071e3',
                        annotation_text=f'{month_name} ▼',
                        annotation_font_color='#0071e3'
                    )
                    fig3.update_xaxes(
                        tickmode='array',
                        tickvals=pred_df['month'],
                        ticktext=pred_df['month_name']
                    )
                    fig3.update_layout(
                        plot_bgcolor='#1c1c1e',
                        paper_bgcolor='#1c1c1e',
                        font_color='#f5f5f7'
                    )
                    st.plotly_chart(fig3, use_container_width=True)

                with col2:
                    hist = monthly_store[
                        (monthly_store['store_id']      == store_id) &
                        (monthly_store['category_name'] == category)
                    ].groupby('year')['total_quantity'].sum().reset_index()

                    fig4 = go.Figure()
                    fig4.add_trace(go.Scatter(
                        x=hist['year'], y=hist['total_quantity'],
                        mode='lines+markers', name='Actual',
                        line=dict(color='#30d158', width=2),
                        marker=dict(size=8)
                    ))
                    fig4.add_trace(go.Scatter(
                        x=[hist['year'].max(), year],
                        y=[hist['total_quantity'].iloc[-1], pred_df['pred_qty'].sum()],
                        mode='lines+markers', name='Predicted',
                        line=dict(color='#0071e3', width=2, dash='dash'),
                        marker=dict(size=8)
                    ))
                    fig4.update_layout(
                        title=f'📈 Actual vs Predicted Trend — {category}',
                        plot_bgcolor='#1c1c1e',
                        paper_bgcolor='#1c1c1e',
                        font_color='#f5f5f7',
                        xaxis_title='Year',
                        yaxis_title='Total Units'
                    )
                    st.plotly_chart(fig4, use_container_width=True)
                st.markdown("### 🔮 Full Year Prediction Table")
                pred_display = pred_df.copy()
                pred_display['pred_rev'] = pred_display['pred_rev'].apply(lambda x: f"${x:,}")
                pred_display['pred_qty'] = pred_display['pred_qty'].apply(lambda x: f"{x:,}")
                pred_display.columns = ['Month No','Month','Predicted Units','Predicted Revenue']
                st.dataframe(pred_display[['Month','Predicted Units','Predicted Revenue']],
                             use_container_width=True, hide_index=True)
    else:
        st.markdown("""
            <div class='custom-info-box'>
                👉 <span>Select your filters from the sidebar and click <b>🚀 Generate Forecast</b></span>
            </div>
            <div class='placeholder-box'>
                <div style='font-size: 48px; margin-bottom: 10px;'>📈</div>
                <div style='font-size: 16px; font-weight: 500;'>Forecast visualisations will appear here after selection</div>
            </div>
        """, unsafe_allow_html=True)

#sales analytics
with tab2:
    st.markdown(f"""
        <div style='display:flex; align-items:center; gap:12px; margin-bottom:10px;'>
            <h2 style='color:#1c1c1e; margin:0;'>💰 Sales Analytics</h2>
            <span class='{"badge-actual" if year <= 2024 else "badge-predicted"}'>
                {"✅ ACTUAL DATA" if year <= 2024 else "🔮 AI PREDICTED"}
            </span>
        </div>
        <p style='color:#333333;'>
            Revenue breakdown for
            <b style='color:#1c1c1e;'>{month_name} {year}</b> |
            <b style='color:#1c1c1e;'>{branch_name}</b> |
            <b style='color:#1c1c1e;'>{country}</b>
        </p>
    """, unsafe_allow_html=True)

    if predict_btn:
        with st.spinner("💰 Fetching sales analytics..."):

            if year <= 2024:
                store_month = monthly_store[
                    (monthly_store['store_id'] == store_id) &
                    (monthly_store['year']     == year) &
                    (monthly_store['month']    == month)
                ]

                if store_month.empty:
                    st.warning(f"⚠️ No sales data for {month_name} {year} at {branch_name}")
                else:
                    total_qty = int(store_month['total_quantity'].sum())
                    total_rev = int(store_month['total_revenue'].sum())
                    total_txn = int(store_month['num_transactions'].sum())
                    best_cat  = store_month.loc[store_month['total_revenue'].idxmax(), 'category_name']
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("💰 Total Revenue",    f"${total_rev:,}")
                    c2.metric("📦 Total Units",      f"{total_qty:,}")
                    c3.metric("🧾 Transactions",     f"{total_txn:,}")
                    c4.metric("🏆 Best Category",    best_cat)

                    st.divider()
                    col1, col2 = st.columns(2)
                    with col1:
                        fig1 = px.bar(
                            store_month.sort_values('total_revenue', ascending=True),
                            x='total_revenue', y='category_name',
                            orientation='h',
                            title=f'💰 Revenue by Category — {branch_name} ({month_name} {year})',
                            color='total_revenue',
                            color_continuous_scale='Blues',
                            labels={'total_revenue':'Revenue','category_name':'Category'},
                            text=store_month.sort_values('total_revenue',ascending=True)['total_revenue'].apply(lambda x: f"${x:,}")
                        )
                        fig1.update_traces(textposition='outside')
                        fig1.update_layout(
                            plot_bgcolor='#1c1c1e',
                            paper_bgcolor='#1c1c1e',
                            font_color='#f5f5f7'
                        )
                        st.plotly_chart(fig1, use_container_width=True)

                    with col2:
                        fig2 = px.pie(
                            store_month,
                            names='category_name',
                            values='total_revenue',
                            title=f'📊 Revenue Share by Category',
                            hole=0.4,
                            color_discrete_sequence=px.colors.sequential.Blues_r
                        )
                        fig2.update_layout(
                            plot_bgcolor='#1c1c1e',
                            paper_bgcolor='#1c1c1e',
                            font_color='#f5f5f7'
                        )
                        st.plotly_chart(fig2, use_container_width=True)

                    st.markdown("### 📈 Monthly Revenue Trend")
                    monthly_rev = monthly_store[
                        (monthly_store['store_id'] == store_id) &
                        (monthly_store['year']     == year)
                    ].groupby('month').agg(
                        total_revenue = ('total_revenue','sum'),
                        total_quantity= ('total_quantity','sum')
                    ).reset_index()

                    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
                    fig3.add_trace(
                        go.Bar(
                            x=monthly_rev['month'],
                            y=monthly_rev['total_revenue'],
                            name='Revenue',
                            marker_color='#0071e3',
                            opacity=0.8
                        ), secondary_y=False
                    )
                    fig3.add_trace(
                        go.Scatter(
                            x=monthly_rev['month'],
                            y=monthly_rev['total_quantity'],
                            name='Units Sold',
                            mode='lines+markers',
                            line=dict(color='#30d158', width=2),
                            marker=dict(size=8)
                        ), secondary_y=True
                    )
                    fig3.update_layout(
                        title=f'📈 Revenue & Units — {branch_name} ({year})',
                        plot_bgcolor='#1c1c1e',
                        paper_bgcolor='#1c1c1e',
                        font_color='#f5f5f7',
                        xaxis_title='Month'
                    )
                    fig3.update_yaxes(title_text="Revenue ($)", secondary_y=False)
                    fig3.update_yaxes(title_text="Units Sold", secondary_y=True)
                    st.plotly_chart(fig3, use_container_width=True)

                    st.markdown("### 🏆 Top 10 Products by Revenue")
                    top_rev = master_df[
                        (master_df['year']     == year) &
                        (master_df['month']    == month) &
                        (master_df['store_id'] == store_id)
                    ].groupby(['product_name','category_name']).agg(
                        Units    = ('quantity','sum'),
                        Revenue  = ('revenue', 'sum'),
                        Avg_Price= ('price',   'mean')
                    ).sort_values('Revenue', ascending=False).head(10).reset_index()

                    top_rev['Revenue']   = top_rev['Revenue'].apply(lambda x: f"${x:,}")
                    top_rev['Avg_Price'] = top_rev['Avg_Price'].apply(lambda x: f"${x:,.0f}")
                    st.dataframe(top_rev, use_container_width=True, hide_index=True)

            else:
                all_cat_preds = []
                for cat in categories:
                    q, r = predict_future(store_id, cat, country, year, month)
                    all_cat_preds.append({
                        'category_name'  : cat,
                        'pred_qty'       : q,
                        'pred_revenue'   : r
                    })
                pred_cat_df = pd.DataFrame(all_cat_preds)
                pred_cat_df = pred_cat_df[pred_cat_df['pred_qty'] > 0]

                total_pred_qty = pred_cat_df['pred_qty'].sum()
                total_pred_rev = pred_cat_df['pred_revenue'].sum()
                best_pred_cat  = pred_cat_df.loc[pred_cat_df['pred_revenue'].idxmax(), 'category_name']

                # KPI Cards
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("💰 Predicted Revenue", f"${total_pred_rev:,}")
                c2.metric("📦 Predicted Units",   f"{total_pred_qty:,}")
                c3.metric("🏆 Top Category",      best_pred_cat)
                c4.metric("🎯 Forecast Engine",    "XGBoost")

                st.divider()

                col1, col2 = st.columns(2)

                with col1:
                    fig4 = px.bar(
                        pred_cat_df.sort_values('pred_revenue', ascending=True),
                        x='pred_revenue', y='category_name',
                        orientation='h',
                        title=f'🔮 Predicted Revenue by Category ({month_name} {year})',
                        color='pred_revenue',
                        color_continuous_scale='Blues',
                        labels={'pred_revenue':'Predicted Revenue','category_name':'Category'},
                        text=pred_cat_df.sort_values('pred_revenue',ascending=True)['pred_revenue'].apply(lambda x: f"${x:,}")
                    )
                    fig4.update_traces(textposition='outside')
                    fig4.update_layout(
                        plot_bgcolor='#1c1c1e',
                        paper_bgcolor='#1c1c1e',
                        font_color='#f5f5f7'
                    )
                    st.plotly_chart(fig4, use_container_width=True)

                with col2:
                    fig5 = px.pie(
                        pred_cat_df,
                        names='category_name',
                        values='pred_revenue',
                        title='📊 Predicted Revenue Share',
                        hole=0.4,
                        color_discrete_sequence=px.colors.sequential.Blues_r
                    )
                    fig5.update_layout(
                        plot_bgcolor='#1c1c1e',
                        paper_bgcolor='#1c1c1e',
                        font_color='#f5f5f7'
                    )
                    st.plotly_chart(fig5, use_container_width=True)

                st.markdown("### 🔮 Full Year Predicted Revenue")
                yearly_pred = []
                for m in range(1, 13):
                    month_total_rev = 0
                    month_total_qty = 0
                    for cat in categories:
                        q, r = predict_future(store_id, cat, country, year, m)
                        month_total_rev += r
                        month_total_qty += q
                    yearly_pred.append({
                        'Month'            : list(month_names.keys())[m-1],
                        'Predicted Units'  : f"{month_total_qty:,}",
                        'Predicted Revenue': f"${month_total_rev:,}"
                    })
                st.dataframe(pd.DataFrame(yearly_pred),
                             use_container_width=True, hide_index=True)
    else:
        st.markdown("""
            <div class='custom-info-box'>
                👉 <span>Select your filters from the sidebar and click <b>🚀 Generate Forecast</b></span>
            </div>
            <div class='placeholder-box'>
                <div style='font-size: 48px; margin-bottom: 10px;'>📈</div>
                <div style='font-size: 16px; font-weight: 500;'>Forecast visualisations will appear here after selection</div>
            </div>
        """, unsafe_allow_html=True)

#inveentory forecasting
with tab3:
    st.markdown(f"""
        <div style='display:flex; align-items:center; gap:12px; margin-bottom:10px;'>
            <h2 style='color:#1c1c1e; margin:0;'>📦 Inventory Forecasting</h2>
            <span class='{"badge-actual" if year <= 2024 else "badge-predicted"}'>
                {"✅ ACTUAL DATA" if year <= 2024 else "🔮 AI PREDICTED"}
            </span>
        </div>
        <p style='color:#333333;'>
            Stock recommendations for
            <b style='color:#1c1c1e;'>{month_name} {year}</b> |
            <b style='color:#1c1c1e;'>{branch_name}</b> |
            <b style='color:#1c1c1e;'>{country}</b>
        </p>
    """, unsafe_allow_html=True)

    if predict_btn:
        with st.spinner("📦 Calculating inventory levels..."):
            SAFETY_HIGH   = 2.0
            SAFETY_MEDIUM = 1.5
            SAFETY_LOW    = 1.2

            def get_urgency(qty):
                if qty >= 300:
                    return "🔴 High", SAFETY_HIGH
                elif qty >= 100:
                    return "🟡 Medium", SAFETY_MEDIUM
                else:
                    return "🟢 Low", SAFETY_LOW

            if year <= 2024:
                store_month_inv = monthly_store[
                    (monthly_store['store_id'] == store_id) &
                    (monthly_store['year']     == year) &
                    (monthly_store['month']    == month)
                ].copy()

                if store_month_inv.empty:
                    st.warning(f"⚠️ No data for {month_name} {year} at {branch_name}")
                else:
                    inv_rows = []
                    for _, row in store_month_inv.iterrows():
                        qty            = int(row['total_quantity'])
                        urgency, mult  = get_urgency(qty)
                        recommended    = int(qty * mult)
                        buffer         = recommended - qty
                        inv_rows.append({
                            'Category'           : row['category_name'],
                            'Actual Sold'        : qty,
                            'Safety Multiplier'  : f"{mult}x",
                            'Recommended Stock'  : recommended,
                            'Buffer Stock'       : buffer,
                            'Urgency'            : urgency
                        })

                    inv_df = pd.DataFrame(inv_rows).sort_values(
                        'Actual Sold', ascending=False
                    )
                    total_sold  = inv_df['Actual Sold'].sum()
                    total_stock = inv_df['Recommended Stock'].sum()
                    high_risk   = len(inv_df[inv_df['Urgency'].str.contains('High')])
                    low_risk    = len(inv_df[inv_df['Urgency'].str.contains('Low')])

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("📦 Total Units Sold",      f"{total_sold:,}")
                    c2.metric("🏭 Total Stock Needed",    f"{total_stock:,}")
                    c3.metric("🔴 High Urgency Items",    f"{high_risk}")
                    c4.metric("🟢 Low Urgency Items",     f"{low_risk}")

                    st.divider()
                    st.markdown("### 📋 Inventory Recommendation Table")
                    st.dataframe(inv_df, use_container_width=True, hide_index=True)

                    st.divider()

                    col1, col2 = st.columns(2)

                    with col1:
                        fig1 = go.Figure()
                        fig1.add_trace(go.Bar(
                            name='Actual Sold',
                            x=inv_df['Category'],
                            y=inv_df['Actual Sold'],
                            marker_color='#30d158'
                        ))
                        fig1.add_trace(go.Bar(
                            name='Recommended Stock',
                            x=inv_df['Category'],
                            y=inv_df['Recommended Stock'],
                            marker_color='#0071e3'
                        ))
                        fig1.update_layout(
                            barmode='group',
                            title=f'📦 Actual Sold vs Recommended Stock ({month_name} {year})',
                            plot_bgcolor='#1c1c1e',
                            paper_bgcolor='#1c1c1e',
                            font_color='#f5f5f7',
                            xaxis_title='Category',
                            yaxis_title='Units'
                        )
                        st.plotly_chart(fig1, use_container_width=True)

                    with col2:
                        fig2 = px.bar(
                            inv_df.sort_values('Buffer Stock', ascending=True),
                            x='Buffer Stock', y='Category',
                            orientation='h',
                            title='🛡️ Buffer Stock Required per Category',
                            color='Buffer Stock',
                            color_continuous_scale='Reds',
                            text=inv_df.sort_values('Buffer Stock',ascending=True)['Buffer Stock'].apply(lambda x: f"{x:,}")
                        )
                        fig2.update_traces(textposition='outside')
                        fig2.update_layout(
                            plot_bgcolor='#1c1c1e',
                            paper_bgcolor='#1c1c1e',
                            font_color='#f5f5f7'
                        )
                        st.plotly_chart(fig2, use_container_width=True)

                    st.markdown("### 📈 Historical Stock Consumption Pattern")
                    hist_inv = monthly_store[
                        (monthly_store['store_id']      == store_id) &
                        (monthly_store['category_name'] == category)
                    ].sort_values(['year','month'])

                    hist_inv['recommended'] = hist_inv['total_quantity'].apply(
                        lambda x: int(x * get_urgency(x)[1])
                    )

                    fig3 = go.Figure()
                    fig3.add_trace(go.Scatter(
                        x=hist_inv.apply(lambda r: f"{int(r['year'])}-{int(r['month']):02d}", axis=1),
                        y=hist_inv['total_quantity'],
                        name='Actual Sold',
                        mode='lines+markers',
                        line=dict(color='#30d158', width=2)
                    ))
                    fig3.add_trace(go.Scatter(
                        x=hist_inv.apply(lambda r: f"{int(r['year'])}-{int(r['month']):02d}", axis=1),
                        y=hist_inv['recommended'],
                        name='Recommended Stock',
                        mode='lines',
                        line=dict(color='#0071e3', width=2, dash='dash')
                    ))
                    fig3.update_layout(
                        title=f'📈 Stock Consumption History — {category} at {branch_name}',
                        plot_bgcolor='#1c1c1e',
                        paper_bgcolor='#1c1c1e',
                        font_color='#f5f5f7',
                        xaxis_title='Year-Month',
                        yaxis_title='Units',
                        xaxis_tickangle=45
                    )
                    st.plotly_chart(fig3, use_container_width=True)

            else:
                pred_inv_rows = []
                for cat in categories:
                    pred_qty, pred_rev = predict_future(
                        store_id, cat, country, year, month
                    )
                    if pred_qty > 0:
                        urgency, mult  = get_urgency(pred_qty)
                        recommended    = int(pred_qty * mult)
                        buffer         = recommended - pred_qty
                        pred_inv_rows.append({
                            'Category'          : cat,
                            'Predicted Sales'   : pred_qty,
                            'Safety Multiplier' : f"{mult}x",
                            'Stock to Keep'     : recommended,
                            'Buffer Stock'      : buffer,
                            'Urgency'           : urgency
                        })

                pred_inv_df = pd.DataFrame(pred_inv_rows).sort_values(
                    'Predicted Sales', ascending=False
                )

                total_pred  = pred_inv_df['Predicted Sales'].sum()
                total_stock = pred_inv_df['Stock to Keep'].sum()
                high_risk   = len(pred_inv_df[pred_inv_df['Urgency'].str.contains('High')])
                low_risk    = len(pred_inv_df[pred_inv_df['Urgency'].str.contains('Low')])

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("🔮 Predicted Sales",     f"{total_pred:,}")
                c2.metric("🏭 Total Stock Needed",  f"{total_stock:,}")
                c3.metric("🔴 High Urgency Items",  f"{high_risk}")
                c4.metric("🟢 Low Urgency Items",   f"{low_risk}")

                st.divider()
                st.markdown("### 📋 Predicted Inventory Table")
                st.dataframe(pred_inv_df, use_container_width=True, hide_index=True)

                st.divider()

                col1, col2 = st.columns(2)

                with col1:
                    fig4 = go.Figure()
                    fig4.add_trace(go.Bar(
                        name='Predicted Sales',
                        x=pred_inv_df['Category'],
                        y=pred_inv_df['Predicted Sales'],
                        marker_color='#0071e3'
                    ))
                    fig4.add_trace(go.Bar(
                        name='Stock to Keep',
                        x=pred_inv_df['Category'],
                        y=pred_inv_df['Stock to Keep'],
                        marker_color='#ff9f0a'
                    ))
                    fig4.update_layout(
                        barmode='group',
                        title=f'📦 Predicted Sales vs Stock to Keep ({month_name} {year})',
                        plot_bgcolor='#1c1c1e',
                        paper_bgcolor='#1c1c1e',
                        font_color='#f5f5f7',
                        xaxis_title='Category',
                        yaxis_title='Units'
                    )
                    st.plotly_chart(fig4, use_container_width=True)

                with col2:
                    urgency_counts = pred_inv_df['Urgency'].value_counts().reset_index()
                    urgency_counts.columns = ['Urgency','Count']
                    fig5 = px.pie(
                        urgency_counts,
                        names='Urgency',
                        values='Count',
                        title='🚦 Urgency Distribution',
                        hole=0.4,
                        color_discrete_map={
                            '🔴 High'  : '#ff453a',
                            '🟡 Medium': '#ffd60a',
                            '🟢 Low'   : '#30d158'
                        }
                    )
                    fig5.update_layout(
                        plot_bgcolor='#1c1c1e',
                        paper_bgcolor='#1c1c1e',
                        font_color='#f5f5f7'
                    )
                    st.plotly_chart(fig5, use_container_width=True)
                st.markdown("### 📅 12-Month Inventory Plan")
                yearly_inv = []
                for m in range(1, 13):
                    m_qty, _ = predict_future(store_id, category, country, year, m)
                    urgency, mult = get_urgency(m_qty)
                    yearly_inv.append({
                        'Month'          : list(month_names.keys())[m-1],
                        'Predicted Sales': f"{m_qty:,}",
                        'Stock to Keep'  : f"{int(m_qty * mult):,}",
                        'Urgency'        : urgency
                    })
                st.dataframe(pd.DataFrame(yearly_inv),
                             use_container_width=True, hide_index=True)
    else:
        st.markdown("""
            <div class='custom-info-box'>
                👉 <span>Select your filters from the sidebar and click <b>🚀 Generate Forecast</b></span>
            </div>
            <div class='placeholder-box'>
                <div style='font-size: 48px; margin-bottom: 10px;'>📈</div>
                <div style='font-size: 16px; font-weight: 500;'>Forecast visualisations will appear here after selection</div>
            </div>
        """, unsafe_allow_html=True)

#seasonal analysis
with tab4:
    st.markdown(f"""
        <div style='display:flex; align-items:center; gap:12px; margin-bottom:10px;'>
            <h2 style='color:#1c1c1e; margin:0;'>🌊 Seasonal Analysis</h2>
            <span class='{"badge-actual" if year <= 2024 else "badge-predicted"}'>
                {"✅ ACTUAL DATA" if year <= 2024 else "🔮 PROPHET FORECAST"}
            </span>
        </div>
        <p style='color:#333333;'>
            Seasonal patterns for
            <b style='color:#1c1c1e;'>{country}</b> |
            <b style='color:#1c1c1e;'>{branch_name}</b> |
            <b style='color:#1c1c1e;'>Full Year {year}</b>
        </p>
    """, unsafe_allow_html=True)

    if predict_btn:
        with st.spinner("🌊 Analyzing seasonal patterns..."):

            month_labels = ['Jan','Feb','Mar','Apr','May','Jun',
                            'Jul','Aug','Sep','Oct','Nov','Dec']

            if year <= 2024:
                store_year = monthly_store[
                    (monthly_store['store_id'] == store_id) &
                    (monthly_store['year']     == year)
                ].groupby('month').agg(
                    total_quantity = ('total_quantity','sum'),
                    total_revenue  = ('total_revenue', 'sum')
                ).reset_index()

                if store_year.empty:
                    st.warning(f"⚠️ No data for {year} at {branch_name}")
                else:
                    peak_month  = store_year.loc[store_year['total_quantity'].idxmax(), 'month']
                    dip_month   = store_year.loc[store_year['total_quantity'].idxmin(), 'month']
                    peak_qty    = int(store_year['total_quantity'].max())
                    dip_qty     = int(store_year['total_quantity'].min())
                    total_qty   = int(store_year['total_quantity'].sum())
                    total_rev   = int(store_year['total_revenue'].sum())
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("📅 Peak Month",    month_labels[peak_month-1], f"{peak_qty:,} units")
                    c2.metric("❄️ Dip Month",     month_labels[dip_month-1],  f"{dip_qty:,} units")
                    c3.metric("📦 Total Units",   f"{total_qty:,}")
                    c4.metric("💰 Total Revenue", f"${total_rev:,}")

                    st.divider()
                    def season_tag(m):
                        if m in [12, 1, 2]: return "❄️ Winter"
                        elif m in [3, 4, 5]: return "🌱 Spring"
                        elif m in [6, 7, 8]: return "☀️ Summer"
                        else: return "🍂 Autumn"

                    def apple_event(m):
                        if m == 9:  return "📱 iPhone Launch"
                        elif m == 11: return "🛍️ Black Friday"
                        elif m == 12: return "🎄 Holiday Season"
                        elif m == 8:  return "🎒 Back to School"
                        else: return ""

                    store_year['season']      = store_year['month'].apply(season_tag)
                    store_year['apple_event'] = store_year['month'].apply(apple_event)
                    store_year['month_name']  = store_year['month'].apply(
                        lambda x: month_labels[x-1]
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        season_colors = {
                            '❄️ Winter': '#636EFA',
                            '🌱 Spring': '#00CC96',
                            '☀️ Summer': '#FFA15A',
                            '🍂 Autumn': '#EF553B'
                        }
                        fig1 = px.bar(
                            store_year,
                            x='month_name', y='total_quantity',
                            color='season',
                            color_discrete_map=season_colors,
                            title=f'🌊 Monthly Sales by Season — {branch_name} ({year})',
                            labels={'month_name':'Month','total_quantity':'Units Sold'},
                            text='total_quantity'
                        )
                        fig1.update_traces(textposition='outside')
                        fig1.update_layout(
                            plot_bgcolor='#1c1c1e',
                            paper_bgcolor='#1c1c1e',
                            font_color='#f5f5f7'
                        )
                        st.plotly_chart(fig1, use_container_width=True)

                    with col2:
                        season_rev = store_year.groupby('season')['total_revenue'].sum().reset_index()
                        fig2 = px.pie(
                            season_rev,
                            names='season',
                            values='total_revenue',
                            title='💰 Revenue Share by Season',
                            hole=0.4,
                            color='season',
                            color_discrete_map=season_colors
                        )
                        fig2.update_layout(
                            plot_bgcolor='#1c1c1e',
                            paper_bgcolor='#1c1c1e',
                            font_color='#f5f5f7'
                        )
                        st.plotly_chart(fig2, use_container_width=True)

                    st.markdown("### 🗓️ Year-over-Year Heatmap")
                    heatmap_data = monthly_store[
                        monthly_store['store_id'] == store_id
                    ].groupby(['year','month'])['total_quantity'].sum().reset_index()

                    heatmap_pivot = heatmap_data.pivot(
                        index='year', columns='month', values='total_quantity'
                    ).fillna(0)
                    heatmap_pivot.columns = month_labels

                    fig3 = px.imshow(
                        heatmap_pivot,
                        title=f'🗓️ Sales Heatmap — {branch_name} (All Years)',
                        color_continuous_scale='Blues',
                        labels=dict(x='Month', y='Year', color='Units Sold'),
                        aspect='auto'
                    )
                    fig3.update_layout(
                        plot_bgcolor='#1c1c1e',
                        paper_bgcolor='#1c1c1e',
                        font_color='#f5f5f7'
                    )
                    st.plotly_chart(fig3, use_container_width=True)

                    st.markdown("### 📊 Quarter-wise Performance")
                    store_year['quarter'] = store_year['month'].apply(
                        lambda x: f"Q{(x-1)//3+1}"
                    )
                    qtr = store_year.groupby('quarter').agg(
                        Units   = ('total_quantity','sum'),
                        Revenue = ('total_revenue', 'sum')
                    ).reset_index()

                    col3, col4 = st.columns(2)
                    with col3:
                        fig4 = px.bar(
                            qtr, x='quarter', y='Units',
                            title='📊 Units by Quarter',
                            color='Units',
                            color_continuous_scale='Blues',
                            text='Units'
                        )
                        fig4.update_traces(textposition='outside')
                        fig4.update_layout(
                            plot_bgcolor='#1c1c1e',
                            paper_bgcolor='#1c1c1e',
                            font_color='#f5f5f7'
                        )
                        st.plotly_chart(fig4, use_container_width=True)

                    with col4:
                        fig5 = px.bar(
                            qtr, x='quarter', y='Revenue',
                            title='💰 Revenue by Quarter',
                            color='Revenue',
                            color_continuous_scale='Blues',
                            text=qtr['Revenue'].apply(lambda x: f"${x:,}")
                        )
                        fig5.update_traces(textposition='outside')
                        fig5.update_layout(
                            plot_bgcolor='#1c1c1e',
                            paper_bgcolor='#1c1c1e',
                            font_color='#f5f5f7'
                        )
                        st.plotly_chart(fig5, use_container_width=True)

                    st.markdown("### 📋 Monthly Seasonal Summary")
                    summary = store_year[[
                        'month_name','total_quantity',
                        'total_revenue','season','apple_event'
                    ]].copy()
                    summary['total_revenue'] = summary['total_revenue'].apply(lambda x: f"${x:,}")
                    summary['total_quantity'] = summary['total_quantity'].apply(lambda x: f"{x:,}")
                    summary.columns = ['Month','Units Sold','Revenue','Season','Apple Event']
                    st.dataframe(summary, use_container_width=True, hide_index=True)

            else:
                if 'country' in prophet_forecast.columns:
                    forecast_year = prophet_forecast[
                        (prophet_forecast['ds'].dt.year == year) &
                        (prophet_forecast['country'] == country)
                    ].copy()
                else:
                    forecast_year = prophet_forecast[
                        prophet_forecast['ds'].dt.year == year
                    ].copy()

                forecast_year['month']      = forecast_year['ds'].dt.month
                forecast_year['month_name'] = forecast_year['month'].apply(
                    lambda x: month_labels[x-1]
                )
                forecast_year['yhat']       = forecast_year['yhat'].clip(lower=0).astype(int)
                forecast_year['yhat_lower'] = forecast_year['yhat_lower'].clip(lower=0).astype(int)
                forecast_year['yhat_upper'] = forecast_year['yhat_upper'].clip(lower=0).astype(int)

                if forecast_year.empty:
                    st.warning(f"⚠️ No Prophet forecast available for {year}")
                else:
                    peak_idx  = forecast_year['yhat'].idxmax()
                    dip_idx   = forecast_year['yhat'].idxmin()
                    peak_m    = forecast_year.loc[peak_idx, 'month_name']
                    dip_m     = forecast_year.loc[dip_idx,  'month_name']
                    total_pred= int(forecast_year['yhat'].sum())

                    # Compare with last actual year
                    if 'country' in prophet_forecast.columns:
                        last_actual_total = monthly_store[
                            (monthly_store['year'] == 2024) &
                            (monthly_store['country'] == country)
                        ]['total_quantity'].sum()
                    else:
                        last_actual_total = monthly_store[
                            monthly_store['year'] == 2024
                        ]['total_quantity'].sum()
                    growth = ((total_pred - last_actual_total) / last_actual_total * 100)

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("📅 Peak Month",      peak_m)
                    c2.metric("❄️ Dip Month",       dip_m)
                    c3.metric("📦 Total Predicted", f"{total_pred:,}")
                    c4.metric("📈 vs 2024",         f"{growth:+.1f}%")

                    st.divider()
                    col1, col2 = st.columns(2)

                    with col1:
                        fig6 = go.Figure()
                        fig6.add_trace(go.Scatter(
                            x=forecast_year['month_name'],
                            y=forecast_year['yhat_upper'],
                            mode='lines',
                            line=dict(width=0),
                            showlegend=False,
                            name='Upper Bound'
                        ))
                        fig6.add_trace(go.Scatter(
                            x=forecast_year['month_name'],
                            y=forecast_year['yhat_lower'],
                            fill='tonexty',
                            fillcolor='rgba(0,113,227,0.15)',
                            line=dict(width=0),
                            name='Confidence Interval'
                        ))
                        fig6.add_trace(go.Scatter(
                            x=forecast_year['month_name'],
                            y=forecast_year['yhat'],
                            mode='lines+markers',
                            name='Forecast',
                            line=dict(color='#0071e3', width=3),
                            marker=dict(size=10)
                        ))
                        fig6.update_layout(
                            title=f'🌊 Prophet Seasonal Forecast — {year}',
                            plot_bgcolor='#1c1c1e',
                            paper_bgcolor='#1c1c1e',
                            font_color='#f5f5f7',
                            xaxis_title='Month',
                            yaxis_title='Predicted Units'
                        )
                        st.plotly_chart(fig6, use_container_width=True)

                    with col2:
                        actual_2024 = monthly_store[
                            monthly_store['year'] == 2024
                        ].groupby('month')['total_quantity'].sum().reset_index()

                        fig7 = go.Figure()
                        fig7.add_trace(go.Scatter(
                            x=[month_labels[m-1] for m in actual_2024['month']],
                            y=actual_2024['total_quantity'],
                            mode='lines+markers',
                            name='2024 Actual',
                            line=dict(color='#30d158', width=2),
                            marker=dict(size=8)
                        ))
                        fig7.add_trace(go.Scatter(
                            x=forecast_year['month_name'],
                            y=forecast_year['yhat'],
                            mode='lines+markers',
                            name=f'{year} Forecast',
                            line=dict(color='#0071e3', width=2, dash='dash'),
                            marker=dict(size=8)
                        ))
                        fig7.update_layout(
                            title=f'📊 2024 Actual vs {year} Forecast',
                            plot_bgcolor='#1c1c1e',
                            paper_bgcolor='#1c1c1e',
                            font_color='#f5f5f7',
                            xaxis_title='Month',
                            yaxis_title='Units'
                        )
                        st.plotly_chart(fig7, use_container_width=True)

                    st.markdown(f"### 📋 {year} Monthly Forecast Table")
                    forecast_display = forecast_year[[
                        'month_name','yhat','yhat_lower','yhat_upper'
                    ]].copy()
                    forecast_display.columns = [
                        'Month','Predicted Units','Lower Bound','Upper Bound'
                    ]
                    st.dataframe(forecast_display,
                                 use_container_width=True, hide_index=True)

                    st.markdown("### 📈 Full Timeline: Actual + Forecast")
                    if 'country' in prophet_forecast.columns:
                        hist_all = monthly_store[
                            monthly_store['country'] == country
                        ].groupby(['year','month'])['total_quantity'].sum().reset_index()
                    else:
                        hist_all = monthly_store.groupby(
                            ['year','month'])['total_quantity'].sum().reset_index()
                    hist_all['date'] = pd.to_datetime(
                        hist_all['year'].astype(str) + '-' +
                        hist_all['month'].astype(str) + '-01'
                    )

                    fig8 = go.Figure()
                    fig8.add_trace(go.Scatter(
                        x=hist_all['date'],
                        y=hist_all['total_quantity'],
                        mode='lines',
                        name='Actual (2020-2024)',
                        line=dict(color='#30d158', width=2)
                    ))
                    if 'country' in prophet_forecast.columns:
                        future_fc = prophet_forecast[
                            (prophet_forecast['ds'].dt.year >= 2025) &
                            (prophet_forecast['country'] == country)
                        ]
                    else:
                        future_fc = prophet_forecast[
                            prophet_forecast['ds'].dt.year >= 2025
                        ]
                    fig8.add_trace(go.Scatter(
                        x=future_fc['ds'],
                        y=future_fc['yhat'].clip(lower=0),
                        mode='lines',
                        name='Prophet Forecast',
                        line=dict(color='#0071e3', width=2, dash='dash')
                    ))
                    fig8.add_trace(go.Scatter(
                        x=pd.concat([future_fc['ds'], future_fc['ds'][::-1]]),
                        y=pd.concat([
                            future_fc['yhat_upper'].clip(lower=0),
                            future_fc['yhat_lower'].clip(lower=0)[::-1]
                        ]),
                        fill='toself',
                        fillcolor='rgba(0,113,227,0.1)',
                        line=dict(color='rgba(255,255,255,0)'),
                        name='Confidence Interval'
                    ))
                    fig8.update_layout(
                        title='📈 Complete Sales Timeline + Prophet Forecast',
                        plot_bgcolor='#1c1c1e',
                        paper_bgcolor='#1c1c1e',
                        font_color='#f5f5f7',
                        xaxis_title='Date',
                        yaxis_title='Total Units'
                    )
                    st.plotly_chart(fig8, use_container_width=True)
    else:
        st.info("👈 Select your filters from the sidebar and click **🚀 Generate Forecast**")

gc.collect()
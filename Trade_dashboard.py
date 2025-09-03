import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

# --- COMMODITY CONFIGURATION ---
# A dictionary to hold all commodity-specific data and conversion logic.
COMMODITY_DATA = {
    'Coffee': {
        'ticker': 'KC=F',
        'price_unit': 'pound',
        'conversion_to_tonne': 2204.62, # pounds per tonne
        'logistics_data': {
            'Country': ['Germany', 'USA', 'Italy', 'Japan', 'France', 'Canada', 'Netherlands', 'South Korea', 'Spain', 'UK'],
            'Shipping_Cost_per_Tonne_INR': [8200, 10000, 8500, 7000, 8300, 10500, 8100, 7200, 8800, 8000],
            'Tariff_Percentage': [0.07, 0.0, 0.05, 0.08, 0.07, 0.0, 0.07, 0.02, 0.07, 0.0],
            'Political_Risk_Score': [0.2, 0.2, 0.3, 0.1, 0.2, 0.2, 0.2, 0.3, 0.3, 0.2]
        }
    },
    'Wheat': {
        'ticker': 'ZW=F',
        'price_unit': 'bushel',
        'conversion_to_tonne': 1 / 0.0272155, # bushels per tonne
        'is_in_cents': True, # Price is given in cents
        'logistics_data': {
            'Country': ['Egypt', 'Indonesia', 'Turkey', 'Brazil', 'Philippines', 'Nigeria', 'Bangladesh', 'Algeria', 'Mexico', 'Japan'],
            'Shipping_Cost_per_Tonne_INR': [4000, 5500, 4200, 9500, 5800, 6500, 5000, 4500, 11000, 7000],
            'Tariff_Percentage': [0.10, 0.05, 0.12, 0.20, 0.07, 0.15, 0.08, 0.06, 0.18, 0.12],
            'Political_Risk_Score': [0.6, 0.4, 0.5, 0.7, 0.4, 0.8, 0.5, 0.6, 0.4, 0.1]
        }
    },
    'Corn': {
        'ticker': 'ZC=F',
        'price_unit': 'bushel',
        'conversion_to_tonne': 1 / 0.0254, # bushels per tonne
        'is_in_cents': True,
        'logistics_data': {
            'Country': ['Mexico', 'Japan', 'EU', 'Egypt', 'South Korea', 'Vietnam', 'Colombia', 'Taiwan', 'Iran', 'Saudi Arabia'],
            'Shipping_Cost_per_Tonne_INR': [11000, 7000, 8000, 4000, 7200, 6000, 12000, 6800, 3800, 3500],
            'Tariff_Percentage': [0.0, 0.12, 0.09, 0.10, 0.02, 0.07, 0.15, 0.06, 0.10, 0.05],
            'Political_Risk_Score': [0.4, 0.1, 0.2, 0.6, 0.3, 0.4, 0.6, 0.3, 0.8, 0.3]
        }
    },
    'Crude Oil': {
        'ticker': 'CL=F',
        'price_unit': 'barrel',
        'conversion_to_tonne': 7.33, # barrels per tonne
        'logistics_data': {
            'Country': ['China', 'USA', 'India', 'Japan', 'South Korea', 'Germany', 'Netherlands', 'Spain', 'Italy', 'Singapore'],
            'Shipping_Cost_per_Tonne_INR': [3000, 9000, 2000, 3200, 3100, 4500, 4400, 4800, 4600, 3500],
            'Tariff_Percentage': [0.05, 0.08, 0.03, 0.06, 0.02, 0.09, 0.09, 0.09, 0.09, 0.0],
            'Political_Risk_Score': [0.5, 0.2, 0.4, 0.1, 0.3, 0.2, 0.2, 0.3, 0.3, 0.1]
        }
    }
}


@st.cache_data(ttl=3600)
def get_real_time_market_data(commodity_name):
    """
    Fetches real-time market data for a selected commodity.
    """
    try:
        config = COMMODITY_DATA[commodity_name]
        
        # --- 1. Fetch Live Financial Data ---
        inr_ticker = yf.Ticker("INR=X")
        usd_to_inr = inr_ticker.history(period="1d")['Close'].iloc[-1]

        commodity_ticker = yf.Ticker(config['ticker'])
        price_per_unit = commodity_ticker.history(period="1d")['Close'].iloc[-1]

        # --- 2. Data Conversion for Analysis ---
        if config.get('is_in_cents', False):
            price_per_unit /= 100 # Convert from cents to dollars

        price_per_tonne_usd = price_per_unit * config['conversion_to_tonne']

        # --- 3. Logistics & Risk Data ---
        df = pd.DataFrame(config['logistics_data'])

        # --- 4. Combine Live and Static Data ---
        df['Commodity_Price_per_Tonne_USD'] = price_per_tonne_usd
        df['USD_to_INR_Exchange_Rate'] = usd_to_inr
        
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")

        return df, last_updated

    except Exception as e:
        st.error(f"Failed to fetch real-time data for {commodity_name}: {e}. Displaying fallback data.")
        # Fallback logic can be enhanced here if needed
        return pd.DataFrame(), "N/A (API Error)"


def calculate_trade_analysis(cost_price_inr, weight_kg, df, commodity_name):
    """
    Calculates the potential profit and other metrics for exporting to each country.
    """
    if df.empty:
        return df

    weight_tonnes = weight_kg / 1000
    
    df['Total_Sale_Price_INR'] = (df['Commodity_Price_per_Tonne_USD'] * weight_tonnes) * df['USD_to_INR_Exchange_Rate']
    df['Total_Shipping_Cost_INR'] = df['Shipping_Cost_per_Tonne_INR'] * weight_tonnes
    df['Tariff_Cost_INR'] = df['Total_Sale_Price_INR'] * df['Tariff_Percentage']
    df['Total_Expenses_INR'] = cost_price_inr + df['Total_Shipping_Cost_INR'] + df['Tariff_Cost_INR']
    df['Potential_Profit_INR'] = df['Total_Sale_Price_INR'] - df['Total_Expenses_INR']
    df['ROI'] = (df['Potential_Profit_INR'] / cost_price_inr) * 100
    
    return df.sort_values(by='Potential_Profit_INR', ascending=False)

# --- Streamlit Dashboard UI ---

st.set_page_config(layout="wide")

# --- Sidebar for User Inputs ---
st.sidebar.header('Your Trade Scenario')
selected_commodity = st.sidebar.selectbox('Select Commodity', list(COMMODITY_DATA.keys()))

cost_price_inr = st.sidebar.number_input(f'Total Cost of Your {selected_commodity} (in ₹)', min_value=1000, value=50000, step=1000)
weight_kg = st.sidebar.number_input(f'Total Weight of {selected_commodity} (in kg)', min_value=100, value=1000, step=100)

st.sidebar.markdown("---")
with st.sidebar.expander("About the Data Sources"):
    st.info("""
        - **Live Data:** Commodity prices and currency exchange rates are fetched using the `yfinance` API.
        - **Static Data:** Shipping costs and tariffs are estimates. Real-world logistics data requires specialized data providers.
    """)

# --- Main Page Title ---
# Use an emoji that matches the commodity
commodity_emojis = {'Coffee': '☕', 'Wheat': '🌾', 'Corn': '🌽', 'Crude Oil': '🛢️'}
st.title(f'{commodity_emojis[selected_commodity]} Live {selected_commodity} Trade Risk & Profitability Dashboard')
st.write(f"An interactive tool to analyze the best export markets for {selected_commodity.lower()}.")


# --- Main Page Calculations & Display ---
market_data, last_updated = get_real_time_market_data(selected_commodity)

if not market_data.empty:
    analysis_df = calculate_trade_analysis(cost_price_inr, weight_kg, market_data, selected_commodity)

    st.header('Market Analysis Results')
    st.write(f"Based on a cost of **₹{cost_price_inr:,}** for **{weight_kg:,} kg** of {selected_commodity.lower()}:")
    st.caption(f"Market data last updated: {last_updated}")

    best_country = analysis_df.iloc[0]
    worst_country = analysis_df.iloc[-1]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('✅ Best Opportunity')
        st.success(f"**{best_country['Country']}**")
        st.metric(label="Potential Profit", value=f"₹{best_country['Potential_Profit_INR']:,.2f}")
        st.metric(label="Return on Investment (ROI)", value=f"{best_country['ROI']:.2f}%")

    with col2:
        st.subheader('❌ Lowest Return')
        st.error(f"**{worst_country['Country']}**")
        st.metric(label="Potential Profit", value=f"₹{worst_country['Potential_Profit_INR']:,.2f}")
        st.metric(label="Return on Investment (ROI)", value=f"{worst_country['ROI']:.2f}%")

    st.markdown("---")

    st.subheader('Full Country Comparison')
    st.dataframe(analysis_df[['Country', 'Potential_Profit_INR', 'ROI', 'Political_Risk_Score', 'Commodity_Price_per_Tonne_USD', 'Shipping_Cost_per_Tonne_INR']].style.format({
        'Potential_Profit_INR': "₹{:,.2f}",
        'ROI': "{:.2f}%",
        'Commodity_Price_per_Tonne_USD': "${:,.2f}",
        'Shipping_Cost_per_Tonne_INR': "₹{:,.0f}"
    }).background_gradient(cmap='RdYlGn', subset=['Potential_Profit_INR', 'ROI']))

    st.subheader('Profitability by Country')
    profit_chart_df = analysis_df[['Country', 'Potential_Profit_INR']].set_index('Country')
    st.bar_chart(profit_chart_df)
else:
    st.warning("Could not perform analysis due to an error in fetching market data.")


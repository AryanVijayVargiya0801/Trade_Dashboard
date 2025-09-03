# 📈 Live Multi-Commodity Trade Dashboard

An interactive dashboard built with Python and Streamlit to analyze the best export markets for various commodities like Coffee, Wheat, Corn, and Crude Oil.

## Features
- **Multi-Commodity Support:** Select a commodity from a dropdown to see a tailored analysis.
- **Live Market Data:** Fetches real-time commodity prices and currency exchange rates using the `yfinance` API.
- **Interactive Inputs:** Users can input their initial cost and weight to see custom calculations.
- **Profitability Analysis:** Calculates potential profit and ROI for various countries, factoring in estimated shipping costs and tariffs.
- **Data Visualization:** Includes a color-coded table and a bar chart for easy comparison.

## How to Run
1.  Install the required libraries:
    ```bash
    pip install streamlit pandas numpy yfinance
    ```
2.  Run the application:
    ```bash
    streamlit run trade_dashboard.py
    ```

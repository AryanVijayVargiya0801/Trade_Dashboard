{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\froman\fcharset0 Times-Roman;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 # \uc0\u55357 \u56520  Live Multi-Commodity Trade Dashboard\
\
## Features - **Multi-Commodity Support:** Select a commodity from a dropdown to see a tailored analysis. - **Live Market Data:** Fetches real-time commodity prices and currency exchange rates using the `yfinance` API. - **Interactive Inputs:** Users can input their initial cost and weight to see custom calculations. - **Profitability Analysis:** Calculates potential profit and ROI for various countries, factoring in estimated shipping costs and tariffs. - **Data Visualization:** Includes a color-coded table and a bar chart for easy comparison.\
\
## How to Run \
1. Install the required libraries: \
	```bash \
	pip install streamlit pandas numpy yfinance	\
	 ``` \
2. Run the application: \
	``\'92bash\
	streamlit run trade_dashboard.py\
	```}
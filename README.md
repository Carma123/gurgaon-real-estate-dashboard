# Gurgaon Real Estate Interactive Dashboard

## Project Overview
An interactive real estate analytics dashboard built using Python to explore property listings, prices, and property areas in Gurgaon.

## Features
- Interactive property type and locality filters
- Price range slider
- Dynamic KPI cards for total listings, average price, median price, and median area
- Interactive Plotly charts with hover information
- Filtered property data table
- Data preparation using Pandas, including duplicate removal and numeric conversion

## Technologies Used
- Python
- Pandas
- Streamlit
- Plotly Express

## How to Run the Project

1. Clone this repository.
2. Install the required packages:

   `python -m pip install -r requirements.txt`

3. Run the dashboard:

   `python -m streamlit run real_estate_dashboard.py`

4. Open the local URL displayed in your terminal.

## Dataset and Limitations
The dashboard uses a Gurgaon real estate listings dataset. Exact duplicate rows are removed, and invalid or non-positive prices and areas are excluded from the analysis.

The dataset's currency and area units have not been independently verified. Results should therefore be interpreted in the dataset's original units.

## Learning Outcomes
This project helped me practise data preparation, filtering, summary statistics, interactive data visualisation, and building a dashboard with Streamlit.

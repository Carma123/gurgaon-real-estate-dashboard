
import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# 1. PAGE SETUP
# ==================================================

st.set_page_config(
    page_title="Real Estate Dashboard",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Real Estate Market Dashboard")
st.caption("Explore property prices, listing counts and property areas.")

# ==================================================
# 2. LOAD AND PREPARE THE DATA
# ==================================================

@st.cache_data
def load_data():
    data = pd.read_csv("realestate.csv")

    # Remove exact duplicate rows.
    data = data.drop_duplicates().copy()

    # Convert prices to numbers, removing commas and spaces.
    for column in ["Price", "Rate per sqft", "Area"]:
        data[column] = pd.to_numeric(
            data[column].astype(str).str.replace(",", "", regex=False).str.strip(),
            errors="coerce"
        )

    # Remove rows that cannot be used for price/area analysis.
    data = data.dropna(subset=["Price", "Area"])
    data = data[(data["Price"] > 0) & (data["Area"] > 0)]

    # Avoid missing category labels in the dropdowns.
    for column in ["Flat Type", "Locality"]:
        data[column] = data[column].fillna("Unknown").astype(str)

    return data


df = load_data()

# ==================================================
# 3. SIDEBAR FILTERS
# ==================================================

st.sidebar.header("Filter properties")

# Property-type dropdown.
property_types = ["All"] + sorted(df["Flat Type"].unique().tolist())

selected_type = st.sidebar.selectbox(
    "Property type",
    property_types
)

# Locality dropdown.
localities = ["All"] + sorted(df["Locality"].unique().tolist())

selected_locality = st.sidebar.selectbox(
    "Locality",
    localities
)

# Price-range slider, expressed in millions.
# The full available price range is used initially.
min_price_m = float(df["Price"].min() / 1_000_000)
max_price_m = float(df["Price"].max() / 1_000_000)

price_range = st.sidebar.slider(
    "Price range (millions)",
    min_value=min_price_m,
    max_value=max_price_m,
    value=(min_price_m, max_price_m),
    step=1.0
)

# ==================================================
# 4. FILTER THE DATA
# ==================================================

# Start with the full dataset.
filtered_df = df.copy()

# Apply the property-type filter if a specific type is selected.
if selected_type != "All":
    filtered_df = filtered_df[
        filtered_df["Flat Type"] == selected_type
    ]

# Apply the locality filter if a specific locality is selected.
if selected_locality != "All":
    filtered_df = filtered_df[
        filtered_df["Locality"] == selected_locality
    ]

# Apply the selected minimum and maximum prices.
filtered_df = filtered_df[
    (filtered_df["Price"] >= price_range[0] * 1_000_000)
    & (filtered_df["Price"] <= price_range[1] * 1_000_000)
]

# ==================================================
# 5. CALCULATE THE KPIs FROM THE FILTERED DATA
# ==================================================

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

if filtered_df.empty:
    col1.metric("Total listings", "0")
    col2.metric("Average price", "N/A")
    col3.metric("Median price", "N/A")
    col4.metric("Median area", "N/A")

    st.warning("No properties match these filters. Adjust the selections.")
    st.stop()

total_listings = len(filtered_df)
overall_average_price = filtered_df["Price"].mean()
overall_median_price = filtered_df["Price"].median()
median_area = filtered_df["Area"].median()

col1.metric("Total listings", f"{total_listings:,}")
col2.metric("Average price", f"{overall_average_price / 1_000_000:.2f}M")
col3.metric("Median price", f"{overall_median_price / 1_000_000:.2f}M")
col4.metric("Median area", f"{median_area:,.0f}")

# ==================================================
# 6. CHART ONE: AVERAGE PRICE BY PROPERTY TYPE
# ==================================================

st.subheader("Average price by property type")

average_by_type = (
    filtered_df.groupby("Flat Type", as_index=False)["Price"]
    .mean()
    .sort_values("Price", ascending=False)
)

fig1 = px.bar(
    average_by_type,
    x="Flat Type",
    y="Price",
    color="Flat Type",
    title="Average Price by Property Type",
    labels={
        "Flat Type": "Property Type",
        "Price": "Average Price"
    },
    hover_data={"Price": ":,.0f"}
)

fig1.update_layout(showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

# ==================================================
# 7. CHART TWO: LISTINGS BY PROPERTY TYPE
# ==================================================

st.subheader("Number of listings by property type")

listing_counts = (
    filtered_df["Flat Type"]
    .value_counts()
    .rename_axis("Flat Type")
    .reset_index(name="Listings")
)

fig2 = px.bar(
    listing_counts,
    x="Flat Type",
    y="Listings",
    color="Flat Type",
    title="Number of Listings by Property Type",
    labels={
        "Flat Type": "Property Type",
        "Listings": "Number of Listings"
    }
)

fig2.update_layout(showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

# ==================================================
# 8. CHART THREE: AREA VS PRICE
# ==================================================

st.subheader("Property area versus price")

fig3 = px.scatter(
    filtered_df,
    x="Area",
    y="Price",
    color="Flat Type",
    hover_data=["Locality", "BHK_Count"],
    title="Property Area vs. Price",
    labels={
        "Area": "Area (dataset units)",
        "Price": "Price"
    },
    opacity=0.6
)

st.plotly_chart(fig3, use_container_width=True)

# ==================================================
# 9. SHOW THE FILTERED DATA
# ==================================================

with st.expander("View filtered property data"):
    st.write(f"Showing {len(filtered_df):,} matching listings.")
    st.dataframe(filtered_df, use_container_width=True)

st.caption(
    "Prices are shown in the dataset's units. "
    "The currency and area units have not been independently verified."
)

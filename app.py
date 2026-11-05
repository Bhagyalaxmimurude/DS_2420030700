
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import backend

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Estate Insights",
    page_icon="🏡",
    layout="wide"
)

# =====================================
# PROFESSIONAL BLUE-BLACK THEME
# =====================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #050B18 0%,
        #0B1930 50%,
        #102D50 100%
    );
    color: #F8FAFC;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #050B18,
        #102D50
    );
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

h1, h2, h3, p, label {
    color: #F8FAFC;
}

div[data-testid="stForm"] {
    background: #111F35;
    padding: 25px;
    border: 1px solid #24466C;
    border-radius: 16px;
}

.stTextInput input {
    background-color: #172943;
    color: white;
    border: 1px solid #34577F;
    border-radius: 8px;
}

div.stButton > button {
    background: linear-gradient(90deg, #1266D5, #2589F5);
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: bold;
    padding: 10px;
}

div.stButton > button:hover {
    background: #D6A84F;
    color: #071426;
}

[data-testid="stMetric"] {
    background: #111F35;
    border: 1px solid #24466C;
    padding: 20px;
    border-radius: 12px;
}

[data-testid="stDataFrame"] {
    background: #111F35;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# =====================================
# LOGIN SYSTEM
# =====================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.markdown("""
        <div style="
            text-align:center;
            padding:35px;
            background:linear-gradient(135deg,#050B18,#123D70);
            border:1px solid #24577D;
            border-radius:18px;
            color:white;
            margin-bottom:25px;">
            <h1 style="color:white;">🏡 ESTATE INSIGHTS</h1>
            <h3 style="color:#D6A84F;">Real Estate Analytics Platform</h3>
            <p style="color:white;">
                Explore Properties | Analyze Prices | Predict Values
            </p>
        </div>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.2, 1])

    with center:

        st.subheader("Welcome Back")

        st.write("Please login to continue.")

        with st.form("login_form"):

            username = st.text_input("Username")

            password = st.text_input(
                "Password",
                type="password"
            )

            login = st.form_submit_button(
                "Login",
                use_container_width=True
            )

        if login:

            if username == "admin" and password == "admin123":

                st.session_state.logged_in = True
                st.rerun()

            else:

                st.error("Invalid username or password.")

        st.caption("Demo Username: admin")
        st.caption("Demo Password: admin123")

    st.stop()


# =====================================
# BACKEND CONNECTION
# =====================================

@st.cache_data
def get_data():

    data = backend.load_data()

    data = backend.clean_data(data)

    return data


df = get_data()

prepared_data = backend.prepare_data(df)


# =====================================
# SIDEBAR NAVIGATION
# =====================================

st.sidebar.markdown("""
<h1 style="color:#42A5FF;">🏡 ESTATE INSIGHTS</h1>
<p style="color:#A9C9EA;">REAL ESTATE INTELLIGENCE</p>
""", unsafe_allow_html=True)

st.sidebar.divider()

page = st.sidebar.radio(
    "MAIN MENU",
    [
        "Home",
        "Data Analysis",
        "Location Analysis",
        "Price Prediction",
        "Machine Learning",
        "Budget Filter",
        "Download Reports",
        "About Project"
    ]
)

st.sidebar.divider()

st.sidebar.write("Logged in as Admin")

if st.sidebar.button("Logout", use_container_width=True):

    st.session_state.logged_in = False
    st.rerun()


# =====================================
# HOME PAGE
# =====================================

if page == "Home":

    st.title("Real Estate Dashboard")

    st.write(
        "Welcome to Estate Insights – Explore Bengaluru "
        "property market trends and price information."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Properties",
        f"{len(df):,}"
    )

    col2.metric(
        "Total Locations",
        f"{df['location'].nunique():,}"
    )

    col3.metric(
        "Average House Price",
        f"₹ {df['price'].mean():.2f} Lakhs"
    )

    st.divider()

    st.subheader("Project Overview")

    c1, c2, c3 = st.columns(3)

    c1.info(
        "📊 DATA ANALYSIS\n\n"
        "Explore property statistics and price trends."
    )

    c2.info(
        "📍 LOCATION INSIGHTS\n\n"
        "Compare house prices across locations."
    )

    c3.info(
        "🤖 PRICE PREDICTION\n\n"
        "Estimate house prices using Machine Learning."
    )

    st.subheader("Recent Property Records")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )


# =====================================
# DATA ANALYSIS
# =====================================

elif page == "Data Analysis":

    st.title("📊 Data Analysis")

    st.write("Explore and understand the Bengaluru house dataset.")

    st.subheader("Dataset Overview")

    st.dataframe(
        df.describe(),
        use_container_width=True
    )

    st.subheader("Missing Values")

    missing = df.isnull().sum().reset_index()

    missing.columns = ["Column", "Missing Values"]

    st.dataframe(
        missing,
        use_container_width=True
    )

    st.divider()

    st.subheader("House Price Distribution")

    fig, ax = plt.subplots()

    sns.histplot(
        df["price"],
        bins=30,
        kde=True,
        ax=ax
    )

    ax.set_xlabel("Price (Lakhs)")
    ax.set_title("Distribution of House Prices")

    fig.patch.set_facecolor("#EAF1F8")
    ax.set_facecolor("#EAF1F8")

    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Area vs Price")

    fig, ax = plt.subplots()

    sns.scatterplot(
        data=prepared_data,
        x="total_sqft",
        y="price",
        ax=ax
    )

    ax.set_xlabel("Area (Square Feet)")
    ax.set_ylabel("Price (Lakhs)")

    fig.patch.set_facecolor("#EAF1F8")
    ax.set_facecolor("#EAF1F8")

    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Correlation Heatmap")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.heatmap(
        prepared_data[
            ["total_sqft", "bath", "price"]
        ].corr(),
        annot=True,
        cmap="Blues",
        ax=ax
    )

    st.pyplot(fig)
    plt.close(fig)


# =====================================
# LOCATION ANALYSIS
# =====================================

elif page == "Location Analysis":

    st.title("📍 Location Analysis")

    st.write("Explore property prices in Bengaluru locations.")

    locations = sorted(
        df["location"].dropna().unique()
    )

    selected_location = st.selectbox(
        "Choose Location",
        locations
    )

    location_data = df[
        df["location"] == selected_location
    ]

    col1, col2 = st.columns(2)

    col1.metric(
        "Available Properties",
        len(location_data)
    )

    col2.metric(
        "Average Price",
        f"₹ {location_data['price'].mean():.2f} Lakhs"
    )

    st.subheader("Property Details")

    st.dataframe(
        location_data[
            ["location", "size", "total_sqft", "bath", "price"]
        ].head(20),
        use_container_width=True
    )

    st.subheader("Top 10 Locations by Average Price")

    top_locations = (
        df.groupby("location")["price"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    top_locations.plot(kind="bar", ax=ax)

    ax.set_ylabel("Average Price (Lakhs)")
    ax.set_xlabel("Location")

    plt.xticks(rotation=45)

    fig.patch.set_facecolor("#EAF1F8")
    ax.set_facecolor("#EAF1F8")

    st.pyplot(fig)
    plt.close(fig)


# =====================================
# PRICE PREDICTION
# =====================================

elif page == "Price Prediction":

    st.title("🏠 House Price Estimator")

    st.write("Enter property details to estimate its price.")

    col1, col2 = st.columns(2)

    with col1:

        area = st.number_input(
            "Area (Square Feet)",
            min_value=100,
            max_value=10000,
            value=1000
        )

        bathrooms = st.number_input(
            "Number of Bathrooms",
            min_value=1,
            max_value=10,
            value=2
        )

    with col2:

        bedrooms = st.number_input(
            "Number of Bedrooms",
            min_value=1,
            max_value=10,
            value=2
        )

        st.write("Selected Bedrooms:", bedrooms)

    if st.button("Estimate House Price"):

        price_per_sqft = (
            prepared_data["price"] * 100000 /
            prepared_data["total_sqft"]
        ).median()

        estimated_price = (
            area * price_per_sqft / 100000
        )

        st.success(
            f"Estimated House Price: ₹ {estimated_price:.2f} Lakhs"
        )

        st.caption(
            "This estimate uses median price per square foot. "
            "Bedroom and bathroom inputs are not used in this calculation."
        )


# =====================================
# MACHINE LEARNING
# =====================================

elif page == "Machine Learning":

    st.title("🤖 Machine Learning")

    st.write(
        "This project uses Linear Regression to estimate "
        "house prices based on area and bathroom count."
    )

    with st.spinner("Training Machine Learning Model..."):

        model, mae, r2 = backend.train_model(df)

    col1, col2 = st.columns(2)

    col1.metric(
        "Mean Absolute Error",
        f"{mae:.2f} Lakhs"
    )

    col2.metric(
        "R2 Score",
        f"{r2:.2f}"
    )

    st.success("Linear Regression model trained successfully!")

    st.subheader("Predict a House Price")

    area = st.number_input(
        "Enter Area (Square Feet)",
        min_value=100,
        max_value=10000,
        value=1200,
        key="ml_area"
    )

    bath = st.number_input(
        "Enter Number of Bathrooms",
        min_value=1,
        max_value=10,
        value=2,
        key="ml_bath"
    )

    if st.button("Predict Using ML Model"):

        prediction = model.predict(
            pd.DataFrame(
                [[area, bath]],
                columns=["total_sqft", "bath"]
            )
        )

        st.success(
            f"ML Predicted House Price: ₹ {prediction[0]:.2f} Lakhs"
        )


# =====================================
# BUDGET FILTER
# =====================================

elif page == "Budget Filter":

    st.title("💰 Find Houses Within Your Budget")

    min_price = float(df["price"].min())

    max_price = float(df["price"].max())

    price_range = st.slider(
        "Select Your Budget (Lakhs)",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price)
    )

    filtered_data = df[
        (df["price"] >= price_range[0]) &
        (df["price"] <= price_range[1])
    ]

    st.metric(
        "Available Properties",
        len(filtered_data)
    )

    st.dataframe(
        filtered_data[
            ["location", "size", "total_sqft", "bath", "price"]
        ].head(100),
        use_container_width=True
    )


# =====================================
# DOWNLOAD REPORTS
# =====================================

elif page == "Download Reports":

    st.title("📥 Download Reports")

    st.write("Download the Bengaluru property dataset.")

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Complete Dataset",
        data=csv_data,
        file_name="Bengaluru_House_Data.csv",
        mime="text/csv"
    )


# =====================================
# ABOUT PROJECT
# =====================================

elif page == "About Project":

    st.title("ℹ️ About Estate Insights")

    st.write(
        "Real Estate Price Exploration Tool is a Data Science "
        "project designed to analyze Bengaluru house prices "
        "and understand factors affecting property values."
    )

    st.subheader("Project Objectives")

    st.markdown("""
    - Analyze Bengaluru house price data.
    - Clean and process the dataset.
    - Explore price patterns using visualizations.
    - Compare property prices across locations.
    - Estimate house prices.
    - Train a Linear Regression model.
    - Filter and download property data.
    """)

    st.subheader("Technologies Used")

    st.markdown("""
    - Python
    - Pandas
    - NumPy
    - Matplotlib
    - Seaborn
    - Scikit-learn
    - Streamlit
    """)

    st.subheader("Conclusion")

    st.write(
        "This project provides an interactive way to explore "
        "real estate data, understand property price trends "
        "and estimate house prices using Machine Learning."
    )

    st.success("Thank you for using Estate Insights!")

import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
import re
import time
import os

st.markdown("""
<style>

/* 🌌 FULL APP BACKGROUND */
.stApp {
    background: linear-gradient(145deg, #0f172a, #020617);
    color: #e2e8f0;
}

/* 📌 SIDEBAR MATCH */
section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.8);
    backdrop-filter: blur(12px);
    border-right: 1px solid #1e293b;
}

/* 🎯 SIDEBAR ICONS */
section[data-testid="stSidebar"] svg {
    color: #38bdf8 !important;
    fill: #38bdf8 !important;
}

/* 🏷️ TITLES */
h1 {
    color: #38bdf8;
    font-weight: 700;
    letter-spacing: 1px;
}

h2, h3 {
    color: #cbd5f5;
}

/* 💎 GLASS CARD (USE EVERYWHERE) */
.block-container {
    background: rgba(15, 23, 42, 0.55);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(56, 189, 248, 0.2);
    backdrop-filter: blur(10px);
}

/* 📊 METRIC CARDS */
[data-testid="metric-container"] {
    background: rgba(30, 41, 59, 0.6);
    backdrop-filter: blur(10px);
    padding: 18px;
    border-radius: 14px;
    border: 1px solid rgba(56, 189, 248, 0.3);
    box-shadow: 0 8px 25px rgba(0,0,0,0.5);
    transition: 0.3s;
}

/* 🔥 HOVER EFFECT */
[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    border: 1px solid #38bdf8;
}

/* 🔘 BUTTONS */
.stButton>button {
    background: linear-gradient(135deg, #38bdf8, #0ea5e9);
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 600;
    padding: 8px 18px;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}

/* ⌨️ INPUT */
.stTextInput>div>div>input {
    background: rgba(15, 23, 42, 0.7);
    color: white;
    border: 1px solid #334155;
    border-radius: 10px;
}

/* 📊 DATAFRAME */
[data-testid="stDataFrame"] {
    background: rgba(15, 23, 42, 0.7);
    border-radius: 12px;
    border: 1px solid #1e293b;
}

/* 📌 SELECTBOX */
.stSelectbox div[data-baseweb="select"] {
    background: rgba(15, 23, 42, 0.7);
    color: white;
}

/* 📌 SLIDER */
.stSlider {
    color: #38bdf8;
}

/* 📌 DIVIDER */
hr {
    border: 1px solid #1e293b;
}

/* 🌊 SCROLLBAR */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #38bdf8;
    border-radius: 10px;
}

/* ✨ TITLE GLOW LINE */
h1::after {
    content: "";
    display: block;
    width: 70px;
    height: 3px;
    background: #38bdf8;
    margin-top: 6px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


st.set_page_config( page_title="Travels Login Page",
                    layout="wide",
                    page_icon="🚌",
                    )


file = "user_load.csv"
df = pd.read_csv("travel_places_30000.csv")

if "logged_in" not in st.session_state:
    st.session_state.logged_in =False
if "username" not in st.session_state:
    st.session_state.username =""
if "page" not in st.session_state:
    st.session_state.page ="Login"

# ---------------------------------------------------

def signup_page():
    st.subheader("Register New User")
    if not os.path.exists(file):
        pd.DataFrame(columns=[
            "Name",
            "Email",
            "Gender",
            "Age",
            "City",
            "State",
            "Country",
            "Username",
            "Password",
        ]).to_csv(file,index=False)

    with st.form("signup"):
        df = pd.read_csv(file)
        name=st.text_input("Name")
        email=st.text_input("Email")
        gender=st.radio("Gender",
                             ["Male","Female","Other"])
        age=st.number_input("Age")
        city=st.text_input("City")
        state=st.text_input("State")
        country=st.text_input("Country")
        username=st.text_input("Username")
        password=st.text_input("Password",type="password")

        submit=st.form_submit_button("Submit")


        if submit:
            if not all([name,email,gender,age,city,state,country,username,password]):
                st.error("Enter All Details!")
            elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                st.error("Invalid email address !")
            elif not re.match(r"[A-Z]", password):
                st.error("Password must contain one uppercase")
            elif not re.search(r"[a-z]", password):
                st.error("Password must contain one Lowercase")
            elif username in df["Username"].values:
                st.error("Username Already Exists")
            else:
                new_user = pd.DataFrame([{
                    "Name":name,
                    "Email":email,
                    "Gender":gender,
                    "Age":age,
                    "City":city,
                    "State":state,
                    "Country":country,
                    "Username":username,
                    "Password":password,
                }])

                pd.concat([df,new_user],ignore_index=True).to_csv(file,index=False)
                st.success("User Created!")
                st.session_state.page = "Login"
                st.rerun()


    if st.button("Already User ? login Here"):
            st.session_state.page = "Login"
            st.rerun()


def login_page():
    st.header("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password",type="password")

    if st.button("Login"):
        if os.path.exists(file):
            df = pd.read_csv(file)
            user = df[(df["Username"]==username) & (df["Password"]==password)]
            if not user.empty:
                st.session_state.logged_in =True
                st.session_state.username = username
                st.session_state.page = "Home"
                st.success("Login successfully !")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Username Or Password Is Incorrect")
    if st.button("New User ?? Register"):
        st.session_state.page="Signup"
        st.rerun()

if st.session_state.page == "Signup":
    signup_page()
    st.stop()
elif st.session_state.page == "Login":
    login_page()
    st.stop()

elif st.session_state.page == "Home":
    if not st.session_state.logged_in:
        st.session_state.page = "Login"
        st.rerun()


if st.session_state.logged_in :
    with st.sidebar:
            selected = option_menu(
                menu_title= "Travel Dashboard",
                options=["Dataset",
                         "Place Explorer",
                         "Travel Analysis",
                         "Map View",
                         "AI Travel Finder",
                         "Travel Assistant"],
                styles={
                    "container": {
                        "padding": "10px",
                        "background": "rgba(15, 23, 42, 0.6)",  # glass effect
                        "border-radius": "12px",
                        "border": "1px solid #1e293b"
                    },

                    "icon": {
                        "color": "#38bdf8",  # neon blue
                        "font-size": "22px"
                    },

                    "nav-link": {
                        "font-size": "16px",
                        "text-align": "left",
                        "margin": "6px",
                        "padding": "10px",
                        "border-radius": "10px",
                        "color": "#cbd5f5",
                        "font-weight": "500",
                        "--hover-color": "rgba(56, 189, 248, 0.15)"  # soft blue hover
                    },

                    "nav-link-selected": {
                        "background": "linear-gradient(135deg, #38bdf8, #0ea5e9)",
                        "color": "white",
                        "font-weight": "600",
                        "border-radius": "10px",
                        "box-shadow": "0 0 10px rgba(56,189,248,0.6)"
                    }
                },

                    icons = [
                        "table",        # Dataset
                        "search",       # Place Explorer
                        "bar-chart",    # Travel Analysis
                        "geo-alt",      # Map View
                        "stars",        # AI Travel Finder
                        "robot"         # Travel Assistant
                    ],

                menu_icon="airplane",

            )
            st.divider()

            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.page = "Login"
                st.success("Logout Thai gaya 👋")
                time.sleep(1)
                st.rerun()

# ------------------------------- data set -----------------------------

if selected == "Dataset":
    st.title("📊 Travel Dataset Dashboard")

    col1,col2,col3 = st.columns(3)

    col1.metric(label="Total Rows",value = df.shape[0])
    col2.metric(label="Total Columns",value = df.shape[1])
    col3.metric(label="Missing Values",value = df.isnull().sum().sum())

    st.divider()

    # column selection
    st.subheader("Column Selection")
    selected_columns = st.multiselect(
        label="Choose Columns",
        options=df.columns.tolist(),
        default=df.columns.tolist()
    )
    filtered_df = df[selected_columns]

    st.divider()

    # search dataset
    st.subheader("Search in Dataset")
    search = st.text_input("Search Data From Here")

    if search:
        filtered_df = filtered_df[
            filtered_df.astype(str).apply(
                lambda row: row.str.contains(search, case=False).any(), axis=1
            )
        ]

    st.divider()

    # column filter - column name | value
    st.subheader("Filter by Column Value")
    col1, col2 = st.columns(2)
    with col1:
        filter_column = st.selectbox("Select Column", filtered_df.columns)
    with col2:
        filter_value = st.selectbox("Select Value", filtered_df[filter_column].dropna().unique())

    # Apply the Filter
    if st.button("Apply Filter"):
        filtered_df = filtered_df[filtered_df[filter_column] == filter_value]

    st.divider()
    st.dataframe(filtered_df)

    st.markdown("### Download Here")
    csv = filtered_df.to_csv(index=False).encode('UTF-8')
    st.download_button(
        label="Download",
        data=csv,
        file_name="Travels_filtered.csv",
        mime="text/csv"
    )

    st.divider()

    # slider
    st.subheader("Row Slider")
    if len(filtered_df) > 0:
        row_num = st.slider("Select Row Number",
                            1,
                            max_value=len(filtered_df),
                            value=1)

        st.subheader("Row Preview")
        st.dataframe(filtered_df.iloc[[row_num - 1]])
    else:
        st.warning("No data to display")

# -----------------------------overview-----------------------------------
elif selected == "Place Explorer":
    st.title("🌍 Travel Dashboard Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tours", len(df))
    col2.metric("Total City", df["City"].nunique() if "City" in df.columns else 0)
    col3.metric("Total Country", df["Country"].nunique())


# place visit lists

    travel_data = df.groupby("City").agg(
        total_tours=("City", "count"),
        total_country=("Country", "nunique"),
        Avg_rating=("Rating", "mean"),
    )

    travel_data["Share %"] = travel_data["total_tours"] / len(df) * 100

    st.dataframe(
        travel_data.style.format({
            "total_tours": "{:,.0f}",
            "total_country": "{:,.0f}",
            "Avg_rating": "{:,.1f}",
            "Share %": "{:,.2f}%"
        }).background_gradient(subset="total_tours", cmap="Spectral")
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(" City Tour Season ")

        eff_df = df.groupby("City").agg(
            Total_tours=("City", "count"),
            Season_Count=("Season", "count")
        )

        st.dataframe(
            eff_df.style
            .highlight_max(axis=0, color="#bd6522")
            .highlight_min(axis=0, color="#e6ed6f"),
            use_container_width=True
        )

    with col2:
        st.subheader("Travel And Distance")

        comp_df = df.groupby("City").agg(
            Travel_Type=("Travel_Type", "nunique"),
            Distance=("Distance_KM", "nunique")
        )

        st.dataframe(comp_df, use_container_width=True)


    st.title("Travels Operation")
    st.markdown("---")

    tours_df= df.copy()
    total_tours = len(tours_df)
    City = tours_df["City"].nunique()
    Country = tours_df["Country"].nunique()

    if tours_df["Rating"].notna().sum() > 0:
        top_rated = tours_df["Rating"].value_counts().idxmax()
    else:
        top_rated = "No Data"

            # kpi layout
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("🎵 Total Tours", f"{total_tours:,}", "Target 1 Lakh")
    kpi2.metric("🎤 Citys", f"{City:,}", "Last Month", "inverse")
    kpi3.metric("🔥 Country", f"{Country:,}", "+2.3 Growth")
    kpi4.metric("🏆 Top Rated Tours", top_rated)

        # show full dataset
    if st.checkbox("Show Full Dataset"):
        st.dataframe(tours_df, use_container_width=True)

        # Column statistics
    st.subheader("Column Statistics")
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    if len(numeric_cols) > 0:
        selected_col = st.selectbox("Select Numeric Column", numeric_cols)
        st.write(df[selected_col].describe())

    st.divider()


# ------------------------------- Charts --------------------------------

elif selected == "Travel Analysis":
    st.title("📈Travels Analysis Charts")


    st.subheader("🎯 1. Trips by Country (MOST IMPORTANT)")
    st.subheader("🌍 Trips by Country")

    country_count = df["Country"].value_counts().head(10)

    fig = px.bar(
        x=country_count.index,
        y=country_count.values,
        title="Top Countries by Trips"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🎯 2. City Popularity (Horizontal Bar)")
    st.subheader("🏙️ Top Cities")

    city_count = df["City"].value_counts().head(10)

    fig = px.bar(
        x=city_count.values,
        y=city_count.index,
        orientation="h",
        title="Most Visited Cities"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("🎯 3. Travel Purpose Distribution (Pie)")
    st.subheader("🎯 Travel Purpose")

    fig = px.pie(
        df,
        names="Trip_Purpose",
        title="Travel Purpose Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("🎯 4. Budget Distribution (Histogram)")
    st.subheader("💰 Budget Distribution")

    fig = px.histogram(
        df,
        x="Budget_Per_Person_USD",
        nbins=30,
        title="Budget Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("🎯 5. Rating vs Budget (BEST INSIGHT 🔥)")
    st.subheader("⭐ Rating vs Budget")

    fig = px.scatter(
        df,
        x="Budget_Per_Person_USD",
        y="Rating",
        color="Trip_Purpose",
        title="Does Higher Budget Mean Better Rating?"
    )
    st.plotly_chart(fig, use_container_width=True)


    st.divider()

    st.subheader("🎯 6. Season-wise Trips (Bar Chart)")
    st.subheader("🌤️ Season-wise Trips")

    season_count = df["Season"].value_counts()

    fig = px.bar(
        x=season_count.index,
        y=season_count.values,
        title="Trips by Season"
    )
    st.plotly_chart(fig, use_container_width=True)


    st.divider()

    st.subheader("7. 🗺️ Map Chart")
    st.subheader("🗺️ Travel Map")

    fig = px.scatter_geo(
        df,
        locations="Country",
        locationmode="country names",
        size="No_of_Travelers",
        color="Rating",
        title="Global Travel Overview"
    )
    st.plotly_chart(fig)

    st.divider()

    st.subheader("🎯 8. Area Chart (Trend Analysis 📈)")
    st.subheader("📅 Travel Trend Over Time")

    df["Travel_Date"] = pd.to_datetime(df["Travel_Date"], errors="coerce")

    year_data = df["Travel_Date"].dt.year.value_counts().sort_index()

    fig = px.area(
        x=year_data.index,
        y=year_data.values,
        title="Trips Over Years"
    )
    st.plotly_chart(fig, use_container_width=True)


    st.divider()

    st.subheader("🎯 9. Box Plot (Outlier Detection 📦)")
    st.subheader("💰 Budget Spread by Travel Type")

    fig = px.box(
        df,
        x="Trip_Purpose",
        y="Budget_Per_Person_USD",
        title="Budget Spread"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("🎯 10. Treemap (Hierarchy View 🌳)")
    st.subheader("🌳 Travel Hierarchy")

    fig = px.treemap(
        df,
        path=["Country", "City", "Trip_Purpose"],
        title="Travel Distribution Hierarchy"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
# --------------------- Map View----------------------------
elif selected == "Map View":
    st.title("🗺️ Dynamic City Map")

    city = st.text_input("Type any city name")

    if city:
        st.write(f"Showing location for {city}")
        st.components.v1.iframe(
            f"https://maps.google.com/maps?q={city}&t=&z=12&ie=UTF-8&iwloc=&output=embed",
            height=500
        )

# ---------------------- Ai Travel Finder ------------------------


elif selected == "AI Travel Finder":

    st.title("🌍 AI TRAVEL FINDER")

    st.write("🔎 Search by City, Country, Region, Season")

    query = st.text_input("Enter place (e.g. Goa, India, Adventure)")

    if query:
        q = query.lower()

        # 🔥 Smart search from full dataset
        filtered = df[df.apply(lambda row: q in str(row.values).lower(), axis=1)]

        if filtered.empty:
            st.warning("😅 No matching place found")
        else:
            # ✅ ONLY BEST RESULT (NO LOOP)
            best = filtered.sort_values(by="Rating", ascending=False).iloc[0]

            st.divider()

            # 📍 Title
            st.subheader(f"📍 {best.get('City', 'N/A')}, {best.get('Country', 'N/A')}")

            # 📊 Details
            st.info(f"""
            ✈️ Trip Type: {best.get('Trip_Purpose', 'N/A')}  
            🌍 Region: {best.get('Region', 'N/A')}  
            🏨 Stay: {best.get('Accommodation_Type', 'N/A')}  
            💰 Budget: ${best.get('Budget_Per_Person_USD', 'N/A')}  
            ⭐ Rating: {best.get('Rating', 'N/A')}  
            🌤️ Season: {best.get('Season', 'N/A')}  
            """)

            # 🖼️ Images
            col1, col2 = st.columns(2)
            col1.image(f"https://loremflickr.com/500/300/{best.get('City', 'travel')},tourism",
                       use_container_width=True)
            col2.image(f"https://loremflickr.com/500/300/{best.get('City', 'travel')},landscape",
                       use_container_width=True)

            # 🎥 Video
            yt_url = f"https://www.youtube.com/results?search_query={best.get('City', 'travel')}+travel+guide"
            st.link_button("🎥 Watch Travel Guide", yt_url)

            # 🗺️ Map
            st.subheader("📍 Location")
            st.components.v1.iframe(
                f"https://maps.google.com/maps?q={best.get('City', '')}&t=&z=12&ie=UTF8&iwloc=&output=embed",
                height=400
            )
# ------------------------- Travel Assistant --------------------------------------


elif selected == "Travel Assistant":

    st.title("🤖 Travel Assistant")

    user_question = st.text_input("Ask Something About Tour Dataset")

    if user_question:
        q = user_question.lower()

        # 🌍 Total Trips

        if "total tours" in q or "how many trips" in q:
            st.success(f"Total Tours : {len(df)}")

        # 🌆 City Analysis
        elif "city" in q:
            city_counts = df["City"].value_counts()
            st.success(f"Top City : {city_counts.idxmax()}")

            fig = px.bar(
                x=city_counts.index[:10],
                y=city_counts.values[:10],
                title="Top Cities"
            )
            st.plotly_chart(fig)

        # 🌍 Country Analysis
        elif "country" in q:
            country_counts = df["Country"].value_counts()
            st.success(f"Top Country :{country_counts.idxmax()}")

            fig = px.bar(
                x=country_counts.index[:10],
                y=country_counts.values[:10],
                title="Top Countries"
            )
            st.plotly_chart(fig)

        # 🌤️ Season Analysis

        elif "season" in q:
            season_counts = df["Season"].value_counts()
            st.success(f"Top Season :{season_counts.idxmax()}")

            fig = px.pie(
                names=season_counts.index,
                values=season_counts.values,
                title="Seasons Distribution"
            )
            st.plotly_chart(fig)

        # 💰 Budget Analysis

        elif "budget" in q:
            df["Budget_Per_Person_USD"] = pd.to_numeric(df["Budget_Per_Person_USD"], errors="coerce")

            st.success(f"Average Budget: ${df['Budget_Per_Person_USD'].mean():,.2f}")

            fig = px.histogram(
                df,
                x="Budget_Per_Person_USD",
                nbins=30,
                title="Budget Distribution"
            )
            st.plotly_chart(fig)

        # ⭐ Rating Analysis

        elif "rating" in q:
            df["Rating"]=pd.to_numeric(df["Rating"], errors="coerce")
            rating_counts =df["Rating"].value_counts()

            if len(rating_counts)>0:
                st.success(f"Top Rating :{rating_counts.idxmax()}")

                fig = px.bar(
                    x=rating_counts.index,
                    y=rating_counts.values,
                    title="Rating Distribution"
                )
                st.plotly_chart(fig)

        # ✈️ Airline Analysis

        elif "airline" in q:
            airline_counts = df["Airline"].value_counts()
            st.success(f"Top Airline :{airline_counts.idxmax()}")

            fig = px.bar(
                x=airline_counts.values[:10],
                y=airline_counts.index[:10],
                orientation="h",
                title="Top Airlines"
            )
            st.plotly_chart(fig)

        elif "travel type" in q or "trip type" in q:
            type_counts = df["Travel_Type"].value_counts()

            fig = px.pie(
                names=type_counts.index,
                values=type_counts.values,
                title="Travel Type Distribution"
            )
            st.plotly_chart(fig)

        # 🛂 Visa Type

        elif "visa" in q:
            visa_counts = df["Visa_Type"].value_counts()

            fig = px.bar(
                x=visa_counts.index,
                y =visa_counts.values,
                title="Visa Type Distribution"
            )
            st.plotly_chart(fig)

        # ⏱️ Duration

        elif "duration" in q:
            df["Duration_Days"]=pd.to_numeric(df["Duration_Days"], errors="coerce")
            st.success(f"Average Duration :{df["Duration_Days"].mean():.1f}Days")

            fig = px.histogram(
                df,
                x="Duration_Days",
                nbins=20,
                title="Trip Duration Distribution"
            )
            st.plotly_chart(fig)
        # ❌ Default
    else:
        st.warning("""
        
Try Asking :
- Total Tours
- City
- Country
- Season
- Budget
- Rating
- Airline
- Visa
- Duration
        """)
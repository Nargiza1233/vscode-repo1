import base64
import os

import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# Sahifa sozlamalari
st.set_page_config(
    page_title="Credit Card Customer Analytics",
    layout="wide"
)

# Logotip/rasmni xavfsiz yuklash (fayl bo'lmasa ham dastur qulamaydi)
LOGO_PATH = "assets/image_2026-06-19_10-04-14.png"

if os.path.exists(LOGO_PATH):
    with open(LOGO_PATH, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="data:image/png;base64,{img_base64}" width="400">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning(f"Rasm topilmadi: {LOGO_PATH}")

# Sarlavha
st.markdown(
    "<h1 style='text-align:center; color:#1E88E5;'>💳 CREDIT CARD CUSTOMERS</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='text-align:center;'>Customer Analytics and Churn Prediction Dashboard</h3>",
    unsafe_allow_html=True
)


# Datasetni yuklash
@st.cache_data
def load_data():
    df = pd.read_csv("BankChurners.csv")

    # Faqat datasetda mavjud bo'lgan ustunlarni o'chiramiz (xato oldini olish uchun)
    cols_to_drop = [
        "CLIENTNUM",
        "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1",
        "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2"
    ]
    existing_cols = [c for c in cols_to_drop if c in df.columns]
    df = df.drop(columns=existing_cols)

    return df


df = load_data()

# Sidebar
page = st.sidebar.selectbox(
    "Choose a page",
    ["About Dataset", "Visual Dashboard", "Customer Analysis", "Prediction", "Team"]
)

# ABOUT DATASET
if page == "About Dataset":

    st.header(" Dataset haqida")

    st.write("""
    Ushbu dataset bankning kredit karta mijozlari haqidagi ma'lumotlarni o'z ichiga oladi.
    Loyihaning asosiy maqsadi — bankni tark etishi mumkin bo'lgan mijozlarni aniqlash.
    """)

    st.write("Mijozlar soni:", len(df))
    st.write("Ustunlar soni:", len(df.columns))

    st.dataframe(df.head())

# DASHBOARD
elif page == "Visual Dashboard":

    total_customers = len(df)
    existing = len(df[df["Attrition_Flag"] == "Existing Customer"])
    attrited = len(df[df["Attrition_Flag"] == "Attrited Customer"])
    avg_credit = round(df["Credit_Limit"].mean(), 2)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", total_customers)
    col2.metric("Existing Customers", existing)
    col3.metric("Attrited Customers", attrited)
    col4.metric("Average Credit Limit", f"${avg_credit}")

    fig1 = px.pie(
        df,
        names="Attrition_Flag",
        title="Customer Attrition"
    )

    fig2 = px.histogram(
        df,
        x="Customer_Age",
        color="Gender",
        title="Customer Age Distribution"
    )

    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)

# CUSTOMER ANALYSIS
elif page == "Customer Analysis":

    gender = st.selectbox(
        "Select Gender",
        ["All"] + list(df["Gender"].unique())
    )

    filtered_df = df.copy()

    if gender != "All":
        filtered_df = filtered_df[filtered_df["Gender"] == gender]

    fig = px.box(
        filtered_df,
        x="Card_Category",
        y="Credit_Limit",
        color="Attrition_Flag",
        title="Credit Limit by Card Category"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(filtered_df)

# PREDICTION
elif page == "Prediction":

    st.header(" Customer Churn Prediction")

    age = st.slider("Customer Age", 18, 80, 35)
    credit = st.number_input("Credit Limit", 1000, 50000, 10000)
    transactions = st.number_input("Total Transactions", 1, 200, 50)

    if st.button("Predict"):

        if transactions < 40 and credit > 15000:
            st.error(" High Risk of Attrition")
        else:
            st.success(" Customer Likely to Stay")

# TEAM
elif page == "Team":

    st.header("👥 Contributors")

    st.write("- Nargiza")
    st.write("- Jamoa a'zosi: Maqsuda")
    st.write("- Jamoa a'zosi: Munisa")

    st.success("Thank you for your attention!")

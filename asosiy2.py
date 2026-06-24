import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# =====================================
# SAHIFA SOZLAMALARI
# =====================================

st.set_page_config(
    page_title="Credit Card Customer Analytics",
    page_icon="💳",
    layout="wide"
)

# =====================================
# LOGO / RASM
# =====================================

try:
    img = Image.open("image_2026-06-19_10-04-14.png")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image(img, width=400)

except:
    st.warning("Rasm topilmadi!")

# =====================================
# SARLAVHA
# =====================================

st.markdown(
    """
    <h1 style='text-align:center; color:#1E88E5;'>
        💳 CREDIT CARD CUSTOMERS
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h3 style='text-align:center; color:gray;'>
        Customer Analytics and Churn Prediction Dashboard
    </h3>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# =====================================
# DATASET YUKLASH
# =====================================

@st.cache_data
def load_data():

    df = pd.read_csv("BankChurners.csv")

    df = df.drop(
        columns=[
            "CLIENTNUM",
            "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1",
            "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2"
        ],
        errors="ignore"
    )

    return df

try:

    df = load_data()

    # =====================================
    # SIDEBAR
    # =====================================

    page = st.sidebar.selectbox(
        "📋 Menyu",
        [
            "About Dataset",
            "Visual Dashboard",
            "Customer Analysis",
            "Prediction",
            "Team"
        ]
    )

    # =====================================
    # ABOUT DATASET
    # =====================================

    if page == "About Dataset":

        st.header("📊 Dataset haqida")

        st.write("""
        Ushbu dataset bankning kredit karta mijozlari haqidagi
        ma'lumotlarni o'z ichiga oladi.

        Loyihaning asosiy maqsadi —
        bankni tark etishi mumkin bo'lgan
        mijozlarni aniqlashdir.
        """)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Mijozlar soni", len(df))

        with col2:
            st.metric("Ustunlar soni", len(df.columns))

        st.subheader("Datasetning dastlabki 5 qatori")

        st.dataframe(df.head())

    # =====================================
    # VISUAL DASHBOARD
    # =====================================

    elif page == "Visual Dashboard":

        st.header("📈 Visual Dashboard")

        total_customers = len(df)

        existing = len(
            df[df["Attrition_Flag"] == "Existing Customer"]
        )

        attrited = len(
            df[df["Attrition_Flag"] == "Attrited Customer"]
        )

        avg_credit = round(
            df["Credit_Limit"].mean(),
            2
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "👥 Total Customers",
                total_customers
            )

        with col2:
            st.metric(
                "✅ Existing Customers",
                existing
            )

        with col3:
            st.metric(
                "❌ Attrited Customers",
                attrited
            )

        with col4:
            st.metric(
                "💳 Avg Credit Limit",
                f"${avg_credit:,.2f}"
            )

        st.markdown("---")

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

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(
                fig1,
                use_container_width=True
            )

        with col2:
            st.plotly_chart(
                fig2,
                use_container_width=True
            )

    # =====================================
    # CUSTOMER ANALYSIS
    # =====================================

    elif page == "Customer Analysis":

        st.header("👨‍💼 Customer Analysis")

        gender = st.selectbox(
            "Select Gender",
            ["All"] + list(df["Gender"].unique())
        )

        filtered_df = df.copy()

        if gender != "All":
            filtered_df = filtered_df[
                filtered_df["Gender"] == gender
            ]

        fig = px.box(
            filtered_df,
            x="Card_Category",
            y="Credit_Limit",
            color="Attrition_Flag",
            title="Credit Limit by Card Category"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Filtered Dataset")

        st.dataframe(filtered_df)

    # =====================================
    # PREDICTION
    # =====================================

    elif page == "Prediction":

        st.header("🔮 Customer Churn Prediction")

        age = st.slider(
            "Customer Age",
            18,
            80,
            35
        )

        credit = st.number_input(
            "Credit Limit",
            min_value=1000,
            max_value=50000,
            value=10000
        )

        transactions = st.number_input(
            "Total Transactions",
            min_value=1,
            max_value=200,
            value=50
        )

        if st.button("Predict"):

            if transactions < 40 and credit > 15000:

                st.error(
                    "⚠️ High Risk of Attrition"
                )

            else:

                st.success(
                    "✅ Customer Likely to Stay"
                )

    # =====================================
    # TEAM
    # =====================================

    elif page == "Team":

        st.header("👥 Contributors")

        st.write("👩‍💻 Nargiza")
        st.write("👩‍💻 Maqsuda")
        st.write("👩‍💻 Munisa")

        st.success(
            "Loyiha jamoasi tomonidan tayyorlandi."
        )

except FileNotFoundError:

    st.error(
        "❌ BankChurners.csv fayli topilmadi!"
    )

    st.info(
        "CSV faylni app.py bilan bir papkaga joylashtiring."
    )

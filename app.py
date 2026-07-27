import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Yarn Quality Dashboard",
    page_icon="🧵",
    layout="wide"
)

st.title("🧵 Quality Control Dashboard")
st.subheader("تحليل جودة الخيوط")

uploaded_file = st.file_uploader(
    "تحميل ملف الجودة",
    type=["xlsx","xls","csv"]
)

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("تم تحميل البيانات بنجاح")

    st.dataframe(df)

    st.divider()

    st.header("📊 مؤشرات الجودة")

    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.metric(
            "متوسط IPI",
            round(df["IPI"].mean(),0)
        )

    with col2:
        st.metric(
            "متوسط RKM",
            round(df["RKM"].mean(),2)
        )

    with col3:
        st.metric(
            "متوسط Bforce",
            round(df["Bforce"].mean(),0)
        )

    with col4:
        st.metric(
            "متوسط CVm%",
            round(df["C.V m"].mean(),2)
        )

    with col5:
        st.metric(
            "عدد النمر",
            df["Act.Count"].nunique()
        )

    st.divider()

    st.header("📈 تحليل النمر")

    summary = df.groupby("Product").agg({
        "Act.Count":"mean",
        "THIN":"mean",
        "THICK":"mean",
        "NEPS":"mean",
        "IPI":"mean",
        "RKM":"mean",
        "ELG":"mean",
        "Bforce":"mean",
        "C.V m":"mean"
    }).reset_index()

    def quality_rating(row):

        score = 100

        if row["IPI"] > 250:
            score -= 30

        if row["C.V m"] > 14:
            score -= 20

        if row["RKM"] < 15:
            score -= 20

        if row["Bforce"] < 300:
            score -= 20

        if row["THIN"] > 5:
            score -= 5

        if row["THICK"] > 100:
            score -= 5

        if score >= 85:
            return "ممتاز"

        elif score >= 70:
            return "جيد"

        elif score >= 50:
            return "مقبول"

        else:
            return "ضعيف"

    summary["التقييم"] = summary.apply(
        quality_rating,
        axis=1
    )

    st.dataframe(
        summary,
        use_container_width=True
    )

    st.divider()

    st.header("📋 استنتاجات الجودة")

    for _, row in summary.iterrows():

        notes = []

        if row["IPI"] > 250:
            notes.append("ارتفاع إجمالي العيوب")

        if row["THIN"] > 5:
            notes.append("ارتفاع أماكن الرفيع")

        if row["THICK"] > 100:
            notes.append("ارتفاع أماكن السميك")

        if row["NEPS"] > 150:
            notes.append("زيادة النبس")

        if row["RKM"] < 15:
            notes.append("انخفاض المتانة")

        if row["Bforce"] < 300:
            notes.append("انخفاض قوة الشد")

        if row["C.V m"] > 14:
            notes.append("عدم انتظامية مرتفعة")

        if len(notes) == 0:
            notes.append("جودة مستقرة ومطابقة للمواصفات")

        st.info(
            f"""
            المنتج : {row['Product']}

            التقييم : {row['التقييم']}

            {" | ".join(notes)}
            """
        )

    st.divider()

    st.header("📊 الرسوم البيانية")

    fig1 = px.bar(
        summary,
        x="Product",
        y="IPI",
        color="التقييم",
        title="IPI حسب النمرة"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    fig2 = px.bar(
        summary,
        x="Product",
        y="RKM",
        color="التقييم",
        title="RKM حسب النمرة"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    fig3 = px.bar(
        summary,
        x="Product",
        y="Bforce",
        color="التقييم",
        title="قوة الشد حسب النمرة"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.divider()

    st.header("🔍 فلترة حسب النمرة")

    selected_product = st.selectbox(
        "اختر نمرة",
        df["Product"].unique()
    )

    filtered = df[
        df["Product"] == selected_product
    ]

    st.dataframe(
        filtered,
        use_container_width=True
    )

    st.download_button(
        "📥 تحميل البيانات",
        filtered.to_csv(
            index=False
        ).encode("utf-8-sig"),
        file_name="quality_data.csv",
        mime="text/csv"
    )

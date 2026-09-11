import streamlit as st
import pandas as pd

st.set_page_config(page_title="Evacon AI System", layout="wide")

# تخصيص الاتجاه للعربية وتنسيق الخط
st.markdown("""
    <style>
    body, [data-testid="stAppViewContainer"] {
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stTextInput>div>div>input {
        text-align: right;
        direction: rtl;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏢 محرك البحث العقاري - Evacon AI")
st.caption("نظام الاستعلام الذكي عن المشاريع، الوحدات، والأسعار")

@st.cache_data
def load_data():
    path = "EVACON_REAL_ESTATE_MASTER_DATABASE.xlsx"
    df_devs = pd.read_excel(path, sheet_name="01_DEVELOPERS")
    df_projs = pd.read_excel(path, sheet_name="02_PROJECTS")
    df_units = pd.read_excel(path, sheet_name="03_UNITS")
    df_plans = pd.read_excel(path, sheet_name="04_PAYMENT_PLANS")
    df_notes = pd.read_excel(path, sheet_name="05_COMMERCIAL_NOTES")

    m = df_units.merge(df_projs, on="Project_ID", how="left")
    m = m.merge(df_devs, on="Developer_ID", how="left")
    m = m.merge(df_plans, on="Unit_ID", how="left")
    m = m.merge(df_notes, on="Unit_ID", how="left")
    return m

df = load_data()

col1, col2, col3, col4 = st.columns(4)
col1.metric("إجمالي الوحدات", len(df))
col2.metric("المشاريع المتاحة", df["Project_Name"].nunique())
col3.metric("المطورين", df["Developer_Name"].nunique())
col4.metric("المواقع المغطاة", df["Normalized_Location"].nunique())

st.divider()

search_term = st.text_input("ابحث عن أي شيء (اسم مشروع، مطور، منطقة، نوع وحدة):", placeholder="مثال: العاصمة، Makan، تجاري، زايد...")

if search_term:
    q = search_term.strip().lower()
    results = df[
        df["Developer_Name"].astype(str).str.lower().str.contains(q, na=False) |
        df["Project_Name"].astype(str).str.lower().str.contains(q, na=False) |
        df["Normalized_Location"].astype(str).str.lower().str.contains(q, na=False) |
        df["Unit_Type"].astype(str).str.lower().str.contains(q, na=False)
    ]
    
    st.write(f"تم العثور على **{len(results)}** نتيجة:")
    
    for _, row in results.iterrows():
        with st.expander(f"📌 {row['Project_Name']} - {row['Unit_Type']} ({row['Normalized_Location']})"):
            c1, c2, c3 = st.columns(3)
            
            p_exact = f"{row['Exact_Price']:,.0f} ج" if pd.notna(row['Exact_Price']) else None
            p_start = f"يبدأ من {row['Starting_Price']:,.0f} ج" if pd.notna(row['Starting_Price']) else None
            price = p_exact or p_start or "غير محدد"
            
            c1.write(f"**المطور:** {row['Developer_Name']}")
            c1.write(f"**المساحة:** {row['Area_m2']} م²" if pd.notna(row['Area_m2']) else "**المساحة:** غير محددة")
            c1.write(f"**السعر:** {price}")
            
            meter_p = f"{row['Price_Per_m2']:,.0f} ج/م²" if pd.notna(row['Price_Per_m2']) else "غير متوفر"
            dp = f"{row['Down_Payment_Percent']*100:.0f}%" if pd.notna(row['Down_Payment_Percent']) else "غير محدد"
            
            c2.write(f"**سعر المتر:** {meter_p}")
            c2.write(f"**نسبة المقدم:** {dp}")
            c2.write(f"**فترة السداد:** {row.get('Installment_Period', 'غير مدونة')}")
            
            c3.write(f"**الاستشاري:** {row.get('Consultant', 'غير مدون')}")
            c3.write(f"**التشطيب:** {row.get('Finishing', 'غير مدون')}")
            c3.write(f"**موعد الاستلام:** {row.get('Delivery_Date', 'غير مدون')}")
            
            if pd.notna(row.get('Commercial_Highlights')):
                st.info(f"💡 **تفاصيل ومميزات:** {row['Commercial_Highlights']}")
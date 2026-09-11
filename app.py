for _, row in results.iterrows():
        # استخراج وتحديد الموقع الأدق المتاح
        raw_loc = row.get('Location_Raw', '')
        norm_loc = row.get('Normalized_Location', '')
        
        # اختيار العنوان الأدق (الخام أولاً إذا كان يحمل تفاصيل أكثر)
        detailed_location = raw_loc if pd.notna(raw_loc) and str(raw_loc).strip() != '' else norm_loc
        
        with st.expander(f"📌 {row['Project_Name']} - {row['Unit_Type']} ({detailed_location})"):
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
            
            # خانة الموقع الدقيق والتشطيب
            c3.write(f"📍 **الموقع التفصيلي:** {detailed_location}")
            c3.write(f"**التشطيب:** {row.get('Finishing', 'غير مدون')}")
            c3.write(f"**موعد الاستلام:** {row.get('Delivery_Date', 'غير مدون')}")
            
            if pd.notna(row.get('Commercial_Highlights')):
                st.info(f"💡 **تفاصيل ومميزات الموقع الإضافية:** {row['Commercial_Highlights']}")
            
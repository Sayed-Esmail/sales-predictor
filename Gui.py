import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import io
import xlsxwriter

# === Load the trained model ===
model = joblib.load("sales_model.pkl")
feature_names = model.feature_names_in_

# === Page setup ===
st.set_page_config(page_title="Sales Predictor", page_icon="💰")
st.title("💰 Sales Prediction Web App")
st.markdown("This app predicts sales amount based on product & customer features.")

# === Helper for safe one-hot encoding ===
def safe_one_hot(input_dict, field_name, value, valid_features):
    col = f"{field_name}_{value}"
    if col in valid_features:
        input_dict[col] = 1

# === Sidebar inputs ===
st.sidebar.header("Input Features")

# Numeric inputs
quantity = st.sidebar.number_input("Quantity", min_value=1, max_value=100, value=5)
price = st.sidebar.number_input("Price", min_value=0.0, max_value=10000.0, value=20.0)
cost = st.sidebar.number_input("Cost", min_value=0.0, max_value=10000.0, value=15.0)
customer_age = st.sidebar.slider("Customer Age", 18, 90, 35)
order_month = st.sidebar.selectbox("Order Month", list(range(1, 13)))
order_dayofweek = st.sidebar.selectbox("Order Day of Week (0 = Monday)", list(range(0, 7)))

# Categorical inputs
category_options = {
    "Bikes": ["Mountain Bikes", "Road Bikes", "Touring Bikes"],
    "Clothing": ["Jerseys", "Shorts", "Caps", "Gloves", "Socks", "Helmets", "Vests"]
}

country = st.sidebar.selectbox("Country", ["Canada", "France", "Germany", "United Kingdom", "United States", "n/a"])
marital_status = st.sidebar.selectbox("Marital Status", ["Married", "Single"])
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "n/a"])
category = st.sidebar.selectbox("Category", list(category_options.keys()))
subcategory = st.sidebar.selectbox("Subcategory", category_options[category])
maintenance = st.sidebar.selectbox("Maintenance Included?", ["Yes", "No"])
product_line = st.sidebar.selectbox("Product Line", ["Other Sales", "Road", "Touring"])

# === Create input dictionary ===
input_dict = dict.fromkeys(feature_names, 0)
input_dict.update({
    "quantity": quantity,
    "price": price,
    "cost": cost,
    "order_month": order_month,
    "order_dayofweek": order_dayofweek,
    "customer_age": customer_age,
})
safe_one_hot(input_dict, "country", country, feature_names)
safe_one_hot(input_dict, "gender", gender, feature_names)
safe_one_hot(input_dict, "category", category, feature_names)
safe_one_hot(input_dict, "subcategory", subcategory, feature_names)
safe_one_hot(input_dict, "product_line", product_line, feature_names)
if "marital_status_Single" in feature_names and marital_status == "Single":
    input_dict["marital_status_Single"] = 1
if "maintenance_Yes" in feature_names and maintenance == "Yes":
    input_dict["maintenance_Yes"] = 1

input_df = pd.DataFrame([input_dict])
st.subheader("🧾 Input Preview")
st.write(input_df)

if st.button("🔮 Predict"):
    try:
        prediction = model.predict(input_df)[0]
        st.success(f"💵 Predicted Sales Amount: ${prediction:,.2f}")
    except Exception as e:
        st.error(f"Prediction error: {e}")

# === Show feature importance ===
try:
    st.subheader("📊 Top 10 Feature Importances")
    importances = model.feature_importances_
    importance_df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
    importance_df = importance_df.sort_values(by="Importance", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=importance_df, x="Importance", y="Feature", ax=ax, palette="Blues_d")
    st.pyplot(fig)
except Exception as e:
    st.error(f"Feature importance plot error: {e}")

# === Download Smart Template ===
st.markdown("## 📄 Download Excel Template with Dropdowns")
output_template = io.BytesIO()
with pd.ExcelWriter(output_template, engine='xlsxwriter') as writer:
    workbook = writer.book
    worksheet = workbook.add_worksheet("sales_input_template")
    writer.sheets["sales_input_template"] = worksheet

    headers = [
        "quantity", "price", "cost", "order_month", "order_dayofweek", "customer_age",
        "country", "gender", "marital_status", "category", "subcategory", "maintenance", "product_line"
    ]
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    worksheet.data_validation(1, 0, 1000, 0, {"validate": "integer", "criteria": ">=", "value": 1})
    worksheet.data_validation(1, 1, 1000, 2, {"validate": "decimal", "criteria": ">=", "value": 0})
    worksheet.data_validation(1, 3, 1000, 3, {"validate": "integer", "criteria": "between", "minimum": 1, "maximum": 12})
    worksheet.data_validation(1, 4, 1000, 4, {"validate": "integer", "criteria": "between", "minimum": 0, "maximum": 6})
    worksheet.data_validation(1, 5, 1000, 5, {"validate": "integer", "criteria": "between", "minimum": 18, "maximum": 90})
    worksheet.data_validation(1, 6, 1000, 6, {"validate": "list", "source": ["Canada", "France", "Germany", "United Kingdom", "United States", "n/a"]})
    worksheet.data_validation(1, 7, 1000, 7, {"validate": "list", "source": ["Male", "Female", "n/a"]})
    worksheet.data_validation(1, 8, 1000, 8, {"validate": "list", "source": ["Married", "Single"]})
    worksheet.data_validation(1, 9, 1000, 9, {"validate": "list", "source": list(category_options.keys())})
    worksheet.data_validation(1, 10, 1000, 10, {"validate": "list", "source": sum(category_options.values(), [])})
    worksheet.data_validation(1, 11, 1000, 11, {"validate": "list", "source": ["Yes", "No"]})
    worksheet.data_validation(1, 12, 1000, 12, {"validate": "list", "source": ["Other Sales", "Road", "Touring"]})

st.download_button(
    label="📃 Download Template (Excel with dropdowns)",
    data=output_template.getvalue(),
    file_name="sales_input_template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# === File Upload for Prediction ===
st.markdown("## 📄 Bulk Prediction Upload")
uploaded_file = st.file_uploader("Upload CSV or Excel file:", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            raw_df = pd.read_csv(uploaded_file)
        else:
            raw_df = pd.read_excel(uploaded_file)

        encoded_df = pd.DataFrame()
        for col in ["country", "gender", "category", "subcategory", "product_line"]:
            dummies = pd.get_dummies(raw_df[col], prefix=col)
            encoded_df = pd.concat([encoded_df, dummies], axis=1)

        if "marital_status" in raw_df.columns and "marital_status_Single" in feature_names:
            encoded_df["marital_status_Single"] = (raw_df["marital_status"] == "Single").astype(int)
        if "maintenance" in raw_df.columns and "maintenance_Yes" in feature_names:
            encoded_df["maintenance_Yes"] = (raw_df["maintenance"] == "Yes").astype(int)

        numeric_cols = ["quantity", "price", "cost", "order_month", "order_dayofweek", "customer_age"]
        encoded_df[numeric_cols] = raw_df[numeric_cols]

        for col in feature_names:
            if col not in encoded_df.columns:
                encoded_df[col] = 0
        encoded_df = encoded_df[feature_names]

        encoded_df['Predicted_Sales_Amount'] = model.predict(encoded_df)
        st.success("✅ Bulk predictions complete.")
        st.dataframe(encoded_df.head(10))

        st.subheader("📈 Prediction Summary")
        total = encoded_df['Predicted_Sales_Amount'].sum()
        avg = encoded_df['Predicted_Sales_Amount'].mean()
        st.metric("Total Predicted Revenue", f"${total:,.2f}")
        st.metric("Average Predicted Sale", f"${avg:,.2f}")

        out = io.BytesIO()
        with pd.ExcelWriter(out, engine="xlsxwriter") as writer:
            encoded_df.to_excel(writer, index=False)
        st.download_button("Download Results", out.getvalue(), "sales_predictions.xlsx")
    except Exception as e:
        st.error(f"Error processing file: {e}")

# === Footer ===
st.markdown("---")
st.markdown("<center>Created by Sayed Esmail | Sales Predictor</center>", unsafe_allow_html=True)

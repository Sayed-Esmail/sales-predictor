# Sales Prediction Web Application

## Project Overview
This project delivers a web-based sales prediction application built with Streamlit. It leverages a pre-trained machine learning model to forecast sales amounts based on various product and customer features. The application provides an intuitive user interface for individual predictions and supports bulk predictions via file uploads, making it a versatile tool for sales forecasting and analysis.

## Features
- **Interactive Sales Prediction**: Predict sales amounts by adjusting various input features through a user-friendly sidebar.
- **Feature Importance Visualization**: Understand the key drivers of sales predictions through a dynamic bar chart displaying feature importances.
- **Excel Template Download**: Generate a pre-formatted Excel template with data validation dropdowns for easy input of new sales data.
- **Bulk Prediction Upload**: Upload CSV or Excel files containing multiple sales records for batch predictions and download the results.
- **Prediction Summary**: View total predicted revenue and average predicted sales for bulk uploads.

## Project Structure
```
.
├── Gui.py
├── requirements.txt
├── sales_model.pkl
└── README.md
```

## Setup and Usage

### Prerequisites
- Python 3.7+
- `pip` (Python package installer)

### Installation
1. **Clone the repository (if applicable) or download the project files.**
2. **Navigate to the project directory in your terminal.**
3. **Install the required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
To start the Streamlit web application, run the following command in your terminal from the project directory:
```bash
streamlit run Gui.py
```

This will open the application in your default web browser. If it doesn't open automatically, Streamlit will provide a local URL (e.g., `http://localhost:8501`) that you can copy and paste into your browser.

## Machine Learning Model
The core of this application is a pre-trained machine learning model, `sales_model.pkl`. This model was trained on historical sales data to learn the relationships between various features (e.g., quantity, price, customer demographics, product categories) and the sales amount. The `Gui.py` script loads this model and uses it to make predictions.

**Model Details (inferred from `Gui.py`):**
- The model is likely a tree-based ensemble model (e.g., RandomForest, Gradient Boosting) given the `feature_importances_` attribute usage.
- It handles both numerical and categorical features, with categorical features being one-hot encoded during the prediction process.

## Dependencies
The project relies on the following key Python libraries, as listed in `requirements.txt`:
- `streamlit`: For building the interactive web application.
- `pandas`: For data manipulation and handling DataFrames.
- `scikit-learn`: For machine learning functionalities, including model loading and potentially the underlying model algorithm.
- `joblib`: For efficient saving and loading of Python objects, specifically the pre-trained machine learning model.
- `matplotlib` & `seaborn`: For creating data visualizations, specifically the feature importance plot.
- `xlsxwriter` & `openpyxl`: For generating and reading Excel files, used for the template download and bulk upload features.

## Future Enhancements
- Implement model retraining functionality within the application.
- Add more advanced data visualization and reporting features.
- Integrate with a database for real-time data ingestion and prediction storage.
- Deploy the application to a cloud platform for wider accessibility.



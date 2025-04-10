

import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Data File Converter", layout="wide")
st.title("File Converter & Cleaner")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning.")

files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name} Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates Removed")
            st.dataframe(df.head())

        if st.checkbox(f"Fill Missing Values (numerical only) - {file.name}"):
            df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
            st.success("Missing values filled with mean")
            st.dataframe(df.head())

        selected_columns = st.multiselect(f"Select Columns to Keep - {file.name}", options=df.columns.tolist(), default=df.columns.tolist())
        df = df[selected_columns]
        st.dataframe(df.head())

        if st.checkbox(f"Show Chart - {file.name}"):
            numeric_df = df.select_dtypes(include=["number"])
            if not numeric_df.empty:
                st.bar_chart(numeric_df.iloc[:, :2])
            else:
                st.warning("No numerical columns to show in chart.")

        format_choice = st.radio(f"Convert {file.name} to:", options=["csv", "Excel"], key=file.name)

        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()
            new_name = file.name.rsplit(".", 1)[0]

            if format_choice == "csv":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name += ".csv"
            else:
                df.to_excel(output, index=False, engine="openpyxl")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name += ".xlsx"

            st.download_button(
                label=f"Download {new_name}",
                data=output.getvalue(),
                file_name=new_name,
                mime=mime
            )

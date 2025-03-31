
import streamlit as st
import pandas as pd
import plotly.express as px

# Load initial data from Excel
@st.cache_data
def load_data():
    df_entry = pd.read_excel("experiment.xlsm", sheet_name="System_Entry", engine="openpyxl")
    df_report = pd.read_excel("experiment.xlsm", sheet_name="System_Report", engine="openpyxl", skiprows=4)
    return df_entry, df_report

df_entry, df_report = load_data()

st.title("System Entry & Report Dashboard")

# --- Sidebar Form for Data Entry ---
st.sidebar.header("Add New System")
with st.sidebar.form("entry_form"):
    system_id = st.text_input("System ID")
    description = st.text_input("System Description")
    submitted = st.form_submit_button("Submit")

    if submitted:
        new_row = pd.DataFrame([[system_id, description]], columns=["System ID", "System Description"])
        df_entry = pd.concat([df_entry, new_row], ignore_index=True)
        df_entry.to_excel("updated_system_entry.xlsx", index=False)
        st.sidebar.success("Entry added!")

# --- Main Dashboard Area ---
st.subheader("System Entry Table")
st.dataframe(df_entry)

st.subheader("System Report Overview")

# Filter by system name
systems = df_report.iloc[:, 2].dropna().unique().tolist()
selected_system = st.selectbox("Select System", systems)

filtered_df = df_report[df_report.iloc[:, 2] == selected_system]
st.write(f"Documents for {selected_system}")
st.dataframe(filtered_df)

# Plot Status Summary
if "STATUS" in df_report.columns:
    status_counts = df_report["STATUS"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig = px.pie(status_counts, names="Status", values="Count", title="Document Status Distribution")
    st.plotly_chart(fig)

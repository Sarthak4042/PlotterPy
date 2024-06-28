import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("PlotterPy")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    
    # Display the dataframe
    st.write("Dataframe:")
    st.write(df)
    
    # Include "Total" option in the dropdowns
    columns_with_total = df.columns.tolist()
    
    # Select graph type
    graph_type = st.selectbox("Select graph type", ["Bar", "Line", "Pie"])
    
    if graph_type == "Pie":
        col_a = st.selectbox("Select column for Pie chart total", columns_with_total)
        col_b = st.selectbox("Select column for Pie chart labels", columns_with_total)
        
        if not pd.api.types.is_numeric_dtype(df[col_a]):
            st.error("Pie chart requires numerical data for the total column.")
        else:
            # Calculate the total for col_a
            total_sum = df[col_a].sum()
            
            # Group by col_b and sum col_a
            grouped_data = df.groupby(col_b)[col_a].sum()
            
            # Plotting pie chart
            st.write(f"Plotting Pie chart for {col_a} by {col_b}")
            fig, ax = plt.subplots()
            ax.pie(grouped_data, labels=grouped_data.index, autopct='%1.1f%%')
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            st.pyplot(fig)
    
    else:
        # Select columns for the X and Y axis
        col1 = st.selectbox("Select X-axis column", columns_with_total + ["Total"])
        col2 = st.selectbox("Select Y-axis column", columns_with_total + ["Total"])
        
        # Calculate total row count if "Total" is selected
        if col1 == "Total":
            x_data = ["Total"]
            y_data = [len(df)]
        else:
            x_data = df[col1]
        
        if col2 == "Total":
            y_data = [len(df)] * len(x_data)
        else:
            y_data = df[col2]
        
        # Plotting bar or line chart
        st.write(f"Plotting {col1} vs {col2} as {graph_type} graph")
        fig, ax = plt.subplots()
        
        if graph_type == "Bar":
            ax.bar(x_data, y_data)
        elif graph_type == "Line":
            ax.plot(x_data, y_data, marker='o')
        
        ax.set_xlabel(col1)
        ax.set_ylabel(col2)
        ax.set_title(f"{col1} vs {col2}")
        st.pyplot(fig)

# import libraries
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


def streamlit_used():
    # page config
    st.set_page_config(
        page_title="Used Cars In Nigeria (jiji)",
        layout="wide",
        initial_sidebar_state="expanded"
    )  
        
    #load datast
    df = pd.read_csv("cleaned_jiji_car_dataset.csv")
    
    # header
    st.title("Car Ads in Nigeria (jiji)")
    st.caption("A stragetic overview of car ads in nigeria (jiji)")
    st.markdown("---")
    
    
    # Sidebar Title
    st.sidebar.markdown("## 🧭 Dashboard Filters")
    st.sidebar.markdown("Fine-tune the dashboard using the filters below.")
    
     # car make filter
    car_make_filter = st.sidebar.multiselect(
        "Car Make",
        options=df["make"].unique(),
        default=df["make"].unique()
    )

    # condition filter
    condition_filter = st.sidebar.multiselect(
        "Car Condition",
        options=df["condition"].unique(),
        default=df["condition"].unique()
    )

    # year filter
    year_filter = st.sidebar.multiselect(
        "Car Year",
        options=df["year"].unique(),
        default=df["year"].unique()
    )
    
     # apply filter
    filtered_df = df[
        (df["make"].isin(car_make_filter)) &
        (df["condition"].isin(condition_filter)) &
        (df["year"].isin(year_filter))
    ]
    
     # kpi summary
    total_no_cars = filtered_df["title"].count()
    avg_car_price = round(filtered_df["price"].mean())
    common_car_make = filtered_df["make"].mode()[0]
    per_foreign_used = round((filtered_df["condition"].str.lower() == "foreign used").sum() / total_no_cars * 100, 2)
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total number of car listings", total_no_cars)

    with col2:
        st.metric("Average car price (₦)", f"₦{avg_car_price:,.0f}")

    with col3:
        st.metric("Most common car make", common_car_make)

    with col4:
        st.metric("Percentage of Foreign Used cars (%)", f"{per_foreign_used}%")
        
    st.markdown("---")
        
    
     # row 1 - school type & population distribution 
    left, right = st.columns(2)
    with left:
        make_count = (filtered_df["make"].value_counts().reset_index())
        st.subheader("Bar chart of Count of cars by make")
        make_count.columns = ["Make", "Count"]
        fig_make_count = px.bar(
            make_count,
            x="Make",
            y="Count",
            title="Count of Cars by Make"
        )
        fig_make_count.update_layout(showlegend=False)
        st.plotly_chart(fig_make_count, use_container_width=True)
        
    with right:
        avg_price_make = (filtered_df.groupby("make")["price"].mean().reset_index())
        st.subheader("Bar chart of average price by make")   
        fig_avg_price_make = px.bar(
            avg_price_make,
            x="make",
            y="price",
            title="Average Price by Make",
            labels={"make": "Make", "price": "Average Price (₦)"}
        )
        fig_avg_price_make.update_layout(showlegend=False)
        st.plotly_chart(fig_avg_price_make, use_container_width=True)
        
    st.markdown("---")    
    
    
     # row 2 - school type & population distribution 
    left, right = st.columns(2)
    with left:
        st.subheader("Boxplot of price distribution by condition")
        fig_box = px.box(
            filtered_df,
            x="condition",
            y="price",
            title="Price Distribution by Car Condition",
            labels={"condition": "Condition", "price": "Price (₦)"}
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
    with right:
        st.subheader("Histogram distribution of year")   
        fig_hist = px.histogram(
            filtered_df,
            x="year",
            nbins=30,
            title="Distribution of Car Manufacturing Year"
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
    st.markdown("---")    
    
    
    # row 3 - school type & population distribution 
    left, right = st.columns(2)
    with left:
        st.subheader("Scatter plot of year vs price (colored by condition)")
        fig_scatter = px.scatter(
            filtered_df,
            x="year",
            y="price",
            color="condition",
            title="Year vs Price (Colored by Condition)",
            labels={"year": "Year", "price": "Price (₦)"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with right:
        numeric_df = filtered_df.select_dtypes(include=np.number)
        corr = numeric_df.corr()
        st.subheader("Histogram distribution of year")   
        fig_heatmap = px.imshow(
            corr,
            text_auto=True,
            title="Correlation Heatmap of Numeric Fields"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        
    st.markdown("---")
    
    # data overview
    st.subheader("Data Preview")
    st.dataframe(filtered_df.head(10))
    

    
streamlit_used()
import pandas as pd
import streamlit as st


def load_data():
    df = pd.read_excel('Coffee_sales.xlsx')
    # replace the NaN with "none"/"Non-Card"
    df.loc[:,"card"]=df.card.fillna("non-card")
    return df

try:
    df = load_data()

    st.title("Coffee Sales App")

     #filters
    filters={
        "coffee_name":df["coffee_name"].unique(),
        "Time_of_Day":df["Time_of_Day"].unique(),
        "Month_name":df["Month_name"].unique(),
        "Cash_type":df["cash_type"].unique(),
        "Weekday":df["Weekday"].unique(),
}
    # store user selection
    selected_filters = {}

    #generate multi-select widgets dynamically
    for key, options in filters.items():
        selected_filters[key] = st.sidebar.multiselect(key,options)

        # take a copy of data
        filtered_df = df.copy()
            
        #apply filter selection to the data
        for key, selected_values in selected_filters.items():
            if selected_values:
                filtered_df = filtered_df[filtered_df[key].isin(selected_values)]

    #display the data
    st.dataframe(filtered_df)

    #section 2: calculations
    no_of_cups=len(filtered_df)
    total_revenue=filtered_df["money"].sum()
    avg_sale=filtered_df["money"].mean()
    perct_sales=f"{(total_revenue/df["money"].sum()) * 100:,.2f}%"

    # display a quick overview using metrics

    st.write("### Quick Overview")

    # streamlit column components
    col1,col2,col3,col4=st.columns(4)

    with col1:
        st.metric("Cups Sold:", no_of_cups)

    with col2:
        st.metric("Revenue:",f"{total_revenue:,.2f}")

    with col3:
        st.metric("Avg Sale:",f"{avg_sale:,.2f}")

    with col4:
        st.metric("Percentage Contribution to sales: ", perct_sales)


        st.write("### Analysis findings")

        temp_1=df["Time_of_Day"].value_counts().reset_index()
        temp_1.columns=["Time_of_Day","Cups sold"]

        st.dataframe(temp_1)

        # simple chart
        import altair as alt

        chart_1=alt.Chart(temp_1).mark_bar().encode(
            x=alt.X("Cups sold:Q"),
            y=alt.Y("Time_of_Day:N"), 
            color=alt.Color("Time of Day:N", legend=None)

        ).properties(height=250)

        # display the chart
        st.altair_chart(chart_1, use_container_width=True)


        # Top coffee types
        st.write("### Revenue by Coffee Types")
        temp_2= filtered_df.groupby("coffee_name")["money"].sum().reset_index().sort_values(by="money", ascending=False)
        # temp_2.columns=[]

        st.dataframe(temp_2)

except Exception as e:
    st.error("Error: check error details")

    with st.expander("Error Details"):
        st.code(str(e))
        # st.code(traceback.format_exc())
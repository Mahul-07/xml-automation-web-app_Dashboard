import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="XML Dashboard",
                    page_icon=":bar_chart:",
                    layout="wide"
)

df = pd.read_excel(
    io='log.xlsx',
    engine='openpyxl',

)

new_df = df.astype(str)
col11, col12, col13 = st.columns(3)

with col11:
    st.write(' ')

with col12:
    st.title(":bar_chart: Xml Dashboard")

with col13:
    st.write(' ')
# st.title(":bar_chart: Xml Dashboard")
st.markdown("##")
new_df['Date'] = pd.to_datetime(new_df['Date']).dt.date


st.header("Please Filter Here:")


col1, col2, col3, col4 = st.columns(4)

with col1:
    module_name = st.selectbox(
    "Select the Module Name",
    options=df["ModuleName"].unique(),
)

with col2:
   start_date = st.date_input(
    "Start Date", 
    value=pd.to_datetime(new_df['Date'].loc[0])
)

with col3:
    end_date = st.date_input(
    "End Date", 
    value=pd.to_datetime("today")
)

with col4:
    user_name = st.multiselect(
    "Select the User:",
    options=df["User"].unique(),
    default=df["User"].unique()
)


st.markdown('------')


if start_date < end_date:
    pass
else:
    st.error('Error: You have enter wrong start date')

mask = (new_df['Date'] > start_date) & (new_df['Date'] <= end_date)
new_df = new_df.loc[mask]

df_selection = df.query(
    "ModuleName == @module_name & User == @user_name"
)

hide_style="""
        <style>
        #MainMenu {visibility:hidden;}
        footer {visibility:hidden;}
        header {visibilty:hidden;}
        </style>
        """
st.markdown(hide_style,unsafe_allow_html=True)
col5, col6 = st.columns([3,1])
date_count=df_selection['Date'].value_counts()
fig = px.bar(
        date_count,
        title="<b>Date</b>",
        template="plotly_white",
    )
fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

# first chart title
col5.markdown('**Date wise selected module execution graph for selected date range**')

col5.bar_chart(date_count)
col6.write(date_count)
st.markdown('--------')


col15,col16 = st.columns([3,1])
fig4 = px.bar(
        new_df['Date'],
        # second chart title
        title="<b>Month wise selected module execution graph for selected months</b>",
        template="plotly_white",
    )
fig4.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

col15.plotly_chart(fig4)
col16.write(new_df['Date'])
st.markdown('------')


col7, col8 = st.columns([3,1])
fig1 = px.pie(
    df_selection,
    names='User',
    # Third chart title
    title="<b>Total selected module execution graph for each user</b>"
)

col7.plotly_chart(fig1)
col8.write(df_selection['User'].value_counts())
st.markdown('-----------------')

col9, col10 = st.columns([3,1])
module_count =df['ModuleName'].value_counts()
fig3 = px.bar(
    module_count,
    title="<b>Module Name</b>",
    template="plotly_white",
)
fig3.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",

)
# fourth chart title
col9.markdown('**All modules total execution graph for selected date range**')

col9.bar_chart(module_count)
col10.write(module_count)
st.markdown('-----------------')


df_selection=df_selection.drop(['Status','Message','FileCount','StartTime','EndTime','IP','JobID'],axis=1)

col11, col12, col13 = st.columns(3)

with col11:
    st.write(' ')

with col12:
    # Table title
    st.markdown('**Detailed view of data**')
    st.dataframe(df_selection)
    

with col13:
    st.write(' ')
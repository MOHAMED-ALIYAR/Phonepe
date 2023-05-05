
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlalchemy


#data in csv

df = pd.read_csv("CSV/Agg_trans.csv")
state = pd.read_csv("CSV/Longitude_Latitude_State_Table.csv")
districts = pd.read_csv("CSV/Data_Map_Districts_Longitude_Latitude.csv")
districts_tran = pd.read_csv("CSV/district_map_transaction.csv")
app_opening = pd.read_csv("CSV/district_registering_map.csv")
user_device = pd.read_csv("CSV/user_by_device.csv")




# title
st.markdown("<h1 style='text-align: center; color: purple;'>PhonePe Pulse Data Analysis </h1>", unsafe_allow_html=True)



#top states data
st.write('# :red[TOP 5 STATES DATA]')
c1,c2=st.columns(2)
with c1:
    Year = st.selectbox(
            'Select the Year',
            ('2022', '2021','2020','2019','2018'),key='y1h2k')
with c2:
    Quarter = st.selectbox(
            'Select the Quatrer',
            ('1', '2', '3','4'),key='qgwe2')
Data_Map_User_df=app_opening.copy() 
top_states=Data_Map_User_df.loc[(Data_Map_User_df['Year'] == int(Year)) & (Data_Map_User_df['Quater'] ==int(Quarter))]
top_states_r = top_states.sort_values(by=['Registered_user'], ascending=False)
top_states_a = top_states.sort_values(by=['App_opening'], ascending=False) 

Data_Aggregated_Transaction_df=df.copy()
top_states_T=Data_Aggregated_Transaction_df.loc[(Data_Aggregated_Transaction_df['Year'] == int(Year)) & (Data_Aggregated_Transaction_df['Quater'] ==int(Quarter))]
topst=top_states_T.groupby('State')
x=topst.sum().sort_values(by=['Transacion_count'], ascending=False)
y=topst.sum().sort_values(by=['Transacion_amount'], ascending=False)


c1,c2,c3,c4= st.tabs(['Registered_user','App_openings','Transaction_count','Transaction_amount'])
#geo_analysis, Device_analysis, payment_analysis, transac_yearwise = st.tabs(
#    ["Geographical analysis", "User device analysis", "Payment Types analysis", "Transacion analysis of States"])
with c1:
    
    st.subheader('Registered User')
    rt=top_states_r[1:6]
    st.markdown(rt[[ 'State','Registered_user']].style.hide(axis="index").to_html(), unsafe_allow_html=True)
    z= px.pie(rt, values='Registered_user',names='State', hole=.5)
    st.plotly_chart(z)
with c2:
    at=top_states_a[1:6]
    st.subheader("App Openings")
    st.markdown(at[['State','App_opening']].style.hide(axis="index").to_html(), unsafe_allow_html=True)
    z1= px.pie(rt, values='App_opening',names='State', hole=.5)
    st.plotly_chart(z1)
with c3:
    st.subheader("Transactions Count")
    z3=pd.DataFrame(x[['Transacion_count']][1:6])
    st.write(z3)
    z4= px.pie(z3, values='Transacion_count', hole=.5)
    st.plotly_chart(z4)    
    
with c4:
    st.subheader("Transaction Amount ")
    z5=(y['Transacion_amount'][1:6])   
    st.write(z5)
    z6= px.pie(z5, values='Transacion_amount', hole=.5)
    st.plotly_chart(z6)
    


# total transaction amount in bar and pie

with st.container():
    st.subheader('Total Transaction amount in bar chart')
    ab= pd.read_csv("CSV/top_tran.csv")
    c=ab.reset_index()
    b=ab.groupby(['State']).sum()[['Transaction_amount','Transaction_count']]
    e=b.reset_index()
    d= px.bar(e,x='State',y='Transaction_amount')
    st.plotly_chart(d)
    st.subheader('Total Transaction amount in pie chart')
    e= px.pie(e, values='Transaction_amount',names='State', hole=.5)
    st.plotly_chart(e)



#amount and count

ta,tc,st1= st.tabs(
    ["Transaction_amount",'Transaction_count','Registerd_user'])




#transcation amount data

with ta:
    d=pd.read_csv(r"C:\Users\admin\Capstone\Phonepe\CSV\Agg_trans.csv")
    #ye= int(st.radio('Select the Year',('2018', '2019', '2020', '2021', '2022'), horizontal=True, key='ye'))
    a=d.groupby(['State','Year']).sum()['Transacion_amount']
    a.reset_index()
   
    li=px.line(d,x='Year',y='Transacion_amount',color='State')
    st.plotly_chart(li)

with tc:
    e=pd.read_csv(r"C:\Users\admin\Capstone\Phonepe\CSV\Agg_trans.csv")
    b=d.groupby(['State','Year']).sum()['Transacion_count']
    b.reset_index()
   
    li2=px.line(df,x='Year',y='Transacion_count',color='State')
    st.plotly_chart(li2)

with st1:
    st.subheader(
        ':violet[Registered user & App installed -> State and Districtwise:]')
    st.write(' ')
    scatter_year = st.selectbox('Select the Year',
                                ('2018', '2019', '2020', '2021', '2022'))
    st.write(' ')
    scatter_state = st.selectbox('Select the State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                         'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                         'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                         'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                         'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                         'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                         'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                         'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                         'uttarakhand', 'west-bengal'), index=10)
    scatter_year = int(scatter_year)
    scatter_reg_df = app_opening[(app_opening['Year'] == scatter_year) & (
        app_opening['State'] == scatter_state)]
    scatter_register = px.scatter(scatter_reg_df, x="District", y="Registered_user",  color="District",
                                  hover_name="District", hover_data=['Year', 'Quater', 'App_opening'], size_max=60)
    st.plotly_chart(scatter_register)
st.write(' ')



# preperation for geo visualization

state = state.sort_values(by='state')
state = state.reset_index(drop=True)
df2 = df.groupby(['State']).sum()[['Transacion_count', 'Transacion_amount']]
df2 = df2.reset_index()

choropleth_data = state.copy()

for column in df2.columns:
    choropleth_data[column] = df2[column]
choropleth_data = choropleth_data.drop(labels='State', axis=1)

df.rename(columns={'State': 'state'}, inplace=True)
sta_list = ['andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
            'assam', 'bihar', 'chandigarh', 'chhattisgarh',
            'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
            'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
            'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
            'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
            'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
            'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
            'uttarakhand', 'west-bengal']
state['state'] = pd.Series(data=sta_list)
state_final = pd.merge(df, state, how='outer', on='state')
districts_final = pd.merge(districts_tran, districts,
                           how='outer', on=['State', 'District'])


geo_analysis, Device_analysis, payment_analysis, transac_yearwise = st.tabs(
    ["Country analysis", "Brand analysis", "Payment Use analysis", "Transacion analysis of States"])



with geo_analysis:
    st.subheader(':violet[Transaction analysis State and District]')
    st.write(' ')
    Year = st.radio('Please select the Year',
                    ('2018', '2019', '2020', '2021', '2022'), horizontal=True)
    st.write(' ')
    Quarter = st.radio('Please select the Quarter',
                       ('1', '2', '3', '4'), horizontal=True)
    st.write(' ')
    Year = int(Year)
    Quarter = int(Quarter)
    plot_district = districts_final[(districts_final['Year'] == Year) & (
        districts_final['Quater'] == Quarter)]
    plot_state = state_final[(state_final['Year'] == Year)
                             & (state_final['Quater'] == Quarter)]
    plot_state_total = plot_state.groupby(
        ['state', 'Year', 'Quater', 'Latitude', 'Longitude']).sum()
    plot_state_total = plot_state_total.reset_index()
    state_code = ['AN', 'AD', 'AR', 'AS', 'BR', 'CH', 'CG', 'DNHDD', 'DL', 'GA',
                  'GJ', 'HR', 'HP', 'JK', 'JH', 'KA', 'KL', 'LA', 'LD', 'MP', 'MH',
                  'MN', 'ML', 'MZ', 'NL', 'OD', 'PY', 'PB', 'RJ', 'SK', 'TN', 'TS',
                  'TR', 'UP', 'UK', 'WB']
    plot_state_total['code'] = pd.Series(data=state_code)
    fig1 = px.scatter_geo(plot_district,
                          lon=plot_district['Longitude'],
                          lat=plot_district['Latitude'],
                          color=plot_district['Transaction_amount'],
                          size=plot_district['Transaction_count'],
                          hover_name="District",
                          hover_data=["State", 'Transaction_amount', 'Transaction_amount',
                                      'Transaction_count', 'Year', 'Quater'],
                          title='District',
                          size_max=22,)
    fig1.update_traces(marker={'color': "#CC0044",
                               'line_width': 1})
    fig2 = px.scatter_geo(plot_state_total,
                          lon=plot_state_total['Longitude'],
                          lat=plot_state_total['Latitude'],
                          hover_name='state',
                          text=plot_state_total['code'],
                          hover_data=['Transacion_count',
                                      'Transacion_amount', 'Year', 'Quater'],
                          )
    fig2.update_traces(marker=dict(color="#D5FFCC", size=0.3))
    fig = px.choropleth(
        choropleth_data,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='Transacion_amount',
        color_continuous_scale='twilight',
        hover_data=['Transacion_count', 'Transacion_amount']
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.add_trace(fig1.data[0])
    fig.add_trace(fig2.data[0])
    fig.update_layout(height=1000, width=1000)
    st.write(' ')
    st.write(' ')
        
    st.plotly_chart(fig)
    
    
# Device analysis statewise
with Device_analysis:
    #with st.container():
    a1=px.scatter(user_device,x='Year',y='Brand_count',color='Brand',hover_name='Brand_percentage',title='Scatter chart analysis')

    st.plotly_chart(a1)
   #barchart
    bar_user = px.bar(user_device, x='Brand', y='Brand_count', color='Brand',
                      title='Bar chart analysis')
    st.plotly_chart(bar_user)
# Payment type analysis of Transacion data 
with payment_analysis:
    st.subheader(':black[Payment type Analysis]')

    payment_mode = pd.read_csv(r"C:\Users\admin\Capstone\Phonepe\CSV\Agg_trans.csv")
    pie_pay_mode_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                              'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                              'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                              'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                              'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                              'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                              'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                              'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                              'uttarakhand', 'west-bengal'), index=10, key='pie_pay_mode_state')
    pie_pay_mode_year = int(st.radio('Please select the Year',
                                     ('2018', '2019', '2020', '2021', '2022'), horizontal=True, key='pie_pay_year'))
    pie_pay_mode__quater = int(st.radio('Please select the Quarter',
                                        ('1', '2', '3', '4'), horizontal=True, key='pie_pay_quater'))
    pie_pay_mode_values = st.selectbox(
        'Please select the values to visualize', ('Transacion_count', 'Transacion_amount'))
    pie_payment_mode = payment_mode[(payment_mode['Year'] == pie_pay_mode_year) & (
        payment_mode['Quater'] == pie_pay_mode__quater) & (payment_mode['State'] == pie_pay_mode_state)]
    # Pie chart 
    pie_pay_mode = px.pie(pie_payment_mode, values=pie_pay_mode_values,
                          names='Transacion_type', hole=.5, hover_data=['Year'])
    # Bar chart 
    pay_bar = px.bar(pie_payment_mode, x='Transacion_type',
                     y=pie_pay_mode_values, color='Transacion_type')
    st.plotly_chart(pay_bar)
    st.plotly_chart(pie_pay_mode)


# Transacion data analysis statewise
with transac_yearwise:
    st.subheader(':black[Transaction analysis]')
    transac_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                         'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                         'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                         'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                         'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                         'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                         'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                         'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                         'uttarakhand', 'west-bengal'), index=10, key='transac')
    transac__quater = int(st.radio('Please select the Quarter',
                                   ('1', '2', '3', '4'), horizontal=True, key='trans_quater'))
    transac_type = st.selectbox('Please select the Mode',
                                ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services', 'Others'), key='transactype')
    transac_values = st.selectbox(
        'Please select the values to visualize', ('Transacion_count', 'Transacion_amount'), key='transacvalues')
    payment_mode_yearwise = pd.read_csv(r"C:\Users\admin\Capstone\Phonepe\CSV\Agg_trans.csv")

    new_df = payment_mode_yearwise.groupby(
        ['State', 'Year', 'Quater', 'Transacion_type']).sum()
    new_df = new_df.reset_index()
    chart = new_df[(new_df['State'] == transac_state) &
                   (new_df['Transacion_type'] == transac_type) & (new_df['Quater'] == transac__quater)]
    #barchart
    year_fig = px.bar(chart, x=['Year'], y=transac_values, color=transac_values, color_continuous_scale='armyrose',
                      title='Transacion analysis '+transac_state + ' regarding to '+transac_type)
    st.plotly_chart(year_fig)    

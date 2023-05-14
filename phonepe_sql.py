import streamlit as st
import pandas as pd
import plotly.express as px
import sqlalchemy


#data in sql

user = 'root'
password = '123456'
host = 'localhost'
port = 3306
database = 'Phonepe'
connection = sqlalchemy.create_engine("mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
    user, password, host, port, database
))

query1 = 'select * from agg_transaction_table'
df = pd.read_sql(query1, con=connection)
query2 = 'select * from longitude_latitude_state_table'
state = pd.read_sql(query2, con=connection)
query3 = 'select * from districts_longitude_latitude_table'
districts = pd.read_sql(query3, con=connection)
query4 = 'select * from district_map_transaction_table'
districts_tran = pd.read_sql(query4, con=connection)
query5 = 'select * from district_map_registering_table'
app_opening = pd.read_sql(query5, con=connection)
query6 = 'select * from agg_userbydevice_table'
user_device = pd.read_sql(query6, con=connection)
query7 = 'select * from top_tran_table'
top_tran = pd.read_sql(query7, con=connection)
query8 = 'select * from top_user_table'
top_user = pd.read_sql(query8, con=connection)





# title
st.markdown("<h1 style='text-align: center; color: purple;'>PhonePe Pulse Data Analysis </h1>", unsafe_allow_html=True)



#top states data
st.write('# :red[TOP 5 STATES DATA]')
c1,c2=st.columns(2)
with c1:
    Year = st.selectbox(
            'Select the Year',
            ('2022', '2021','2020','2019','2018'),key='dfg')
with c2:
    Quarter = st.selectbox(
            'Select the Quatrer',
            ('1', '2', '3','4'),key='fgh')
Data_Map_User_df=app_opening.copy() 
top_states=Data_Map_User_df[(Data_Map_User_df['Year'] == int(Year)) & (Data_Map_User_df['Quater'] ==int(Quarter))]
top_states_r = top_states.sort_values(by=['Registered_user'], ascending=False)
top_states_a = top_states.sort_values(by=['App_opening'], ascending=False) 

Data_Aggregated_Transaction_df=df.copy()
top_states_T=Data_Aggregated_Transaction_df[(Data_Aggregated_Transaction_df['Year'] == int(Year)) & (Data_Aggregated_Transaction_df['Quater'] ==int(Quarter))]
topst=top_states_T.groupby('State')
x=topst.sum().sort_values(by=['Transacion_count'], ascending=False)
y=topst.sum().sort_values(by=['Transacion_amount'], ascending=False)


c1,c2,c3,c4= st.tabs(['Registered_user','App_openings','Transaction_count','Transaction_amount'])

with c1:
    
    st.subheader('Registered User')
    c5,c6=st.columns(2)
    with c5:
        rt=top_states_r[1:6]
        st.markdown(rt[[ 'State','Registered_user']].style.hide(axis="index").to_html(), unsafe_allow_html=True)
    with c6:
        z= px.pie(rt, values='Registered_user',names='State', hole=.5)
        st.plotly_chart(z)
with c2:
    at=top_states_a[1:6]
    st.subheader("App Openings")
    c7,c8=st.columns(2)
    with c7:
        st.markdown(at[['State','App_opening']].style.hide(axis="index").to_html(), unsafe_allow_html=True)
    with c8:
        z1= px.pie(rt, values='App_opening',names='State', hole=.5)
        st.plotly_chart(z1)
with c3:
    st.subheader("Transactions Count")
    c9,c10=st.columns(2)
    with c9:
        z3=pd.DataFrame(x[['Transacion_count']][1:6])
        st.write(z3)
    with c10:
        z4= px.pie(z3, values='Transacion_count', hole=.5)
        st.plotly_chart(z4)    
    
with c4:
    st.subheader("Transaction Amount ")
    c11,c12=st.columns(2)
    with c11:
        z5=(y['Transacion_amount'][1:6])   
        st.write(z5)
    with c12:
        
        z6= px.pie(z5, values='Transacion_amount', hole=.5)
        st.plotly_chart(z6)
    




# total transaction amount in bar and pie

with st.container():
    st.subheader('Total Transaction amount in bar chart')
    ab= pd.read_sql(query7,con=connection)
    c=ab.reset_index()
    b=ab.groupby(['State']).sum()[['Transaction_amount','Transaction_count']]
    e=b.reset_index()
    d= px.bar(e,x='State',y='Transaction_amount')
    st.plotly_chart(d)




#amount and count

ta,tc,st1= st.tabs(
    ["Transaction_amount",'Transaction_count','Registerd_user'])




#transcation amount data

with ta:
    st.subheader("Trancation amount in year")
    d=pd.read_sql(query1, con=connection)
    #ye= int(st.radio('Select the Year',('2018', '2019', '2020', '2021', '2022'), horizontal=True, key='ye'))
    a=d.groupby(['State','Year']).sum()['Transacion_amount']
    a.reset_index()
    sca = st.selectbox('Select the State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                         'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                         'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                         'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                         'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                         'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                         'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                         'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                         'uttarakhand', 'west-bengal'))
    
    sca1=d[d['State']==sca]
    li=px.line(sca1,x='Year',y='Transacion_amount')
    st.plotly_chart(li)

with tc:
    st.subheader("Trancation count in year")
    #e=pd.read_sql(query1, con=connection)
    b=d.groupby(['State','Year']).sum()['Transacion_count']
    b.reset_index()
    sc = st.selectbox('Select the State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                         'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                         'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                         'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                         'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                         'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                         'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                         'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                         'uttarakhand', 'west-bengal'),index=22)

    sc1=d[d['State']==sc]


   
    li2=px.line(sc1,x='Year',y='Transacion_count')
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
   #barchart
    device=pd.read_sql(query6, con=connection)
    dev_year = int(st.radio('Please select the Year',
                                     ('2018', '2019', '2020', '2021', '2022'), horizontal=True, key='pie_pay'))
    dev=device[device['Year']==dev_year]
    bar_user = px.bar(dev, x='Brand', y='Brand_count', color='Brand',
                      title='Bar chart analysis')
    st.plotly_chart(bar_user)
# Payment type analysis of Transacion data 
with payment_analysis:
    st.subheader(':black[Payment type Analysis]')

    payment_mode = pd.read_sql(query1, con=connection)
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
    payment_mode_yearwise = df = pd.read_sql(query1, con=connection)

    new_df = payment_mode_yearwise.groupby(
        ['State', 'Year', 'Quater', 'Transacion_type']).sum()
    new_df = new_df.reset_index()
    chart = new_df[(new_df['State'] == transac_state) &
                   (new_df['Transacion_type'] == transac_type) & (new_df['Quater'] == transac__quater)]
    #barchart
    year_fig = px.bar(chart, x=['Year'], y=transac_values, color=transac_values, color_continuous_scale='armyrose',
                      title='Transacion analysis '+transac_state + ' regarding to '+transac_type)
    st.plotly_chart(year_fig)    



from flask import Flask, render_template, request,jsonify
import pandas as pd
import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly
import plotly.express as px
import json
app = Flask(__name__)
app.debug = True
data3=None


def load_data():
    data=getData('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv','https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv','https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    data1 = mergeDt(data)
    data3={"Confirmed":data1[data1['Date'] == data1.iloc[-1][0]]["Confirmed"].sum(),"Deaths":data1[data1['Date'] == data1.iloc[-1][0]]["Deaths"].sum()
    ,"Recovered":data1[data1['Date'] == data1.iloc[-1][0]]["Recovered"].sum()}
    countries=[{"label": x, "value": x} for x in data1['Country'].unique()]
    data3['countries']=countries
    options=['Confirmed','Deaths','Recovered']
    data3['option_contry']=options
    data3['data']=data1
    return data3
@app.route('/', methods=['GET','POST'])
def dropdown():
    colours = ['Red', 'Blue', 'Black', 'Orange']
    if not data3:
        print("loading")
        load_data()
        print("Done")
    return render_template('test.html', data=data3)

@app.route('/wold/<country>')
def country(country):
    if data3:
        country_d=data3['data'][data3['data']['Country']==country]
        country_d1={"Confirmed":country_d[country_d['Date'] == country_d.iloc[-1][0]]["Confirmed"].sum(),"Deaths":country_d[country_d['Date'] == country_d.iloc[-1][0]]["Deaths"].sum()
        ,"Recovered":country_d[country_d['Date'] == country_d.iloc[-1][0]]["Recovered"].sum()}
        for i in country_d1.keys():
            country_d1[i]=int(country_d1[i])
        df = pd.DataFrame({
      "date": data3['data']['Date'],
      "Deaths":  data3['data']['Deaths'], })
        fig=px.line(df, x='date' , y='Deaths', title="Graph of deaths")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        country_d1['graph_d']=graphJSON
        return jsonify(country_d1)
    return jsonify({'Confirmed':0,'Recovered':0,'Deaths':0})
@app.route('/graphd/<country>')
def graph_countryd(country):
    if data3 and country:
        date=[]
        for i in data3['data']['Date']:
            date.append(i)
        deaths=[]
        for i in data3['data']['Deaths']:
            deaths.append(int(i))   
        df = pd.DataFrame({
      "date": date,
      "Deaths":  deaths})
        fig=px.line(df, x='date' , y='Deaths', title="Graph of deaths")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
       
        return graphJSON
    return jsonify({'Confirmed':0,'Recovered':0,'Deaths':0})  
@app.route('/graphc/<country>')
def graph_countryc(country):
    if data3 and country:
        date=[]
        for i in data3['data']['Date']:
            date.append(i)
        Confirmed=[]
        for i in data3['data']['Confirmed']:
            Confirmed.append(int(i))
        df = pd.DataFrame({
      "date": date,
      "Confirmed":  Confirmed})
        fig=px.line(df, x='date' , y='Confirmed', title="Graph of deaths")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
       
        return graphJSON
    return jsonify({'Confirmed':0,'Recovered':0,'Deaths':0})   
@app.route('/graphr/<country>')
def graph_countryr(country):
    

    if data3 and country:
        date=[]
        for i in data3['data']['Date']:
            date.append(i)
        Recovered=[]
        for i in data3['data']['Recovered']:
            Recovered.append(int(i))
        df = pd.DataFrame({
      "date": date,
      "Recovered":  Recovered})
        fig=px.line(df, x='date' , y='Recovered', title="Graph of deaths")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
       
        return graphJSON
    return jsonify({'Confirmed':0,'Recovered':0,'Deaths':0}) 
@app.route('/pie/<country>')
def pie_country(country):
    if 'wol' in country:
        df = pd.DataFrame({"type": ["Confirmed","Deaths","Recovered"],"value":  [data3['Confirmed'],data3['Deaths'],data3['Recovered']]})
        fig = px.pie(df, values='value', names='type', title='Distribution Wold wide')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
       
        return graphJSON
    else:
        country_d=data3['data'][data3['data']['Country']==country]
        country_d1={"Confirmed":country_d[country_d['Date'] == country_d.iloc[-1][0]]["Confirmed"].sum(),"Deaths":country_d[country_d['Date'] == country_d.iloc[-1][0]]["Deaths"].sum()
        ,"Recovered":country_d[country_d['Date'] == country_d.iloc[-1][0]]["Recovered"].sum()}
        value=[]
        type_=[]
        for i in country_d1.keys():
            value.append(int(country_d1[i]))
            type_.append(country_d1[i])
        df = pd.DataFrame({"type": ["Confirmed","Deaths","Recovered"],"value":  value})
        fig = px.pie(df, values='value', names='type', title=country+" Distribution")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
       
        return graphJSON
@app.route('/graph/<country>')
def graph_countryw(country):
    if "wol" in country:
        date=[]
        for i in data3['data']['Date']:
            date.append(i)
        Recovered=[]
        for i in data3['data']['Recovered']:
            Recovered.append(int(i))
        deaths=[]
        for i in data3['data']['Deaths']:
            deaths.append(int(i))  
        Confirmed=[]
        for i in data3['data']['Confirmed']:
            Confirmed.append(int(i))  
        df = pd.DataFrame({"date": date,"Recovered":  Recovered})
        fig = make_subplots(rows=1,cols=3,subplot_titles=("Confirmed", "Deaths", "Recovered"))

        fig.add_trace(
            go.Scatter(x=date, y=Confirmed),
            row=1, col=1,
        )

        fig.add_trace(
            go.Scatter(x=date, y=deaths),
            row=1, col=2
        )
        fig.add_trace(
            go.Scatter(x=date, y=Recovered),
            row=1, col=3
        )
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
       
        return graphJSON
    else:
        country_d=data3['data'][data3['data']['Country']==country]
        date=[]
        for i in country_d['Date']:
            date.append(i)
        Recovered=[]
        for i in country_d['Recovered']:
            Recovered.append(int(i))
        deaths=[]
        for i in country_d['Deaths']:
            deaths.append(int(i))  
        Confirmed=[]
        for i in country_d['Confirmed']:
            Confirmed.append(int(i))  
        df = pd.DataFrame({"date": date,"Recovered":  Recovered})
        fig = make_subplots(rows=1,cols=3,subplot_titles=("Confirmed", "Deaths", "Recovered"))

        fig.add_trace(
            go.Scatter(x=date, y=Confirmed),
            row=1, col=1,
        )

        fig.add_trace(
            go.Scatter(x=date, y=deaths),
            row=1, col=2
        )
        fig.add_trace(
            go.Scatter(x=date, y=Recovered),
            row=1, col=3
        )
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
       
        return graphJSON
    if data3 and country:
        date=[]
        for i in data3['data']['Date']:
            date.append(i)
        Recovered=[]
        for i in data3['data']['Recovered']:
            Recovered.append(int(i))
        df = pd.DataFrame({
      "date": date,
      "Recovered":  Recovered})
        fig=px.line(df, x='date' , y='Recovered', title="Graph of deaths")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
       
        return graphJSON
    return jsonify({'Confirmed':0,'Recovered':0,'Deaths':0}) 

def mergeDt(data):

    df_merged = pd.merge(data[0], data[1], how='inner', on=['Date', 'Country'])

    df_merged = pd.merge(df_merged, data[2], how='inner', on=['Date', 'Country'])
    print(df_merged.head())
    return df_merged
def getData(confirmed=None,death=None,recovered=None):
    df_confirmed = pd.read_csv(confirmed)
    df_deaths = pd.read_csv(death)
    df_recovered = pd.read_csv(recovered)


    df_confirmed = df_confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date', value_name='Confirmed')
    df_confirmed['Date'] = [datetime.datetime.strptime(d,"%m/%d/%y").date() for d in df_confirmed['Date']]
    df_confirmed = df_confirmed.rename(columns={'Country/Region': 'Country'})
    df_confirmed = df_confirmed.groupby(['Date', 'Country'], as_index=False)['Confirmed'].sum()

    df_deaths = df_deaths.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date', value_name='Deaths')
    df_deaths['Date'] = [datetime.datetime.strptime(d,"%m/%d/%y").date() for d in df_deaths['Date']]
    df_deaths = df_deaths.rename(columns={'Country/Region': 'Country'})
    df_deaths = df_deaths.groupby(['Date', 'Country'], as_index=False)['Deaths'].sum()

    df_recovered = df_recovered.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date', value_name='Recovered')
    df_recovered['Date'] = [datetime.datetime.strptime(d,"%m/%d/%y").date() for d in df_recovered['Date']]
    df_recovered = df_recovered.rename(columns={'Country/Region': 'Country'})
    df_recovered = df_recovered.groupby(['Date', 'Country'], as_index=False)['Recovered'].sum()


    df_health = pd.read_json('https://www.svt.se/special/articledata/2532/alder_data.json')
    dic = {}
    columns = []
    # print(df_recovered.head())
    # print(df_confirmed.head())
    for index in range(len(df_health)):
        dic[df_health.iloc[index][1]['datum']] = [i for i in df_health.iloc[index][1].values()]
        
    df_health = pd.DataFrame.from_dict(dic, orient='index', columns=[i for i in df_health.iloc[0][1]])  
    for column in df_health.columns:
        if 'totalt' in column and 'unika personer totalt' not in column:
            columns.append(column)

    columns.remove('100-109 totalt')
    columns.remove('110-119 totalt')
    columns.sort()
    df_health = df_health[columns]

    # print(df_health.head())
    return (df_confirmed,df_deaths,df_recovered,df_health)
if __name__ == "__main__":
    if not data3:
        data3=load_data()
    app.run()
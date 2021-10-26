# -*- coding: utf-8 -*-


#Please read the following instructions to run my dashboard:
#1. Set the work_directory (below) to the correct path
#2. Check if the required packages (os, pandas, plotly.express, dash and 
#dash_bootstrap_components) have been installed.
#3. Excute this python file using runfile("HW4_Lcuas Zhang.py") with the two 
#excel files in the folder. 
#4. Visit my dashboard on http://127.0.0.1:8050/


work_directory = "C:\\Users\\zlj\\Desktop\\BIOSTAT 823\\HW4"
text_header="""

**Homework 4 for BIOS 823**

*By Lucas Zhang*

Is there life after graduate school?
Download data of [Science and Engineering PhDs awarded in the US] 
(https://ncses.nsf.gov/pubs/nsf19301/data). 
Do some analysis in `pandas`. 
Make a [dashboard visualization](https://pyviz.org/dashboarding/) 
of a few interesting aspects of the data.

Here I visualize the tables [Doctorate recipients from U.S. colleges and 
universities: 1958–2017]
(https://ncses.nsf.gov/pubs/nsf19301/assets/data/tables/sed17-sr-tab001.xlsx) 
and [Doctorate-granting institutions, by state
or location and major science and engineering fields of study: 2017]
(https://ncses.nsf.gov/pubs/nsf19301/assets/data/tables/sed17-sr-tab007.xlsx)
to illustrate the overall tendencies of Doctoral recipients over years and 
accross different institutes in the U.S.

Please also visit my [GitHub Page](https://lujun995.github.io/) and 
[GitHub repository](https://github.com/Lujun995/BIOS823)
"""

#Initialization
import os
import pandas as pd
import plotly.express as px  
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

#Data preparation
os.chdir(work_directory)
f_time = "Number of Doctorate recipients 1958–2017.xlsx"
f_instit_majo = "Doctorate-granting institutions, by location and major fields.xlsx"
df_time = pd.read_excel(f_time, header=[0], engine='openpyxl')
df_demograph = pd.read_excel(f_instit_majo, header=[0, 1, 2], engine='openpyxl')
df_demograph = df_demograph.set_index(df_demograph.columns[0])
df_demograph = df_demograph.stack(level=0).stack(level=0).stack(level=0).reset_index()
colnames = ["Location", "Sci/Eng", "Field", "Major", "Student Number"]
colnames_o = list(df_demograph)
df_demograph.rename(columns = {colnames_o[i]: colnames[i] 
                                 for i in range(0,len(colnames_o))},
                      inplace = True)
for i in range(2, df_demograph.shape[1]-1):
    index = df_demograph.iloc[:, i].str.contains("Unnamed:").values
    df_demograph.iloc[index, i] = df_demograph.iloc[index, i - 1]
states = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", 
          "California", "Colorado", "Connecticut", "District ", "of Columbia", 
          "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", 
          "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", 
          "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", 
          "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", 
          "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", 
          "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", 
          "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", 
          "Wisconsin", "West Virginia", "Wyoming"]
df_states = df_demograph[df_demograph.Location.isin(states)]
df_states = df_states[df_states.Field != "All fields"]
df_states = df_states[df_states.Major != "Total"]
df_instit = df_demograph[ ~ df_demograph.Location.isin(states)]
df_instit = df_instit[df_instit.Field != "All fields"]
df_instit = df_instit[df_instit.Major != "Total"]
df_instit = df_instit[df_instit.Location != "All institutions"]

#figures
#fig = px.sunburst(df, path=['sex', 'day', 'time'], 
#values='total_bill', color='day')
#df_major_ins = df_institu.groupby(["Major", "Institute"]).sum()

#text contents
text_time = """
The figure below shows the number of PhD degree recipients rapidly increased from 1958 to 2017.
In 1958, there are less than 9,000 PhD graduate every year all over the United States. 
Six decades later, the number of PhD degree recipients increased to 55,000, four times more than
in 1958.

Feel free to use the slider bar below to specify a period of interest.
"""
text_instit = """
The figure below shows the number of PhD recipients in different majors in 2017. In the
dropdown box below, you can select institutes of interest. If the box is clear, you select
all the records.

What are the distribution of majors of PhD graduates from Duke, Harvard and 
MIT in 2017? Type Duke, Harvard and Massachusetts Institute of Technology in the box and 
select the corresponding institutes. Is what you find in line with your impression?

From the sunburst graph below, we can find that while a lot of PhD recipients graduated from 
all the three institutes in 2017, Harvard grants the most PhD degrees in life science and MIT 
is the winner in engineering.
"""

#HTML layout
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children="How many PhDs students graduate in the U.S. every year?"), 
                    className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(dcc.Markdown(children=text_header), 
                    className="mb-4")
        ]),
        html.Hr(), #a thematic break between paragraph-level elements
        
        dbc.Row([
            dbc.Col(html.H3(children="Number of PhD Graduates over Years in the U.S."), 
                    className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(dcc.Markdown(children=text_time), 
                    className="mb-4")
        ]),
        dcc.Graph(id = 'fig_time'),
        dcc.RangeSlider(id = "year_range", step = 1, 
                        min = df_time['Year'].min(), max=df_time['Year'].max(),
                        value = [df_time['Year'].min(), df_time['Year'].max()],
                        updatemode = "drag", pushable = True,
                        marks = {str(year): str(year) 
                                 for year in range(df_time['Year'].min(),
                                                   df_time['Year'].max(), 10)}
                        ),
        html.Hr(),
        
        dbc.Row([
            dbc.Col(html.H3(children="Number of PhD Graduates over Different Majors in the U.S."), 
                    className="mb-2")
        ]),
        dbc.Row([dbc.Col(dcc.Markdown(children=text_instit), className="mb-4")]),
        dcc.Dropdown(id = "instit_choice", value=["Duke U."], multi=True,
                     options=[{"label": sch, "value": sch} for sch in df_instit.Location.unique()],
                     placeholder="All institutes"),
        dcc.Graph(id = 'fig_instit', style={'width': '90vh', 'height': '90vh'}),
        html.Hr(),
        
    ])
])

#Interactive Figures
@app.callback(Output("fig_time", "figure"), Input("year_range", "value"))
def ifig_time(years): #this seems directly related to the callback on the above
    df_time_ranged = df_time[(df_time["Year"] >= years[0]) &
                             (df_time["Year"] <= years[1])]
    fig_time = px.line(df_time_ranged, x="Year", y="Doctorate recipients", 
                       template = "simple_white", markers = True)
    fig_time.update_layout(transition_duration=500)
    return fig_time
#the number of graduates seems to be related to the GDP growth rate

@app.callback(Output("fig_instit", "figure"), Input("instit_choice", "value"))
def ifig_instit(schools):
    if len(schools) == 0:
        df_instit_s = df_instit
    else:
        df_instit_s = df_instit[df_instit.Location.isin(schools)]
    df_instit_s = df_instit_s.groupby(["Field", "Major"]).sum().reset_index()
    fig_instit = px.sunburst(df_instit_s, path = ['Field', 'Major'], 
                             values = "Student Number", color = "Field",
                             template = "simple_white")
    fig_instit.update_layout(transition_duration=500)
    return fig_instit
        

#fig = px.sunburst(df, path=['sex', 'day', 'time'], values='total_bill', color='day')


if __name__ == '__main__':
    app.run_server(debug=True)
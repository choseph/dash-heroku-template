import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"], low_memory=False)

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

paragraph1 = "Many studies have been devoted to explaining the existing wage gap between men and women in the United States. A variety of measures are consistent in revealing that there is discrimination based on gender however these measures fail to gauge the full effects of discrimination due to the complexity of this issue. The data generally fail to capture the amount of opportunities denied for women, so a complete analysis is not possible. Nonetheless, analyzing available data is a good starting point."
paragraph2 = "The NORC GSS is an organization that collects data on Americans in hopes to study and analyze certain trends, attitudes, and behaviors. This data contains questions pertaining to demography, behavior, and miscellaneous topics. This data allows scholars to monitor social change in the United states by examining the characteristics of certain subgroups and comparing responses to other countries. To ensure that the data is of the highest quality, GSS deploys transparent and advanced survey methods. "
sources = "Sources: [Gender gap source](https://www.epi.org/publication/what-is-the-gender-pay-gap-and-is-it-real/), [GSS Source] (https://gss.norc.org/About-The-GSS)"

table2 = gss_clean[['income', 'job_prestige', 'socioeconomic_index', 'education', 'sex']].groupby('sex').mean().round(2).reset_index()
table2 = ff.create_table(table2)

table3 = gss_clean[['id', 'sex', 'male_breadwinner']].groupby(['sex', 'male_breadwinner']).count().reset_index()
table3 = table3.rename({'id':'count'}, axis = 1)

fig3 = px.bar(table3, x='male_breadwinner', y='count', color='sex',
             labels={'male_breadwinner':'Level of Agreement with Male Breadwinner Question', 'count':'Number of People'},
             hover_data = ['male_breadwinner'],
             text='male_breadwinner',
             barmode = 'group')
fig3.update_layout(showlegend=True)
fig3.update(layout=dict(title=dict(x=0.5)))

# Problem 4
table4 = gss_clean[['sex', 'job_prestige', 'income', 'education', 'socioeconomic_index']]

# table4 = table4[~table4.income.isnull()]

fig4 = px.scatter(table4, x='job_prestige', y='income', 
                 color = 'sex', 
                 trendline='ols',
                 height=600, width=600,
                 labels={'job_prestige':'Occupational prestige score', 
                        'income':'Annual Income'},
                 hover_data=['job_prestige', 'income', 'socioeconomic_index', 'education'])
fig4.update(layout=dict(title=dict(x=0.5)))

# Problem 5 a
table5_income = gss_clean[['sex', 'income']]

fig5_a = px.box(table5_income, x='income', y = 'sex', color = 'sex',
                   labels={'income':'Annual Income','sex':''})

fig5_a.update(layout=dict(title=dict(x=0.5)))
fig5_a.update_layout(showlegend=False)

# Problem 5 b
table5_prestige = gss_clean[['sex', 'job_prestige']]

fig5_b = px.box(table5_prestige, x='job_prestige', y = 'sex', color = 'sex',
                   labels={'job_prestige':'Occupational prestige score'})

fig5_b.update(layout=dict(title=dict(x=0.5)))
fig5_b.update_layout(showlegend=False)

table6 = gss_clean[['income', 'sex', 'job_prestige']]

table6['job_prestige_group'] = pd.cut(table6.job_prestige, 
                                         bins=6, 
                                         labels=("1 Very Low", "2 Low", "3 Medium", "4 High", "5 Very High", "6 Super High"))
table6 = table6.dropna()

table6 = table6.sort_values('job_prestige_group')



fig6 = px.box(table6, x = 'income', y = 'sex', color = 'sex', 
             facet_col='job_prestige_group', facet_col_wrap=2,
             labels={'job_prestige':'Occupational prestige score', 'sex':''})

fig6.update(layout=dict(title=dict(x=0.5)))
fig6.update_layout(showlegend=False)
fig3.update_layout({'paper_bgcolor': 'powderblue'})
fig4.update_layout({'paper_bgcolor': 'powderblue'})
fig5_a.update_layout({'paper_bgcolor': 'powderblue'})
fig5_b.update_layout({'paper_bgcolor': 'powderblue'})
fig6.update_layout({'paper_bgcolor': 'powderblue'})


app = Dash(__name__, external_stylesheets=external_stylesheets)
server= app.server

app.layout = html.Div(
    [
        html.H1("Exploring the Gender Wage Gap in the United States",style = {'font-weight':'bold'}),
        html.H1("By: Joe Cho",style = {'font-weight':'bold'}),
      
        dcc.Markdown(children = paragraph1),
        dcc.Markdown(children = paragraph2),
        dcc.Markdown(children = sources),
        
        html.H2("Comparing Men and Women",style = {'text-decoration':'underline'}),
        
        dcc.Graph(figure=table2),
        
        
        html.H2("Responses to Various Questions",style = {'text-decoration':'underline'}),
        
        html.Div([
            
            html.H3("Question"),
            
            dcc.Dropdown(id='variable',
                         options=[{'label': i, 'value': i} for i in ['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer','men_overwork']],
                         value='male_breadwinner'),
            
            html.H3("Group By:"),
            
            dcc.Dropdown(id='groupby',
                         options=[{'label': i, 'value': i} for i in ['sex', 'region','education']],
                         value='sex'),
        
        ], style={'width': '25%', 'float': 'left'}),
        
        html.Div([
            
            dcc.Graph(id="graph")
        
        ], style={'width': '70%', 'float': 'right'}),
        
        html.Div([
            html.H2("Alternative Methods of Visualization",style = {'text-decoration':'underline'}),
            dbc.Col([
                html.Div([
                    dcc.Tabs(id='tabs-example', value='tab-1', children=[
                        dcc.Tab(label='Scatterplot', value='tab-1'),
                        dcc.Tab(label='Boxplots', value='tab-2'),
                    ]),
                html.Div(id='tabs-example-content')
                ])
            ])],style = {'padding-top':'450px'})
    
    ], style = {'background-color':'powderblue','font-family':'Courier New'}
)
@app.callback(Output(component_id="graph",component_property="figure"), 
                  [Input(component_id='variable',component_property="value"),
                   Input(component_id='groupby',component_property="value")])

def make_figure(x, y):  
    table3 = gss_clean.groupby([y, x]).count().reset_index()
    table3 = table3.rename({'id':'count'}, axis = 1)
    tempfigure = px.bar(table3, x=x, y='count', color = y,
             hover_data = [x],
             barmode = 'group')
    tempfigure.update_layout({'paper_bgcolor': 'powderblue'})
    return tempfigure

@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([html.H3('Scatterplot of Annual Income Against Job Prestige for Each Gender'),dcc.Graph(id= 'graph1', figure = fig4)],style = {'float':'center'})
    elif tab == 'tab-2':
        return html.Div([html.Div([html.H2("Distribution of Annual Income by Gender"),dcc.Graph(figure=fig5_a)], style = {'width':'50%', 'float':'left','background-color':'powderblue'}),
            html.Div([
            html.H2("Distribution of Incomes binned by Job Prestige For Each Gender"),            
            dcc.Graph(figure=fig6)], style = {'width':'50%', 'float':'right','background-color':'powderblue'})])
    

if __name__ == '__main__':
    app.run_server(mode='inline', debug=True, port=8054)

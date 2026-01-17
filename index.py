from app import app, server
import dash
from dash import Dash, Input, Output, html, dcc, State, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
import json
import os
from dash.dash_table.Format import Group


app.layout = dbc.Container([
    dcc.Location(id='url'),
    dbc.Row([
        #SideBar
        dbc.Col([
            html.Div([
                html.H3("Lu.Freire", className="text-primary", style={'fontSize': '3.5rem', 'fontWeight': 'bold'}),
                html.P("Estética e Bem-estar", className="text-muted", style={'fontSize': '1.5rem'}),
                html.Hr()
            ],style={'padding': '20px', 'height': '100vh', 'borderRight': '1px solid #444'})
        ],md=2),        
        
        #Calendario
        dbc.Col([
            #caixa do calendario
            dbc.Col([
                #Linha 1 botoes voltar a avancar e Ano
                dbc.Row([
                    dbc.Button('<', id='voltar',
                        style={
                            'color' : 'black',
                            'background-color' : '#ffffff',
                            'border' : '1px solid black',
                            'border-radius' : '50%',
                            'width' : '35px',
                            'height': '35px',
                            'margin-top' : '60px',
                            'margin-left' : '280px',
                            'font-weight' : 'bold',
                            'font-size' : '20px',
                            'padding' : '0px 0px'
                        }),

                        dbc.Button('>',id='avancar',
                            style={
                                'color' : 'black',
                                'background-color': '#ffffff',
                                'border' : '1px solid black',
                                'border-radius' : '50%',
                                'width' : '35px',
                                'height' : '35px',
                                'margin-top' : '60px',
                                'margin-left' : '160px',
                                'font-weight': 'bold',
                                'font-size' : '20px',
                                'padding' : '0px 12px'
                            }),

                        html.Div('Ano', 
                            style={
                                'width' : 'fit-content',
                                'padding' : '0px',
                                'textAlign': 'center',
                                'margin-left' : '-160px', 
                                'margin-top' : '45px', 
                                'font-weight': 'bold',
                                'font-size' : '40px',
                                'background-color' : 'transparent'},
                            id='div-ano', className='primary-font-color')
                ]),
                
                #linha 2 mes
                dbc.Row([
                    html.Div('Mês',
                        style={
                            'width' : '130px',
                            'textAlign': 'center',
                            'margin-left' : '330px',
                            'margin-top' : '0px',
                            'font-weight': 'bold',
                            'font-size' : '26px',
                            'background-color' : 'transparent'
                        }, id='div-mes', className ='secundary-font-color')
                ]),
                
                #Linha 3 calendario
                dbc.Row([
                    #datatable
                ]),
            ], md=12, style={
                        'margin-left' : '7.5px', 
                        'margin-top' : '35px', 
                        'border-top-left-radius': '2%',
                        'border-bottom-left-radius' : '2%'
                        }, className = 'primary-color'),
        ],md=5),
        
        #Lista de tarefas
        dbc.Col([
            dbc.Row([
                #Dia do mes e dia da semana
                dbc.Col([
                    
                    html.Div(id='div-dia-mes-atual',
                        style={
                            'margin-left':'0px',
                            'margin-top':'20px',
                            'width':'fit-content',
                            'height':'fit-content',
                            'font-size':'150px',
                            'line-height':'0.85',
                            'background-color':'transparent'
                        }, className='primary-font-color'),
                    
                    html.Div(id='div-dia-semana-atual',
                        style={
                            'margin-left':'172px',
                            'margin-top':'-30px',
                            'width':'140px',
                            'height':'30px',
                            'font-size':'20px',
                            'background-color':'transparent'
                        }, className='primary-font-color'),
                ],md=8, className='secundary-color'),
                
                #Adicionar tarefa com o botao
                dbc.Col([
                    html.Div("Adicionar nova tarefa",
                                style={
                                    'margin-left' : '20px',
                                    'margin-top' : '48px', 
                                    'width' : '80px',
                                    'height' : '50px',
                                    'text-align' : 'left'
                                    }, className='primary-font-color'),

                    dbc.Button([html.I(className = "fa fa-plus", style={'font-size' : '400%'})],
                                    id='open-modal-button',
                                    style={
                                        'width' : '40px',
                                        'height' : '40px',
                                        'margin-top' : '-77px',
                                        'margin-left' : '120px',
                                        'border-radius' : '50%'
                                        }),
                        
                        html.Div(id='div-data-concatenada',
                                hidden=True),  

                ], md=4, className = 'secundary-color', style={ 'border-top-right-radius' : '7%'})
            ], style={'margin-top' : '35px', 'width' : '550px'}),
            dbc.Row([
                dbc.Card(
                    style = {
                        'color' : '#000000',
                        'border-radius' : '0px',
                        'width' : '550px',
                        'height' : '413px',
                        'margin-left' : '0px',
                        'margin-top' : '0px',
                        'background-color': 'rgba(0,0,0)',
                        'border-bottom-right-radius' : '2%'
                        }, id='card-geral')
            ])
        ],md=5),
    ]),

        dbc.Modal([
            dbc.ModalHeader('Nova Tarefa',
                            style={
                                'color':'#ffffff',
                                'font-size':'20px',
                            },className='modal-color'),
            
            dbc.ModalTitle(
                dbc.Input(id='titulo-input',
                          placeholder='Adicione um titulo', type='text',
                          style={
                              'widht':'400px',
                              'border-top':'transparent',
                              'border-left':'transparent',
                              'border-right':'transparent',
                              'border-bottom':'2px solid black',
                              'border-radius':'0px',
                              'margin-left':'10px',
                              'font-weight':'bold',
                              'margin-top':'20px'
                          }, className='input-modal-color'), className='modal-color'
            ),
            
            dbc.ModalBody([
                dbc.Input(id="horario-input", placeholder="Horário", type="text",
                            style={
                                'width' : '76px',
                                'margin-top' : '20px',
                                'border' : '1px solid black'},
                            className='input-modal-color',
                            maxlength=7
                    ),

                dbc.Input(id="local-input", placeholder="Local", type="text", 
                            style={
                                'width' : '450px',
                                'margin-top' : '20px',
                                'border' : '1px solid black'},
                            className='input-modal-color'
                    ),

                dbc.Input(id="descricao-input", placeholder="Descrição", type="text", 
                            style={
                                'width' : '450px',
                                'margin-top' : '20px',
                                'border' : '1px solid black'},
                            className='input-modal-color'
                    ),

                html.Div(id="required-field-notification", 
                            style={
                                'width' : '450px',
                                'margin-top' : '20px'},
                            className ='secundary-font-color'
                    ),

                dbc.Button('Salvar',  color="light", className="me-1", id='submit-tarefa', n_clicks=0,
                            style={
                                'margin-top' : '15px',
                                'margin-left' : '390px',
                                'font-weight': 'bold',
                                'font-size' : '16px',}
                    )
            ], className='modal-color')
        ],style={
            'color':'#000000',
            'background-color':'rgba(255, 255, 255, 0.4)',
        }, id='modal-tarefa',
            is_open=False),
    
],fluid=True, style={'backgroundColor': '#1a1a1a', 'color': 'white'})
    
@app.callback(
    Output('modal-tarefa', 'is_open'),

    Input('open-modal-button', 'n_clicks'),
    Input('submit-tarefa', 'n_clicks'),

    State('modal-tarefa', 'is_open'),
    State('horario-input', 'value'),
    prevent_initial_call=True
)

def toggle_modal(n1, n2, is_open, horario):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    if changed_id.split('.')[0] == 'open-modal-button':
        return not is_open

    if changed_id.split('.')[0] == 'submit-tarefa' and horario:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run(debug=True)
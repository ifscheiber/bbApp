from dash import register_page, html, dcc, Output, Input, State, callback, callback_context
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

import pandas as pd

import plotly.express as px

from data.mock_data import mock_data_accounts as md

# ----------------------------------------------------------------------------------------------------------------------
# Register Page
# ----------------------------------------------------------------------------------------------------------------------
# create report
class TestReport:

    def __init__(self, page_url='home'):


        self.dl_billing_url_id = 'lpn_dl_billing_url_to_all_pages_id'
        self.setup_new_account_id = f'setup_new_account_{page_url}_id'

        mock_data, columnDefs, pinned_row = md.get_mock_data_hierachy()
        rowData = mock_data.to_dict('records')
        pinned_row = pinned_row.to_dict('records')

        # Conditional Style for the pinned 'Aggregation' row!
        get_row_style = dict(
            styleConditions=[
                dict(
                    condition="params.node.rowIndex != 0 & params.data.type == ''",
                    style=dict(
                        fontWeight='bolder',
                        border='none',


                        borderBottom="1px solid #405A73",
                    ),
                ),
                dict(
                    condition="params.node.rowIndex == 0",
                    style=dict(
                        fontWeight='bolder',
                        border='none',
                        borderBottom="1px solid #405A73",
                    ),
                )
            ]
        )

        grid = dag.AgGrid(
            className="ag-theme-alpine ag-theme-accordion",
            columnDefs=columnDefs,
            defaultColDef={
                "flex": 1,
            },
            dashGridOptions={
                'domLayout':"autoHeight",
                "autoGroupColumnDef": {
                    "headerName": "System",
                    "minWidth": 300,
                    "cellRendererParams": {
                        "suppressCount": True,
                    },
                },
                "groupDefaultExpanded": 1,
                "getDataPath": {"function": "getDataPath(params)"},
                "treeData": True,

                'pinnedBottomRowData': pinned_row,
                #'groupIncludeTotalFooter': 'True'
            },
            getRowStyle=get_row_style,
            rowData=rowData,
            enableEnterpriseModules=True,

        )

        '''grid = dag.AgGrid(
            id="custom-components-grid",
            className="ag-theme-alpine ag-theme-lpn-dark",
            columnDefs=columnDefs,
            rowData=df.to_dict("records"),
            defaultColDef=defaultColDef,
            columnSize="responsiveSizeToFit",
            columnSizeOptions= {
                'columnLimits': [
                    {'key': 'edit', 'minWidth': 40, 'maxWidth': 60},
                    {'key': 'analyse', 'minWidth': 40, 'maxWidth': 60},
                    {'key': 'price', 'minWidth': 220, 'maxWidth': 220},
                    {'key': 'volume', 'minWidth': 500, 'maxWidth': 500},
                ],
                'defaultMinWidth': 175
            },
            dashGridOptions={"domLayout": "autoHeight"},
            style={"height":'auto', 'width': '100%', }
        )'''

        figure = md.get_mock_line_chart_data()
        figure.update_layout(
            dict(
                plot_bgcolor='#102E44',
                paper_bgcolor='#102E44',

                font=dict(
                    color='#88CACA',
                    size=14
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="top", y=.85,
                    xanchor="left", x=0.15,
                    borderwidth=0,
                    font=dict(
                        size=14,
                        color='#88CACA'
                    ),
                ),
                # xref='container'

                height=350,
                # width=272,
                xaxis=dict(
                    #showgrid=False,
                    zeroline=True,

                    zerolinecolor='#405A73',
                    zerolinewidth=0.5,

                    #showticklabels=False,
                    #showline=False
                    tickson='labels',
                    gridcolor='#405A73',

                ),

                yaxis=dict(
                    #showgrid=False,
                    zeroline=True,
                    gridcolor='#405A73',
                    zerolinecolor='#405A73',
                    zerolinewidth=0.5,
                    showticklabels=True,
                    #showline=False,
                    #ticklen = 100,
                    tickson='labels',
                    ticksuffix=' '
                )

            )
        )



        r1 = dbc.Row(
            children=[
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader('Costs', className='test-card-header'),
                        dbc.CardBody(
                            dcc.Graph(
                                figure=figure,
                                style={'width': 'auto', 'height': 'auto'}
                            )
                        )],
                        class_name='test-borders'),
                    md=4,
                    sm=12
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader('Cost', className='test-card-header'),
                        dbc.CardBody(
                            'Some Text'
                        )
                    ],
                    class_name='test-borders'
                    ),
                    md=4,
                    sm=12
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader('Alerts', className='test-card-header'),
                        dbc.CardBody(
                            'No Alert'
                        )
                    ],
                        class_name='test-borders'
                    ),
                    md=4,
                    sm=12
                ),

            ], class_name=' mb-5'


        )
        r2 = dbc.Row(
            dbc.Col(
                    [dbc.Card(
                        [


                                grid


                        ],
                        style={'border': 'none'},
                        className='test-borders'
                    ),

                    ],

            )
        )

        self.visualization = html.Main(
            dbc.Container(children=[
                r1, r2
            ]),

            className='app-layout')

    def define_callbacks(self):
        """
        Defines the dash.callbacks.
        Should consist of several inner functions, each specifying a callback.
        """

        @callback(
            Output(self.dl_billing_url_id, 'href'),
            Input(self.setup_new_account_id, 'n_clicks'),
            prevent_initial_call=True
        )
        def board_client(board_user_button_n_clicks: int):
            if board_user_button_n_clicks:
                return '/account-setup'



report = TestReport()

def layout():
    return report.visualization

# include callbacks
report.define_callbacks()

# register page
register_page(__name__, name='Overview', path='/test-home')

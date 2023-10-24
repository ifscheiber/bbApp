from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from datetime import datetime
from data.mock_data import mock_data_accounts as md
from views.utils import get_colorway, get_highlight_colorway
from views.testPage.billing_units_content import BillingUnits
from views.testPage.info_center_content import InfoCenterContent

class Header2Row:

    def __init__(self, parent_page: str):

        self.select_account_id = f"select_account_{parent_page}_id"
        self.current_billing_period_id = f"current_billing_period_{parent_page}_id"
        self.request_count_id = f"request_count_{parent_page}_id"
        self.cost_estimate_id = f"cost_estimate_{parent_page}_id"

        self.select_lvl_1_id = f"select_lvl_1_{parent_page}_id"
        self.select_lvl_2_id = f"select_lvl_2_{parent_page}_id"
        self.select_lvl_3_id = f"select_lvl_3_{parent_page}_id"
        self.select_lvl_4_id = f"select_lvl_4_{parent_page}_id"

        self.info_center = InfoCenterContent(parent_page='pp')
        self.billing_units = BillingUnits(parent_page='pps')

        select_menu_items = [
            dict(
                id=self.select_lvl_1_id,
                description='Business Division',
                data=[
                    dict(value="all", label="All"),
                    dict(value="buy_side", label="Buy Side"),
                    dict(value="sell_side", label="Sell Side"),
                    dict(value="custody", label="Custody"),
                ],
                clearable=True,
                placeholder='Select',
                value='all',
                disabled=False,
                styles=None
            ),
            dict(
                id=self.select_lvl_2_id,
                description='Billing Unit',
                data=[
                    dict(value="all", label="All"),
                    dict(value="os_1", label="OS 123456"),
                    dict(value="a_1", label="A 987456")
                ],
                clearable=True,
                placeholder='Select',
                value='all',
                disabled=True,
                styles=dict(description={
                    "color": "var(--lpn-bg-dark) !important"
                })
            ),
            dict(
                id=self.select_lvl_3_id,
                description='Account/Request System',
                data=[
                    dict(value="all", label="All"),
                ],
                clearable=True,
                placeholder='Select',
                value="all",
                disabled=True,
                styles=dict(description={
                    "color": "var(--lpn-bg-dark) !important"
                })
            ),
            dict(
                id=self.select_lvl_4_id,
                description='Request System',
                data=[
                    dict(value="all", label="All"),
                ],
                clearable=True,
                placeholder='Select',
                value='all',
                disabled=True,
                styles=dict(description={
                    "color": "var(--lpn-bg-dark) !important"
                })
            ),

        ]

        select_menu_column_children = [
            dbc.Row(
                [
                    dbc.Col(
                        'Company',
                        class_name='col-auto lpn-billing-unit'
                    ),

                ],
                className='mb-2rem lpn'
            )
        ]

        for d in select_menu_items:
            select_menu_column_children.append(
                dbc.Row(
                    dmc.Select(
                        id=d['id'],
                        className='lpn lpn-form-sm lpn-end-form-col',
                        data=d['data'],
                        description=d['description'],
                        rightSection=DashIconify(
                            icon="bi:chevron-down",
                            width=16,
                            className='lpn-negative-margin-top-6px'
                        ),
                        value=d['value'],
                        #placeholder=d['placeholder'],
                        disabled=d['disabled'],
                        styles=d['styles'],
                        #clearable=d['clearable']
                    ),
                    className='mb-3 lpn  lpn-extra-margin-left-4px'
                )
            )


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
                    title='',
                    orientation="v",
                    yanchor="bottom", y=0.046,
                    xanchor="right", x=1,
                    borderwidth=0,
                    font=dict(
                        size=14,
                        color='#88CACA'
                    ),
                ),
                # xref='container'

                height=333,
                # width=272,
                xaxis=dict(
                    #showgrid=False,
                    zeroline=True,

                    zerolinecolor='#405A73',
                    zerolinewidth=0.5,

                    #showticklabels=False,
                    #showline=False
                    #tickson='labels',
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
        billing_period = dbc.Stack(
            [
                html.Div('Account', className='lpn-form-sm-header'),
                dcc.Graph(
                    figure=figure,
                    style={'width': 'auto', 'height': 'auto'}
                )
            ], gap=2
        )

        billing_period = dbc.Row(
            [
                dbc.Col(
                    select_menu_column_children,
                    class_name='col-auto lpn me-4'
                ),
                dbc.Col(
                    [dbc.Row(
                        [
                            dbc.Col(
                                'Costs Incurred',
                                class_name='col-auto lpn-form-sm-header'
                            ),
                            dbc.Col(
                                DashIconify(
                                    icon="bi:info-circle",
                                    width=16,
                                ),
                                align='center',
                                class_name='col-auto me-5 lpn info-col'
                            )
                        ],
                        className='mb-0 lpn'
                    ),
                        html.Div(
                            "as of September 13, 2023, 12:35",
                            className='lpn-previous mb-4'
                        ),
                        dcc.Graph(
                            figure=figure,
                            config={'displayModeBar': False},
                        )
                    ],
                    align='center',
                    class_name='col'
                )
            ]
        )




        current_billing_period = dbc.Stack(
            [
                html.Div(
                    'September 2023',
                    id=self.current_billing_period_id,
                    className='lpn margin-left-24px'
                ),
            ],
            gap=2
        )


        current_estimates = [
            dbc.Row(
                [
                    dbc.Col(
                        'Cost Incurred',
                        class_name='col-auto lpn-form-sm-header lpn-hidden'
                    ),

                ]
            )
        ]

        current_estimates = dbc.Stack(
            current_estimates +[

                html.Div(
                    "as of September 13, 2023, 12:35",
                    className='lpn-previous lpn-hidden'
                )
            ],
        )

        estimated_bill = dbc.Stack(
            [
                html.Div(
                    "Intraday",
                    className='lpn'
                ),
                html.Div(
                    '$5,666',
                    id=self.cost_estimate_id,
                    className='lpn-number-big-2'
                ),
                html.Div(
                    'Previous Business Day: $8,666.65',
                    id=self.cost_estimate_id,
                    className='lpn-previous'
                ),
            ],
        )

        estimated_bill_2 = dbc.Stack(
            [
                html.Div(
                    "Billing Period",
                    className='lpn'
                ),
                html.Div(
                    '$65,666',
                    id=self.cost_estimate_id,
                    className='lpn-number-big-2'
                ),
                html.Div(
                    'Previous Billing Period: $118,666.65',
                    id=self.cost_estimate_id,
                    className='lpn-previous'
                ),
            ],
        )


        estimated_bill_3 = dbc.Stack(
            [
                html.Div(
                    ["Refresh Charges"],
                    className='lpn'
                ),
                html.Div(
                    '$29,667',
                    id=self.cost_estimate_id,
                    className='lpn-number-big-2'
                ),
                html.Div(
                    'Previous Billing Period: $16,666.65',
                    id=self.cost_estimate_id,
                    className='lpn-previous'
                ),
            ],
        )




        self.content = dbc.Row(
            [
                dbc.Col(
                    [
                        billing_period,

                    ],
                    class_name='col me-4'
                ),

                dbc.Col(
                    [
                        dbc.Row(current_estimates, class_name=' mb-4 '),
                        dbc.Row(
                            estimated_bill, class_name='mb-5 lpn-extra-margin-left-4px'
                        ),
                        dbc.Row(estimated_bill_2, class_name=' mb-5 lpn-extra-margin-left-4px'),
                        dbc.Row(estimated_bill_3, class_name=' lpn-extra-margin-left-4px')

                    ],
                    class_name='col-auto text-end'
                )
            ],
            className='mb-2rem margin-left-24px'
        )
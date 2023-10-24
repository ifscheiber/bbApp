from dash import html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from datetime import datetime


class Header2Row:

    def __init__(self, parent_page: str):

        self.select_account_id = f"select_account_{parent_page}_id"
        self.current_billing_period_id = f"current_billing_period_{parent_page}_id"
        self.request_count_id = f"request_count_{parent_page}_id"
        self.cost_estimate_id = f"cost_estimate_{parent_page}_id"

        billing_period = dbc.Stack(
            [
                html.Div('Account', className='lpn-form-sm-header'),
                dmc.Select(
                    placeholder='Select an Account',
                    id=self.select_account_id,
                    clearable=False,
                    icon=DashIconify(
                        icon="mdi:bank",
                        width=16,
                        className='lpn lpn-negative-margin-top-6px'
                    ),
                    data=[
                        {'value': 'all', 'label': 'All'}
                    ],
                    rightSection=DashIconify(
                        icon="bi:chevron-down",
                        width=16,
                        className='lpn-negative-margin-top-6px'
                    ),
                    value='all',
                    className='lpn lpn-form-sm',
                ),
            ], gap=2
        )

        current_billing_period = dbc.Stack(
            [
                html.Div(
                    "Current Billing Month",
                    className='lpn-form-sm-header'
                ),
                html.Div(
                    'September 2023',
                    id=self.current_billing_period_id,
                    className='lpn margin-left-24px'
                ),
            ],
            gap=2
        )

        current_requests = dbc.Stack(
            [
                html.Div(
                    "Request Count",
                    className='lpn lpn-form-sm-header'
                ),
                html.Div(
                    1500,
                    id=self.request_count_id,
                    className='lpn  margin-left-24px'
                ),
            ],
            gap=2
        )

        estimated_bill = dbc.Stack(
            [
                html.Div(
                    "Cost Estimate",
                    className='lpn-form-sm-header'
                ),
                html.Div(
                    '$255,666.65',
                    id=self.cost_estimate_id,
                    className='lpn-number-big-2 margin-left-24px'
                ),
            ],
            gap=2
        )

        self.content = dbc.Row(
            [
                dbc.Col(
                    billing_period,
                    class_name='col me-5'
                ),
                dbc.Col(
                    current_billing_period,
                    class_name='col-auto text-end me-5'
                ),
                dbc.Col(
                    current_requests,
                    class_name='col-auto text-end me-5'
                ),
                dbc.Col(
                    estimated_bill,
                    class_name='col-auto text-end'
                )
            ],
            className='mb-5'
        )
from dash import register_page, html, dcc, Output, Input, State, callback, callback_context, no_update
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
from pathlib import Path

from IPython.display import display

import pandas as pd

import plotly.express as px
from data import mock_data as md
import plotly.graph_objects as go

from views.dl_invoices.accordion_dl_invoices import AccordionDLInvoices
from views import vu

import dash_mantine_components as dmc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dash_iconify import DashIconify
from datetime import datetime


# ----------------------------------------------------------------------------------------------------------------------
# Register Page
# ----------------------------------------------------------------------------------------------------------------------
# create report


class DLInvoice:

    def __init__(self, page_url='home'):
        self.dl_billing_url_id = 'lpn_dl_billing_url_to_all_pages_id'

        # colorscale
        self.color_scale = vu.get_colorway()

        # mock data
        data_path = Path('data/mock_data/dl_details.csv')
        df = pd.read_csv(data_path)
        self.df = df.loc[df['id_account_number'] == 30314240]

        df_bval = pd.read_csv('data/mock_data/bval_details.csv')
        self.df_bval = df_bval.loc[df['id_account_number'] == 30314240]

        # Billing by Request Type
        df_request_type = self.df.groupby('request_type').sum()['total'].iloc[::-1].reset_index()

        df_request_type_pie = pd.concat(
            [df_request_type, pd.DataFrame({'request_type': ['bval'], 'total': [df_bval.total.sum()]})]).reset_index(
            drop=True)
        fig_brt = go.Figure(layout_xaxis_range=[0, df_request_type_pie['total'].sum()])

        # Loop over each request type
        for i, rt in enumerate(df_request_type_pie['request_type'].unique()):
            fig_brt.add_trace(
                go.Bar(
                    name=rt,
                    # y=[rt],  # y-axis will have request types
                    x=[df_request_type_pie['total'][i]],  # x-axis will have the values for the current cost type
                    orientation='h',
                    marker=dict(
                        color=self.color_scale[i],
                        line=dict(width=1, color='#6FB0B0')
                    ),
                    # width=0.25
                )
            )

        '''fig_brt = px.pie(df_request_type_pie, values=df_request_type_pie['total'],
                         names=df_request_type_pie['request_type'],
                         hole=0.5, color_discrete_sequence=self.color_scale)
            fig_brt.update_traces(textposition='outside', textinfo='percent+label')
                         '''

        '''

        fig_brt = make_subplots(3, 1, specs=[[{'type':'domain'}], [{'type':'domain'}],  [{'type':'domain'}]],
                            subplot_titles=['scheduled','adhoc',  'bval'], vertical_spacing=0)

        for i, rt in enumerate(df_request_type_pie['request_type']):
            fig_brt.add_trace(go.Pie(labels=[rt], values=df_request_type_pie.loc[df_request_type_pie['request_type']==rt, 'total'], scalegroup='one',
                                 name=rt), i+1, 1)'''

        # fig_brt.show()

        fig_brt.update_layout(
            dict(
                barmode='stack',
                plot_bgcolor='#102E44',
                paper_bgcolor='#102E44',
                font=dict(
                    color='#88CACA',
                    size=14
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="top", y=0,
                    xanchor="auto", x=1,
                    borderwidth=0,
                    font=dict(
                        size=14,
                        color='#88CACA'
                    ),
                ),
                # xref='container'

                height=100,
                # width=272,
                xaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False,
                    showline=False
                ),
                yaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False,
                    showline=False,
                )

            )
        )

        df_cost_type = self.df.groupby('request_type').sum()[['access', 'unique', 'refresh', 'total']].drop('adhoc')
        fig_dbct = go.Figure(layout_xaxis_range=[0, df_cost_type['total'].iloc[0] + 1])

        # Loop over each cost type
        for i, cost_type in enumerate(['access', 'unique', 'refresh']):
            fig_dbct.add_trace(
                go.Bar(
                    name=cost_type,
                    x=df_cost_type[cost_type],
                    y=['Cost Type'],
                    # x-axis will have the values for the current cost type
                    orientation='h',
                    marker=dict(
                        color=self.color_scale[i],
                        line=dict(width=1, color='#6FB0B0')
                    ),
                    # width=0.25
                )
            )

        dbct_layout = dict(
            barmode='stack',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(
                color='#88CACA',
                size=16
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top", y=0,
                xanchor="auto", x=1,
                borderwidth=0,
                font=dict(
                    size=14,
                    color='#88CACA'
                ),
            ),
            height=100,
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                showline=False,
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                showline=False,
            )

        )

        fig_dbct.update_layout(
            dbct_layout,

        )

        df_asset_type = self.df.groupby(['request_type', 'asset_type_name']).sum()['total'].reset_index()
        df_asset_type_adhoc = \
            self.df.loc[df['request_type'] == 'adhoc'].groupby(['request_type', 'asset_type_name']).sum()[
                'total'].reset_index()
        df_asset_type_adhoc['total'] = df_asset_type_adhoc['total'] / df_asset_type_adhoc['total'].sum()
        df_asset_type_schedule = \
            self.df.loc[df['request_type'] == 'scheduled'].groupby(['request_type', 'asset_type_name']).sum()[
                'total'].reset_index()
        df_asset_type_schedule['total'] = df_asset_type_schedule['total'] / df_asset_type_schedule['total'].sum()
        df_asset_type = pd.concat([df_asset_type_adhoc, df_asset_type_schedule])

        df_asset_type_p = df_asset_type.pivot(index='request_type', columns='asset_type_name',
                                              values='total').reset_index().drop(0)

        df = df_asset_type_p
        # Identify columns to be considered for 'Others'
        cols = df.columns[1:]
        sorted_cols = df[cols].sum().sort_values(ascending=False)
        top_5_cols = sorted_cols.head(5).index.tolist()

        # Condition for minimum value
        min_value = 0.05 * df[cols].sum(axis=1).values[0]
        other_cols = [col for col in cols if col not in top_5_cols or df[col].values[0] < min_value]

        # Create 'Others' column
        df['Others'] = df[other_cols].sum(axis=1)

        # Drop the columns summed into 'Others'
        df = df.drop(columns=other_cols)

        rename_dict = {
            'CMO/ABS,ABS/CMO/CMBS/Whole Loan': 'CMO/ABS/CMBS/WL',
            'Corporate/Preferred/MoneyMarket': 'Corp/Pref/MM',
            'Options/Futures/FX/Warrants': 'Opt/Fut/FX/Warr',
            'Sovereign/Supranational/Agency': 'Sov/Supra/Agency'
        }
        df_asset_type_p = df.rename(columns=rename_dict)

        fig_bar_dbat = go.Figure()

        # Loop over each cost type
        for i, asset_type in enumerate(df_asset_type_p.columns[1:]):
            fig_bar_dbat.add_trace(
                go.Bar(
                    name=asset_type,
                    # y-axis will have request types
                    x=df_asset_type_p[asset_type],  # x-axis will have the values for the current cost type
                    orientation='h',
                    marker=dict(
                        color=self.color_scale[i],
                        line=dict(width=1, color='#6FB0B0')
                    ),
                    # width=0.25,
                )
            )

        fig_bar_dbat.update_layout(
            dbct_layout
        )
        fig_bar_dbat.update_layout(
            dict(
                margin=dict(l=0, r=0, t=0, b=80),
                height=150)
        )

        grid = AccordionDLInvoices('dl_invoice_page', )

        # --------------------------------------------------------------------------------------------------------------
        # Layout
        # --------------------------------------------------------------------------------------------------------------

        account_number = dbc.Stack(
            [
                html.Div("Account Number", className='lpn-form-sm-header'),
                dmc.Select(
                    id="example-email-grid",
                    placeholder="Enter email",
                    className='lpn lpn-form-sm',
                    data=[
                        {"value": "12345678910", "label": "12345678910"},
                        {"value": "ng", "label": "Angular"},
                        {"value": "svelte", "label": "Svelte"},
                        {"value": "vue", "label": "Vue"},
                    ],
                    rightSection=DashIconify(
                        icon="bi:chevron-down",
                        width=16,
                    ),
                    value='12345678910'
                )
            ], gap=2
        )

        invoice_date = dbc.Stack(
            [
                html.Div("Invoice Date", className='lpn-form-sm-header'),
                dmc.DatePicker(
                    placeholder='Select a Date',
                    id="date-picker",
                    clearable=False,
                    value=datetime.now(),
                    rightSection=DashIconify(
                        icon="bi:calendar",
                        width=16,
                    ),
                    className='lpn-form-sm'
                ),
            ], gap=2

        )

        invoice_number = dbc.Stack(
            [
                html.Div("Invoice Number", className='lpn-form-sm-header'),
                dmc.Select(
                    id="example-email-grid",
                    placeholder="Enter email",
                    className='lpn lpn-form-sm',
                    data=[
                        {"value": "12345678910", "label": "12345678910"},
                        {"value": "ng", "label": "Angular"},
                        {"value": "svelte", "label": "Svelte"},
                        {"value": "vue", "label": "Vue"},
                    ],
                    rightSection=DashIconify(
                        icon="bi:chevron-down",
                        width=16,
                    ),
                    value='12345678910'
                ),
            ], gap=2
        )

        total_billed = dmc.Card(
            children=[
                dbc.Stack(
                    [
                        html.Div("Total Billed Amount", className='lpn-form-sm-header'),
                        html.Div("$32,355.59", className='lpn-number-big-2 margin-left-24px'),
                    ],
                    gap=2
                )
            ]
        )

        breakdown_rt = dmc.Card(
            children=[
                dmc.Stack(
                    [
                        html.Div("Billing by Request Type", className='lpn-form-sm-header'),
                        dcc.Graph(figure=fig_brt, config={'displayModeBar': False}, className='margin-left-24px'),
                    ]
                )
            ]
        )




        page_header = html.H1('Invoice Explorer', className='lpn')

        header_row = dbc.Row(
            [
                dbc.Col(account_number, class_name='col-auto me-5'),
                dbc.Col(invoice_date, class_name='col-auto me-4'),
                dbc.Col(invoice_number, class_name='col-auto'),
                dbc.Col(total_billed, class_name='auto text-end'),
            ], class_name='lpn-invoice-row'
        )

        detailed_breakdown = dbc.Stack(
            [
                html.Div("Detailed Breakdown", className='lpn-form-sm-header'),
                dmc.SegmentedControl(
                    id="segmented",
                    data=[
                        {"value": "react", "label": "Scheduled"},
                        {"value": "ng", "label": "Ad Hoc"},
                        {"value": "svelte", "label": "BVAL"},
                    ],
                ),
                dmc.SegmentedControl(
                    id="segmented",
                    data=[
                        {"value": "react", "label": "Cost Type"},
                        {"value": "ng", "label": "Data Type"},
                        {"value": "svelte", "label": "Asset Type"},
                    ],
                )
            ], gap=3
        )

        detailed_breakdown_graph = dbc.Stack(
            [
                html.Div("hidden", className='lpn-form-sm-header-hidden'),
                dcc.Graph(
                    figure=fig_bar_dbat,
                    config={'displayModeBar': False}
                )
            ], gap=3
        )


        breakdowns_row = dbc.Row(
            [
                dbc.Col(breakdown_rt,  class_name='col-4 me-5'),
                dbc.Col(
                    dbc.Row(
                        [
                            dbc.Col(detailed_breakdown,  class_name='col-auto'),
                            dbc.Col(detailed_breakdown_graph,  class_name='col')
                        ]
                    ),  class_name='col'
                )
            ]
        )


        r2 = dbc.Row(
            dbc.Col(
                grid.visualization
            )
        )

        self.visualization = html.Main(
            dbc.Container(
                [
                    page_header,
                    dbc.Stack([header_row, breakdowns_row, r2], gap=5)
                ],
                class_name='lpn-container-padded-lr'
            ),
            className='app-layout'
        )

    def define_callbacks(self):
        """
        Defines the dash.callbacks.
        Should consist of several inner functions, each specifying a callback.
        """

        pass


report = DLInvoice()


def layout():
    return report.visualization


# include callbacks
report.define_callbacks()

# register page
register_page(__name__, name='Invoice Explorer', path='/invoices-explorer')

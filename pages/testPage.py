from dash import register_page, html, dcc, Output, Input, State, Patch, callback, clientside_callback, ClientsideFunction, no_update, ctx
import dash_bootstrap_components as dbc
from pathlib import Path
from datetime import datetime
import data.mock_data.mock_data_fig as md

import numpy as np
import pandas as pd

from views import vu

import dash_mantine_components as dmc
import plotly.graph_objects as go

from dash_iconify import DashIconify
from datetime import datetime

from views.dl_invoices_home.accounts_tab_content import AccountsTabContent
from views.dl_invoices_home.drilldown_tab_content import DrilldownTabContent

from views.testPage.header_2_row import Header2Row
from views.testPage.billing_units_content import BillingUnits
from views.testPage.info_center_content import InfoCenterContent

class DLAccount:

    def __init__(self, page_url='landing'):
        # TODO: this is DataHandling and should NOT be contained here!
        # mock data
        data_path = Path('data/mock_data/dl_details.csv')
        data_path_bval = Path('data/mock_data/bval_details.csv')
        self.df = md.get_mock_table_data(data_path, data_path_bval)

        # Billing History

        # Billing by Request Type
        fig_brt = md.get_mock_data(data_path, data_path_bval)
        # Billing by Cost Type NOTE: Request Type will need to be toggled!
        fig_ct = md.get_mock_data(data_path, data_path_bval, 'ct', request_type='bval')

        # colorscale  TODO: Should be global!
        self.color_scale = vu.get_colorway()

        # Page contents
        self.header2row = Header2Row(parent_page=page_url)
        self.info_center = InfoCenterContent(parent_page=page_url)
        self.billing_units = BillingUnits(parent_page=page_url)

        # IDs of the page
        self.total_billed_amount_id = self.header2row.cost_estimate_id

        self.grid_id = self.info_center.grid_id


        # --------------------------------------------------------------------------------------------------------------
        # # Page Header -> static
        # --------------------------------------------------------------------------------------------------------------
        page_header = dbc.Row(
            [
                dbc.Col(
                    html.H1(
                        'Expense Tracker',
                        className='lpn page-header'
                    ),
                    class_name='col-auto'
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
            className='mb-2rem'
        )

        # Tabs
        tabs = dbc.Row(
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("Notifications", value="accounts"),
                            dmc.Tab("Cost Overview", value="drilldown")
                        ]
                    ),
                    dmc.TabsPanel(
                        self.info_center.content,
                        value='accounts'
                    ),
                    dmc.TabsPanel(
                        self.billing_units.content,
                        value='drilldown'
                    )
                ],
                value='accounts'
            ),
        )

        # --------------------------------------------------------------------------------------------------------------
        # Assembled Page Content
        # --------------------------------------------------------------------------------------------------------------
        self.visualization = html.Main(
            dbc.Container(
                [
                    page_header,
                    self.header2row.content,
                    tabs
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


# ----------------------------------------------------------------------------------------------------------------------
# Register Page
# ----------------------------------------------------------------------------------------------------------------------
# create report
report = DLAccount()


def layout():
    return report.visualization


# include callbacks
report.define_callbacks()

# register page
register_page(__name__, name='Home', path='/')

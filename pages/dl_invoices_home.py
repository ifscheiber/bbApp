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
from views.dl_invoices_home.header_2_row import Header2Row


class DLInvoiceHome:

    def __init__(self, page_url='home'):
        # TODO: this is DataHandling and should NOT be contained here!
        # mock data
        data_path = Path('data/mock_data/dl_details.csv')
        data_path_bval = Path('data/mock_data/bval_details.csv')
        self.df = md.get_mock_table_data(data_path, data_path_bval)

        # colorscale  TODO: Should be global!
        self.color_scale = vu.get_colorway()

        # Page contents
        self.header2row = Header2Row(parent_page=page_url)
        self.accounts_tab_content = AccountsTabContent(parent_page=page_url)
        self.drilldown_tab_content = DrilldownTabContent(parent_page=page_url)

        # IDs of the page
        self.datepicker_id = self.header2row.datepicker_id
        self.total_billed_amount_id = self.header2row.total_billed_amount_id

        self.grid_id = self.accounts_tab_content.grid_id

        self.drilldown_graph_id = self.drilldown_tab_content.graph_id
        self.select_lvl_1_id = self.drilldown_tab_content.select_lvl_1_id
        self.select_lvl_2_id = self.drilldown_tab_content.select_lvl_2_id
        self.select_lvl_3_id = self.drilldown_tab_content.select_lvl_3_id
        self.select_lvl_4_id = self.drilldown_tab_content.select_lvl_4_id

        # --------------------------------------------------------------------------------------------------------------
        # # Page Header -> static
        # --------------------------------------------------------------------------------------------------------------
        page_header = dbc.Row(
            [
                dbc.Col(
                    html.H1(
                        'Data Cost Explorer',
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
            className='mb-5'
        )

        # Tabs
        tabs = dbc.Row(
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("Accounts", value="accounts"),
                            dmc.Tab("Drilldown", value="drilldown")
                        ]
                    ),
                    dmc.TabsPanel(
                        self.accounts_tab_content.content,
                        value='accounts'
                    ),
                    dmc.TabsPanel(
                        self.drilldown_tab_content.content,
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

        @callback(
            Output(self.total_billed_amount_id, 'children'),
            Output(self.grid_id, 'rowData'),
            Output(self.grid_id, 'dashGridOptions'),
            Input(self.datepicker_id, 'value'),
            State(self.grid_id, 'dashGridOptions'),
            State(self.select_lvl_1_id, 'value'),
            State(self.select_lvl_2_id, 'value'),
            State(self.select_lvl_3_id, 'value'),
            State(self.select_lvl_4_id, 'value')
        )
        def update_on_date_change(selected_date: str, dash_grid_options: dict, select_lvl_1: str,
                                  select_lvl_2: str, select_lvl_3: str, select_lvl_4: str):

            # Define outputs
            out = dict(
                total_billed_amount=no_update,
                row_data=no_update,
                dash_grid_options=no_update,
            )

            # Prepare data for Grid
            df = self.df[['id_account_number', 'request_type', 'total']].groupby(
                ['id_account_number', 'request_type']).sum().iloc[::-1].reset_index()
            df = df.pivot(columns='request_type', values='total', index='id_account_number').reset_index()
            df['total'] = df.iloc[:, 1:].sum(axis=1)
            df['rowHeight'] = 70

            # TODO: we need to insert the graph.json for the time series (that does not exist yet.
            #  So we will call the mock data to include the figures)
            data_path = Path('data/mock_data/dl_details.csv')
            df['snapshot'] = ""
            for i, r in df.iterrows():
                fig = md.get_mock_history(data_path, selected_date)
                df.at[i, "snapshot"] = fig

            #df['snapshot'] = df['total'].apply(lambda x: [0] * 11 + [x])
            df['icon'] = 'mdi:bank'
            df = df.sort_values('total')

            aggregated_total = df['total'].sum()

            # Create a new DataFrame with the aggregated values
            aggregated_df = pd.DataFrame({
                'icon': None,
                'id_account_number': ['Total'],
                'total': [aggregated_total],
                'scheduled': [df['scheduled'].sum()],
                'adhoc': [df['adhoc'].sum()],
                'bval': [df['bval'].sum()],
                'snapshot': [""],
                'percent': 1,
                'rowHeight': 100
            })
            for i, r in aggregated_df.iterrows():
                fig = md.get_mock_history(data_path, selected_date, x_axis_ticks=True)
                aggregated_df.at[i, "snapshot"] = fig

            df['percent'] = df['total']/aggregated_total

            dash_grid_options['pinnedBottomRowData'] = aggregated_df.to_dict('records')

            # update the outputs dict
            out['row_data'] = df.to_dict('records')
            out['total_billed_amount'] = f"${aggregated_total: ,.2f}"
            out['dash_grid_options'] = dash_grid_options

            return tuple(out.values())


        clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='on_interaction_trend_column'
            ),
            Output(self.datepicker_id, 'value'),
            Input(self.grid_id, "cellRendererData"),
            State(self.grid_id, 'rowData'),
            prevent_initial_call=True
            # TODO: currently we need to go back to the update_on_date_change callback, but actually this would not be
            #  required since we can modify the graph on clientside, at least as long as we hav the underlying data
            #  stored in a e.g. dcc.Store ... Also check asynchronous functions!
        )


        @callback(
            Output(self.drilldown_graph_id, 'figure'),

            Output(self.select_lvl_2_id, 'value'),
            Output(self.select_lvl_2_id, 'disabled'),
            Output(self.select_lvl_2_id, 'data'),
            Output(self.select_lvl_2_id, 'styles'),

            Output(self.select_lvl_3_id, 'value'),
            Output(self.select_lvl_3_id, 'disabled'),
            Output(self.select_lvl_3_id, 'styles'),

            Output(self.select_lvl_4_id, 'value'),
            Output(self.select_lvl_4_id, 'disabled'),
            Output(self.select_lvl_4_id, 'data'),
            Output(self.select_lvl_4_id, 'styles'),
            Output(self.select_lvl_4_id, 'description'),

            Input(self.datepicker_id, 'value'),
            Input(self.select_lvl_1_id, 'value'),
            Input(self.select_lvl_2_id, 'value'),
            Input(self.select_lvl_3_id, 'value'),
            Input(self.select_lvl_4_id, 'value'),
        )
        def on_select_drilldown_path(date: str, select_lvl_1: str, select_lvl_2: str, select_lvl_3: str, select_lvl_4: str):

            trigger = ctx.triggered_id

            # Define outputs
            out = dict(
                drilldown_graph_figure=no_update,
                lvl_2_value=no_update,
                lvl_2_disabled=no_update,
                lvl_2_data=no_update,
                lvl_2_styles=no_update,
                lvl_3_value=no_update,
                lvl_3_disabled=no_update,
                lvl_3_styles=no_update,
                lvl_4_value=no_update,
                lvl_4_disabled=no_update,
                lvl_4_data=no_update,
                lvl_4_styles=no_update,
                lvl_4_description=no_update,
            )

            if select_lvl_1 == 'bval':
                cost_types = ['ACCESS', 'HIST', 'T2']
            else:
                cost_types = ['access', 'unique', 'refresh']


            # TODO: style_updates
            styles_active = None
            styles_disabled = {'description': {"color": "var(--lpn-bg-dark) !important"}}

            # TODO: prepare the drilldown figure
            # condition 1: all but first level are disabled  -> plot breakdown into request types
            if select_lvl_1 == 'all':
                df = self.df[['id_account_number', 'request_type', 'total']].groupby(
                    ['id_account_number', 'request_type']).sum().iloc[::-1].reset_index()
                df = df.pivot(columns='request_type', values='total', index='id_account_number').reset_index()
                df['total'] = df.iloc[:, 1:].sum(axis=1)

                # Create a new DataFrame with the aggregated values
                aggregated_df = pd.DataFrame({
                    'id_account_number': ['aggregated'],
                    'total': df['total'].sum(),
                    'scheduled': [df['scheduled'].sum()],
                    'adhoc': [df['adhoc'].sum()],
                    'bval': [df['bval'].sum()],
                })

                df = pd.concat([df, aggregated_df]).sort_values('total', ascending=False)
                drilldown = ['scheduled', 'adhoc', 'bval']

                out['lvl_2_disabled'] = True
                out['lvl_2_styles'] = styles_disabled
                out['lvl_2_value'] = 'all'
                out['lvl_3_disabled'] = True
                out['lvl_3_styles'] = styles_disabled
                out['lvl_4_value'] = 'all'
                out['lvl_4_disabled'] = True
                out['lvl_4_styles'] = styles_disabled

            # condition 2: first & 2nd  level are active  -> plot breakdown into cost type
            elif select_lvl_2 == 'all' or select_lvl_2 not in cost_types:

                '''if select_lvl_1 == 'bval':
                    cost_types = ['ACCESS', 'HIST', 'T2']
                else:
                    cost_types = ['access', 'unique', 'refresh']'''

                keep_cols = ['id_account_number'] + cost_types
                df = self.df.loc[self.df['request_type'] == select_lvl_1, keep_cols]
                df = df.groupby(['id_account_number']).sum().iloc[::-1].reset_index()

                # Create a new DataFrame with the aggregated values
                aggregated_df = {'id_account_number': ['aggregated']}
                aggregated_df.update({ct: [df[ct].sum()] for ct in cost_types})
                aggregated_df = pd.DataFrame(aggregated_df)

                df = pd.concat([df, aggregated_df])
                df['total'] = df.iloc[:, 1:].sum(axis=1)
                df = df.sort_values('total', ascending=False)

                drilldown = cost_types

                out["lvl_2_data"] = [{'value': 'all', 'label': 'All'}] + [{'value': i, 'label': i} for i in cost_types]
                out['lvl_2_disabled'] = False
                out['lvl_2_styles'] = styles_active
                out['lvl_2_value'] = 'all'
                out['lvl_3_disabled'] = True
                out['lvl_3_styles'] = styles_disabled
                out['lvl_4_disabled'] = True
                out['lvl_4_styles'] = styles_disabled
                out['lvl_4_value'] = 'all'

            # condition 3: plot breakdown into data category or asset type
            else:
                # TODO Also the value may be changed depending on what the value was before! --> to all, or remain
                #  Could be done with checking the current lel_2_value and then update accordingly!


                out["lvl_2_data"] = [{'value': 'all', 'label': 'All'}] + [{'value': i, 'label': i} for i in cost_types]


                df = self.df.loc[self.df['request_type'] == select_lvl_1]

                # condition 4: plot breakdown of single data category/asset type
                if select_lvl_4 == 'all' or (select_lvl_4 != 'all' and ctx.triggered_id == self.select_lvl_3_id):
                    drilldown_lvl = select_lvl_3
                    out["lvl_4_data"] = ([{'value': 'all', 'label': 'All'}] +
                                         [{'value': l, 'label': l} for l in df[select_lvl_3].unique()])
                    lvl_4_description_map = dict(data_category='Data Category', asset_type_name='Asset Type')
                    out['lvl_4_description'] = lvl_4_description_map[select_lvl_3]

                    if select_lvl_4 != 'all' and ctx.triggered_id == self.select_lvl_3_id:
                        out["lvl_4_value"] = 'all'

                elif select_lvl_4 != 'all':
                    df = df.loc[df[select_lvl_3] == select_lvl_4]
                    drilldown_lvl = next(iter(set.difference({'data_category', 'asset_type_name'}, {select_lvl_3})))

                else:
                    print('ERROR')

                keep_columns = [drilldown_lvl] + ['id_account_number', select_lvl_2]
                df = df[keep_columns].groupby(keep_columns[:2]).sum().iloc[::-1].reset_index()

                df = df.groupby('id_account_number', group_keys=False).apply(vu.top_5_and_other, select_lvl_2).reset_index(drop=True)
                df = df.pivot(index='id_account_number', values=select_lvl_2, columns=drilldown_lvl).reset_index()


                drilldown = df.iloc[:, 1:].keys()

                # Create a new DataFrame with the aggregated values
                aggregated_df = {'id_account_number': ['aggregated']}
                aggregated_df.update({l: [df[l].sum()] for l in drilldown})
                aggregated_df = pd.DataFrame(aggregated_df)

                df = pd.concat([df, aggregated_df])
                df['total'] = df.iloc[:, 1:].sum(axis=1)
                df = df.sort_values('total', ascending=False)

                out['lvl_3_disabled'] = False
                out['lvl_3_styles'] = styles_active
                out['lvl_4_disabled'] = False
                out['lvl_4_styles'] = styles_active



            # Create the Figure Patch
            patched_fig = Patch()
            patched_fig_lst = []

            for i, rt in enumerate(drilldown):
                patched_fig_lst.append(
                    go.Bar(
                        name=str(rt),
                        y=[str(a) for a in df['id_account_number'].unique()],  # y-axis will have accounts
                        x=df[rt],  # x-axis will have the values for the current cost type
                        orientation='h',
                        marker=dict(
                            color=self.color_scale[i],
                            line=dict(width=1, color='#B2FCFB')
                        )
                    )
                )

            patched_fig['data'] = tuple(patched_fig_lst)

            out['drilldown_graph_figure'] = patched_fig

            return tuple(out.values())


# ----------------------------------------------------------------------------------------------------------------------
# Register Page
# ----------------------------------------------------------------------------------------------------------------------
# create report
report = DLInvoiceHome()


def layout():
    return report.visualization


# include callbacks
report.define_callbacks()

# register page
register_page(__name__, name='Home', path='/os-home')

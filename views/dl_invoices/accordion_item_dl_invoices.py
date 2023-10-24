import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc
import dash_ag_grid as dag
import dash_mantine_components as dmc

from pathlib import Path


class AccordionItemDLInvoice:

    def __init__(self, parent_page: str):
        """

        :type form_ids: list
        form_ids: contaons the ids of the individual input ids

        """
        # --------------------------------------------------------------------------------------------------------------
        # IDs of the form
        # --------------------------------------------------------------------------------------------------------------
        self.input_rs_name_id = f'input_rs_name_{parent_page}'
        self.text_area_rs_description_id = f'text_area_rs_description_{parent_page}'

        self.table_req_files_id = f'table_req_files__dir_{parent_page}'
        self.table_resp_files_id = f'table_resp_files__dir_{parent_page}'

        self.button_add_req_dir = f'button_req_files_dir_{parent_page}'
        self.button_resp_files_dir_id = f'button_resp_files_dir_{parent_page}'

        # --------------------------------------------------------------------------------------------------------------
        # Table of new paths
        # --------------------------------------------------------------------------------------------------------------
        df, columnDefs, defaultColDef = self.mock_data()
        request_file_dirs_grid = dag.AgGrid(
            id="custom-components-request_file_dirs_grid",
            className="ag-theme-alpine ag-theme-accordion",
            enableEnterpriseModules=True,
            licenseKey='test',
            columnDefs=columnDefs,
            rowData=df.to_dict("records"),
            defaultColDef=defaultColDef,
            columnSize="responsiveSizeToFit",
            dashGridOptions={"domLayout": "autoHeight", "rowSelection": "multiple", "suppressAggFuncInHeader": True,

                             "autoGroupColumnDef": {
                                 "headerName": "Billing Details",
                                 "minWidth": 320,
                                 "cellRendererParams": {
                                     "suppressCount": True,
                                 },

                             },
                             "showOpenedGroup": True,
                             'groupRemoveLowestSingleChildren': True

                             },
            style={"height": 'auto'}
        )

        request_file_dirs = html.Div(
            [

                dbc.Row(
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            request_file_dirs_grid
                                        ],
                                        class_name='inner-table'
                                    ),
                                ],
                                class_name='lpn-cards-without-border'
                            ),
                        ],
                    )
                ),
            ]
        )

        # --------------------------------------------------------------------------------------------------------------
        # Visualization
        # --------------------------------------------------------------------------------------------------------------
        self.visualization = html.Div(
            children=dbc.AccordionItem(
                request_file_dirs
            )
        )


    def mock_data(self):

        data_path = Path('data/mock_data/dl_details.csv')
        my_df = pd.read_csv(data_path)
        my_df = my_df.loc[my_df['id_account_number'] == 30314240]
        my_df['year'] = my_df['start_date'].apply(lambda x: x.split('-')[0])
        my_df['month'] = my_df['start_date'].apply(lambda x: x.split('-')[1])

        columnDefs = [

                    {
                        "field": "request_type",
                        "rowGroup": True,
                        "hide": True,
                        "suppressColumnsToolPanel": True,
                    },
                    {
                        "field": "asset_type_name",
                        "rowGroup": True,
                        "hide": True,
                        "suppressColumnsToolPanel": True,
                    },
                    {
                        "field": "data_category",
                        "rowGroup": True,
                         "hide": True,
                        "suppressColumnsToolPanel": True,
                    },



                    {"field": "access", "sortable": True, "filter": True, "aggFunc": "sum",
                     "valueFormatter": {"function": "d3.format('(.2f')(params.value)"}, 'maxWidth': 150,
                     'columnGroupShow': 'open'},
                    {"field": "unique", "sortable": True, "filter": True, "aggFunc": "sum",
                     "valueFormatter": {"function": "d3.format('(.2f')(params.value)"}, 'maxWidth': 150,
                     'columnGroupShow': 'open'},
                    {"field": "refresh", "sortable": True, "filter": True, "aggFunc": "sum",
                     "valueFormatter": {"function": "d3.format('(.2f')(params.value)"}, 'maxWidth': 150,
                     'columnGroupShow': 'open'},
                    {"field": "total", "sortable": True, "filter": True, "aggFunc": "sum",
                     "valueFormatter": {"function": "d3.format('(.2f')(params.value)"}, 'maxWidth': 150,
                     'columnGroupShow': 'closed'},

        ]

        defaultColDef = {
            "filter": "agNumberColumnFilter",
            # "resizable": True,
            "sortable": True,
            # "editable": False,
        }

        return my_df, columnDefs, defaultColDef

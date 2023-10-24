import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc
import dash_ag_grid as dag
import dash_mantine_components as dmc


class AccordionItemRequestSystem:

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
        # Input Request System Name
        # --------------------------------------------------------------------------------------------------------------
        input_rs_name = dbc.FormFloating(
            [
                dbc.Input(
                    id=self.input_rs_name_id,
                    placeholder="Enter Request System Name",
                    disabled=False,
                    class_name='lpn-form-element-dark-mode lpn-margin-lr', ),
                dbc.Label("Name"),

            ],
            class_name='lpn-form-element-dark-mode lpn-margin-lr'
        )

        # --------------------------------------------------------------------------------------------------------------
        # TextArea Request system description
        # --------------------------------------------------------------------------------------------------------------
        text_area_rs_description = dbc.FormFloating(
            [
                dbc.Textarea(
                    id=self.text_area_rs_description_id,
                    placeholder="Request System Description",
                    disabled=False,
                    class_name='lpn-form-element-dark-mode lpn-margin-lr',
                ),
                dbc.Label("Description")
            ],
            class_name='lpn-form-element-dark-mode lpn-margin-lr'
        )

        # --------------------------------------------------------------------------------------------------------------
        # Table of new paths
        # --------------------------------------------------------------------------------------------------------------
        df, columnDefs, defaultColDef = self.mock_data()
        request_file_dirs_grid = dag.AgGrid(
            id="custom-components-request_file_dirs_grid",
            className="ag-theme-alpine ag-theme-accordion",
            columnDefs=columnDefs,
            rowData=df.to_dict("records"),
            defaultColDef=defaultColDef,
            columnSize="responsiveSizeToFit",
            dashGridOptions={"domLayout": "autoHeight", "singleClickEdit": True, "stopEditingWhenCellsLoseFocus": True},
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
                                        ]
                                    ),
                                ],
                                class_name='lpn-cards-without-border'
                            ),
                        ],
                        className='lpn-row-no-padding-lr'
                    )
                ),
            ]
        )

        # --------------------------------------------------------------------------------------------------------------
        # Table of new paths
        # --------------------------------------------------------------------------------------------------------------
        df, columnDefs, defaultColDef = self.mock_data()
        response_file_dirs_grid = dag.AgGrid(
            id="custom-components-request_file_dirs_grid",
            className="ag-theme-alpine ag-theme-accordion",
            columnDefs=columnDefs,
            rowData=df.to_dict("records"),
            defaultColDef=defaultColDef,
            columnSize="responsiveSizeToFit",
            dashGridOptions={"domLayout": "autoHeight", "singleClickEdit": True, "stopEditingWhenCellsLoseFocus": True},
            style={"height": 'auto'}
        )

        response_file_dirs = html.Div(
            [

                dbc.Row(
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            response_file_dirs_grid
                                        ]
                                    ),
                                ],
                                class_name='lpn-cards-without-border'
                            ),
                        ],
                        className='lpn-row-no-padding-lr'
                    )
                ),
            ]
        )


        # --------------------------------------------------------------------------------------------------------------
        # Assembled form
        # --------------------------------------------------------------------------------------------------------------
        form = dbc.AccordionItem(
            [
                dbc.Stack([
                    input_rs_name,
                    text_area_rs_description,
                    request_file_dirs,
                    response_file_dirs
                ],
                    gap=3
                ),

            ]
        )

        self.visualization = html.Div(
            children=[form],
        )




    def mock_data(self):
        data = {
            "directory_path": ['some random text'] + [''],

        }

        df = pd.DataFrame(data)

        columnDefs = [
            {
                "headerName": "Request File Directory Paths",
                "field": "directory_path",
                #"cellRenderer": "StockLink",
                "tooltipField": "directory_id",
                "tooltipComponent": "CustomTooltip",
            },
        ]

        defaultColDef = {
            "filter": "agNumberColumnFilter",
            #"resizable": True,
            "sortable": True,
            "editable": True,
        }

        return df, columnDefs, defaultColDef








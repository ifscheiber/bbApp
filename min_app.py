import datetime

from dash import Dash, page_container, page_registry, dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
import dash_iconify
from data.mock_data import mock_data_accounts as md

"""
Tree Data
"""

import dash_ag_grid as dag
from dash import Dash, Input, Output, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__)

mock_data, columnDefs, pinned_row = md.get_mock_data_hierachy()
rowData = mock_data.to_dict('records')
pinned_row = pinned_row.to_dict('records')


grid = html.Div(
    [
        dag.AgGrid(
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

                'pinnedBottomRowData': pinned_row
            },
            rowData=rowData,
            enableEnterpriseModules=True,

        ),
    ]
)

app.layout = html.Div(
    [
        dcc.Markdown("Example: Organisational Hierarchy using Tree Data "),
        grid,
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)



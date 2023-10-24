from dash import Dash, html
import dash_ag_grid as dag
import pandas as pd

from dash_framework.visualization_items.visualization_item import VisualizationItem
import dash_bootstrap_components as dbc


class AgGridDataLicense(VisualizationItem):

    def __init__(self, parent_page: str, visualization_item_id: str, data_handler, tables_to_query, title: str = None,
                 custom_css: str = None, column_css: int = None):
        """

        :type form_ids: list
        form_ids: contaons the ids of the individual input ids

        """
        super(AgGridDataLicense, self).__init__(visualization_item_id, title, custom_css, column_css,
                                              no_bottom_top_padding=True, column_align='center')


        data = {
            "ticker": ["AAPL", "MSFT", "AMZN", "GOOGL"],
            "price": [154.99, 268.65, 100.47, 96.75],
            "volume": ["Low", "High", "Low", "High"],
            "binary": [False, True, False, False],
            "edit": [{ "className": "bi bi-pencil", "n_clicks":0} for i in range(4)],
            "analyse": [{"className": "bi bi-eye", "n_clicks":0} for i in range(4)],
            "action": ["buy", "sell", "hold", "buy"],
        }
        df = pd.DataFrame(data)

        columnDefs = [
            {
                "headerName": "Data License",
                "field": "ticker",
                #"cellRenderer": "StockLink",
                "tooltipField": "ticker",
                "tooltipComponent": "CustomTooltip",
            },
            {
                "headerName": "Account Number",
                "field": "price",
                "valueFormatter": {"function": """d3.format("($,.2f")(params.value)"""},
                "editable": True,
            },
            {
                "headerName": "Account Description",
                "field": "volume",
                #"cellRenderer": "Tags",
                "editable": True,
            },

            {
                "headerName": "",
                "field": "edit",
                "type": "rightAligned",
                "cellRenderer": "CustomButton",
                "sortable":False,
                "filter": None,

            },
            {   "headerName": "",
                "field": "analyse",
                "type": "rightAligned",
                "cellRenderer": "CustomButton",
                "sortable":False,
                "filter": None,

                },

        ]


        defaultColDef = {
            "filter": "agNumberColumnFilter",
            #"resizable": True,
            "sortable": True,
            "editable": False,
        }


        grid = dag.AgGrid(
            id="custom-components-grid",
            className="ag-theme-alpine ag-theme-lpn-dark",
            columnDefs=columnDefs,
            rowData=df.to_dict("records"),
            defaultColDef=defaultColDef,
            columnSize="sizeToFit",
            columnSizeOptions= {
            'columnLimits': [
                {'key': 'edit', 'minWidth': 40, 'maxWidth': 60},
                {'key': 'analyse', 'minWidth': 40, 'maxWidth': 60},
                {'key': 'price', 'minWidth': 220, 'maxWidth': 220},
                {'key': 'volume', 'minWidth': 300, 'maxWidth': 300},
            ],
                'defaultMinWidth': 175
            },
            style={'height': '240px'},
            dashGridOptions={"tooltipShowDelay": 100, "rowHeight":48},

        )

        '''grid = dag.AgGrid(
            id="get-started-example-basic",
            rowData=df.to_dict("records"),
            columnDefs=columnDefs,
            columnSize="sizeToFit",
            className="ag-theme-alpine ag-theme-lpn-dark",
        )'''

        self.visualization = html.Div(
            children=dbc.Row(
                dbc.Col(grid, align='center'),
                justify='center',
                style= {'width': '100%', 'height': '270px', 'margin-left': 'auto', 'margin-right': 'auto', 'valign': 'center'}
            ),
            className='container ',
            style= {'border': '1px solid var(--color-aqua-200)', 'border-radius': '0.375rem' , 'width': '900px',
                    'height': '300px',}
        )

# --------------------------------------------------------------------------------------------------------------
        # IDs of the form
        # --------------------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from data.mock_data import mock_data_accounts as md


class InfoCenterContent:

    def __init__(self, parent_page: str):
        """

        :param parent_page: The name/id of the parent page. Required for construction of IDs of the Grid
        """
        # IDs of the element
        self.grid_id = f"account_grid_{parent_page}_id"

        # Define the columns
        column_defs, row_data = md.get_alert_table()

        grid = dag.AgGrid(
            className="ag-theme-alpine ag-theme-accordion headers1",
            enableEnterpriseModules=True,
            licenseKey='test',
            columnDefs=column_defs,
            rowData=row_data,
            columnSize="responsiveSizeToFit",
            dashGridOptions=dict(
                domLayout="autoHeight",
                tooltipShowDelay=250,
                headerHeight= 0
            ),
            style={"height": 'auto'}
        )

        self.content = dbc.Row(grid)


'''# the 'Snapshot'  TODO: replace by plotly figure!
            dict(
                field="snapshot",
                headerName='Trend',
                cellRenderer="agSparklineCellRenderer",
                cellRendererParams=dict(
                    sparklineOptions=dict(
                        type='column',
                        fill='#91cc75',
                        # stroke= '#91cc75',
                        highlightStyle=dict(
                            fill='orange'
                        ),
                        paddingInner=0.1,
                        paddingOuter=0.1,
                        padding=dict(
                            top=12
                        ),
                        label=dict(
                            enabled=False,
                            placement='outsideEnd'
                        ),
                        axis=dict(
                            stroke='#405A73',
                            strokeWidth=0
                        )
                    )
                )
            ),'''

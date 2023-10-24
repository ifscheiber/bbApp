import numpy as np
import pandas as pd

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify


class AccountsTabContent:

    def __init__(self, parent_page: str):
        """

        :param parent_page: The name/id of the parent page. Required for construction of IDs of the Grid
        """
        # IDs of the element
        self.grid_id = f"account_grid_{parent_page}_id"

        # Define the columns
        column_defs = [
            # the links to the accounts-page
            dict(
                field="icon",
                headerName='',
                cellRendererSelector=dict(function='getIcon(params)'),
                minWidth=50,
                maxWidth=50,
                cellStyle=dict(
                    styleConditions=[
                        dict(
                            condition="params.data.id_account_number == 'Total'",
                            style={"padding-bottom": "30px"}
                        ),
                    ]
                )
            ),

            # the account number
            dict(
                field="id_account_number",
                headerName='Account',
                rowGroup=False,
                minWidth=111,
                maxWidth=145,
                cellStyle=dict(
                    styleConditions=[
                        dict(
                            condition="params.data.id_account_number == 'Total'",
                            style={"padding-bottom": "30px"}
                        ),
                    ]
                )
            ),


                    # the amount billed for the 'scheduled'-requests
                    dict(
                        field="scheduled",
                        headerName='Scheduled',
                        maxWidth=135,
                        valueFormatter=dict(function="d3.format('($,.2f')(params.value)"),
                        type='rightAligned',
                        cellStyle=dict(
                            styleConditions=[
                                dict(
                                    condition="params.data.id_account_number == 'Total'",
                                    style={"padding-bottom": "30px"}
                                ),
                            ]
                        )
                    ),

                    # the amount billed for the 'ad hoc'-requests
                    dict(
                        field="adhoc",
                        headerName='Ad Hoc',
                        rowGroup=False,
                        minWidth=102,
                        maxWidth=125,
                        type='rightAligned',
                        valueFormatter=dict(function="d3.format('($,.2f')(params.value)"),
                        cellStyle=dict(
                            styleConditions=[
                                dict(
                                    condition="params.data.id_account_number == 'Total'",
                                    style={"padding-bottom": "30px"}
                                ),
                            ]
                        )
                    ),

                    # the amount billed for the 'BVAL'-requests
                    dict(
                        field="bval",
                        headerName='BVAL',
                        rowGroup=False,
                        minWidth=102,
                        maxWidth=125,
                        valueFormatter=dict(function="d3.format('($,.2f')(params.value)"),
                        type='rightAligned',
                        cellStyle=dict(
                            styleConditions=[
                                dict(
                                    condition="params.data.id_account_number == 'Total'",
                                    style={"padding-bottom": "30px"}
                                ),
                            ]
                        )
                    ),

                    # the absolute amount billed for the month
                    dict(
                        field='total',
                        headerName='\u03a3',
                        rowGroup=False,
                        maxWidth=150,
                        minWidth=102,
                        valueFormatter=dict(function="d3.format('($,.2f')(params.value)"),
                        type='rightAligned',
                        cellStyle=dict(
                            styleConditions=[
                                dict(
                                    condition="params.data.id_account_number == 'Total'",
                                    style={"padding-bottom": "30px"}
                                ),
                            ]
                        )
                    ),

            # the absolute amount billed for the month
            dict(
                field='percent',
                headerName='%',
                headerTooltip='% of Total',
                suppressMenu=True,
                rowGroup=False,
                minWidth=60,
                maxWidth=75,
                valueFormatter=dict(function="d3.format('(.1%')(params.value)"),
                type='rightAligned',
                cellStyle=dict(
                    styleConditions=[
                        dict(
                            condition="params.data.id_account_number == 'Total'",
                            style={"padding-bottom": "30px"}
                        ),
                    ]
                )
            ),


            # the ''Trend' of total
            dict(
                field="snapshot",

                cellRenderer="DCC_GraphClickData",
                headerName="Trend",
                minWidth=450,
                #type='rightAligned',
                cellStyle={"fontWeight": "normal"},
                #headerClass= 'ag-right-aligned-header'

            ),
        ]

        # Conditional Style for the pinned 'Aggregation' row!
        get_row_style = dict(
            styleConditions=[
                dict(
                    condition="params.data.id_account_number == 'Total'",
                    style=dict(
                        fontWeight='bolder',
                        # align='start',
                        border='none',
                        borderTop="1px solid #405A73",
                    ),
                )
            ]
        )

        grid = dag.AgGrid(
            id=self.grid_id,
            className="ag-theme-alpine ag-theme-accordion headers1",
            enableEnterpriseModules=True,
            licenseKey='test',
            columnDefs=column_defs,
            columnSize="responsiveSizeToFit",
            dashGridOptions=dict(
                domLayout="autoHeight",
                rowSelection="multiple",
                suppressAggFuncInHeader=True,
                showOpenedGroup=True,
                groupRemoveLowestSingleChildren=True,
                getRowHeight={"function": "params.data.rowHeight"},
                tooltipShowDelay=250
            ),
            getRowStyle=get_row_style,
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

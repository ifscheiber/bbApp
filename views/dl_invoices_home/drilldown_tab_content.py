from dash import dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.graph_objects as go


class DrilldownTabContent:

    def __init__(self, parent_page: str):

        # IDs of the element
        self.graph_id = f"drilldown_graph_{parent_page}_id"
        self.select_lvl_1_id = f"select_lvl_1_{parent_page}_id"
        self.select_lvl_2_id = f"select_lvl_2_{parent_page}_id"
        self.select_lvl_3_id = f"select_lvl_3_{parent_page}_id"
        self.select_lvl_4_id = f"select_lvl_4_{parent_page}_id"

        select_menu_items = [
            dict(
                id=self.select_lvl_1_id,
                description='Request Type',
                data=[
                    dict(value="all", label="All"),
                    dict(value="scheduled", label="Scheduled"),
                    dict(value="adhoc", label="Ad Hoc"),
                    dict(value="bval", label="BVAL")
                ],
                value='all',
                disabled=False,
                styles=None
            ),
            dict(
                id=self.select_lvl_2_id,
                description='Cost Type',
                data=[
                    dict(value="all", label="All")
                ],
                value='all',
                disabled=True,
                styles=dict(description={
                    "color": "var(--lpn-bg-dark) !important"
                })
            ),
            dict(
                id=self.select_lvl_3_id,
                description='Level 3',
                data=[
                    dict(value="data_category", label="Data Category"),
                    dict(value="asset_type_name", label="Asset Type")
                ],
                value="data_category",
                disabled=True,
                styles=dict(description={
                    "color": "var(--lpn-bg-dark) !important"
                })
            ),
            dict(
                id=self.select_lvl_4_id,
                description='Data Category',
                data=[
                    dict(value="all", label="All"),
                ],
                value='all',
                disabled=True,
                styles=dict(description={
                    "color": "var(--lpn-bg-dark) !important"
                })
            ),

        ]

        select_menu_column_children = [
            dbc.Row(
                [
                    dbc.Col(
                        'Select Path',
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
                className='mb-4 lpn'
            )
        ]

        for d in select_menu_items:
            select_menu_column_children.append(
                dbc.Row(
                    dmc.Select(
                        id=d['id'],
                        className='lpn lpn-form-sm lpn-end-form-col',
                        data=d['data'],
                        description=d['description'],
                        rightSection=DashIconify(
                            icon="bi:chevron-down",
                            width=16,
                            className='lpn-negative-margin-top-6px'
                        ),
                        value=d['value'],
                        disabled=d['disabled'],
                        styles=d['styles']
                    ),
                    className='mb-3 lpn'
                )
            )

        # initialize the figure
        fig = go.Figure()
        fig.update_layout(
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
                    orientation="v",
                    #yanchor="top", y=1.05,
                    #xanchor="left", x=1,
                    borderwidth=0,
                    font=dict(
                        size=14,
                        color='#88CACA'
                    ),
                ),
                # xref='container'

                height=300,
                # width=272,
                xaxis=dict(
                    #showgrid=False,
                    zeroline=True,

                    zerolinecolor='#405A73',
                    zerolinewidth=0.5,

                    #showticklabels=False,
                    #showline=False
                    tickson='labels',
                    tickprefix='$',
                    gridcolor='#405A73',

                ),

                yaxis=dict(
                    showgrid=False,
                    zeroline=False,

                    zerolinecolor='#405A73',
                    zerolinewidth=0.5,
                    showticklabels=True,
                    showline=False,
                    #ticklen = 100,
                    tickson='labels',
                    ticksuffix=' '
                )

            )
        )

        self.content = dbc.Row(
            [
                dbc.Col(
                    select_menu_column_children,
                    class_name='col-auto lpn me-5'
                ),
                dbc.Col(
                    dcc.Graph(
                        figure=fig,
                        id=self.graph_id,
                        config={'displayModeBar': False},
                        className='margin-left-24px'
                    ),
                    align='center',
                    class_name='col'
                )
            ]
        )

import random

import pandas as pd
import dash
from dash import html, dcc
import dash_ag_grid as dag
import views.utils as vu


def get_mock_data():
    business_units = ['Buy Side', 'Buy Side', 'Buy Side', 'Sell Side']
    optimization_sets = ['opt_set_1', 'opt_set_1', 'opt_set_2', 'opt_set_3']
    accounts = ['account 1', 'account 2', 'account 3', 'account_4']
    request_systems = ['res_1', 'res_2', 'res_3', 'res_4']
    purpose = ['some text', 'that', 'explains the', 'exact purpose']

    columnDefs = [
        # Row group by country and by year is enabled.
        {
            "field": "bunit",
            "rowGroup": True,
            "hide": True,
            "suppressColumnsToolPanel": True,
        },
        {
            "field": "optimization_sets",
            "rowGroup": True,
            "hide": True,
            "suppressColumnsToolPanel": True,
        },
        {
            "field": "accounts",
            # "pivot": True,
            "hide": True,
            "suppressColumnsToolPanel": True,
        },
        {"field": "purpose", "suppressColumnsToolPanel": True, },
    ]


def get_mock_data_hierachy():
    systems = [
        ['Buy Side'],
        ['Buy Side', 'opt_set_1'],
        ['Buy Side', 'opt_set_1', 'account_1'],
        ['Buy Side', 'opt_set_1', 'account_1', 'req_sys_1'],
        ['Buy Side', 'opt_set_1', 'account_1', 'req_sys_2'],
        ['Buy Side', 'opt_set_1', 'account_2'],
        ['Buy Side', 'opt_set_1', 'account_2', 'req_sys_3'],
        ['Buy Side', 'account_3'],
        ['Buy Side', 'account_3', 'req_sys_3'],
        ['Buy Side', 'opt_set_2'],
        ['Buy Side', 'opt_set_2', 'account_4'],
        ['Buy Side', 'opt_set_2', 'account_4', 'req_sys_4'],
        ['Sell Side'],
        ['Sell Side', 'opt_set_3', ],
        ['Sell Side', 'opt_set_3', 'account_4'],
        ['Sell Side', 'opt_set_3', 'account_4', 'req_sys_5'],

    ]

    type = ['', 'optimization_set', 'account', 'request_system', 'request_system', 'account', 'request_system',
            'account', 'request_system', 'optimization_set', 'account', 'request_system', '', 'optimization_set',
            'account', 'request_system', ]

    purpose = ['',
               'some description on the grouping',
               'The purpose of this account',
               'the purpose of that accounts request system',
               'the purpose of that accounts request system',
               'The purpose of this account',
               'the purpose of that accounts request system',
               'The purpose of this account',
               'the purpose of that accounts request system',
               'some description on the grouping',
               'The purpose of this account',
               'the purpose of that accounts request system',
               '',
               'some description on the grouping',
               'The purpose of this account',
               'the purpose of that accounts request system',
               ]

    today_cost = [
        None, None, None, 50, 50, None, 1000, None, 200, None, None, 150, None, None, None, 150
    ]

    prev_cost_change = [
        None, None, None, 20, -50, None, 1000, None, -200, None, None, 25, None, None, None, 150,
    ]

    links = [''] + ['bi:box-arrow-in-up-right'] * (len(systems) - 2) + ['']

    mock_data = pd.DataFrame(
        dict(
            bunit=systems,
            type=type,
            purpose=purpose,
            current_cost=today_cost,
            prev_cost_change=prev_cost_change,
            icon=links
        )
    )

    pinned_row = pd.DataFrame(
        dict(
            bunit='TOTAL',
            type='',
            purpose='',
            current_cost=2000,
            prev_cost_change=10,
            icon=None
        ), index=[5]
    )

    column_def = [
        # dict(field='bunit', headerName='tstem'),
        dict(field='purpose', headerName='Description'),

        dict(field='current_cost', headerName='Todays Cost', aggFunc='sum', type="rightAligned", ),
        dict(field='prev_cost_change', headerName='Change', aggFunc='sum', type="rightAligned", ),


    ]

    return mock_data, column_def, pinned_row


mock_data, columnDefs, pinned_row = get_mock_data_hierachy()

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dag.AgGrid(
            enableEnterpriseModules=True,
            columnDefs=columnDefs,
            rowData=mock_data.to_dict("records"),
            defaultColDef={"resizable": True},
            dashGridOptions={
                "autoGroupColumnDef": {
                    "headerName": "Organisation Hierarchy",
                    "minWidth": 300,
                    "cellRendererParams": {
                        "suppressCount": True,
                    },
                },
                "getDataPath": {"function": "getDataPath(params)"},
                "groupDefaultExpanded": -1,
                "treeData": True,
                "pinnedBottomRowData": [pinned_row.to_dict('records')]
            }
        ),
    ]
)

import plotly.express as px
from pandas.tseries.offsets import MonthEnd


def get_random_data(start_date, billing_month: str):
    end_of_month = pd.to_datetime(start_date) + MonthEnd(0)

    dates = pd.date_range(start_date, end_of_month, freq='D')
    random_numbers = [random.randint(0, 2500) for _ in range(len(dates))]
    df = pd.DataFrame({'date': dates, 'cost': random_numbers})
    df['billing_month'] = billing_month
    df['day'] = df['date'].dt.day
    df['cumulative_cost'] = df['cost'].cumsum()
    return df


def get_mock_line_chart_data():
    df = pd.concat([get_random_data('06/01/2023', 'current'),
                    get_random_data('05/01/2023', 'previous')])

    line_chart = px.line(df, x='day', y='cumulative_cost', color='billing_month', markers=True,
                         color_discrete_sequence=vu.get_colorway())
    # bar_chart = px.bar(df, x='day', y='cost', color='billing_month', barmode = 'group')
    # bar_chart.show()
    return line_chart


def get_alert_table():
    urgency = [
        ['mdi:alert-outline', 'red', '1.25rem'],
        ['mdi:information-outline', 'var(--color-chart-green)', '1.25rem'],
        ['mdi:information-outline', 'var(--primary-text-color)', '1.25rem']
    ]
    billing_unit = ['OS 123456', 'A 456789', 'RS 777856']
    description = ['Exceeded Next Band', 'Approaches next band', 'Large Request']
    date = [pd.to_datetime('12-09-2023'), pd.to_datetime('10-09-2023'), pd.to_datetime('09-09-2023')]

    checkbox = [1, 2, 3]
    link = [{'icon': 'bi:box-arrow-in-up-right', 'color': 'var(--primary-text-color)', 'size': '0.725rem'}] * 3



    df = pd.DataFrame(
        dict(
            urgency=urgency,
            billing_unit=billing_unit,
            description=description,
            date=date,
            checkbox=checkbox,
            link=link
        )
    )

    column_def = [
        dict(
            field='urgency',
            headerName='',
            cellRendererSelector=dict(function='getIcon(params)'),
            minWidth=33,
            maxWidth=33,
            cellStyle=dict(
                styleConditions=[
                    dict(
                        condition="params.data.id_account_number == 'Total'",
                        style={"padding-bottom": "30px"}
                    ),
                ]
            )
        ),
        dict(field='billing_unit', headerName='Billing Unit'),

        dict(field='description', headerName='Description'),
        dict(field='date', headerName='Date'),


    ]

    return column_def, df.to_dict('records')


if __name__ == "__main__":
    get_mock_line_chart_data()


'''
dict(
            field="link",
            headerName='',
            cellRendererSelector={'function': 'getTextWithLinkIcon(params)'},
            #cellRenderer='TextWithLinkIcon',
            #cellRendererParams= {
            #    "variant": "outline",
            #    "icon": "ic:baseline-shopping-cart",
            #    "color": "green",
            #    "radius": "xl"
            #},
            #minWidth=50,
            #maxWidth=50,
            cellStyle=dict(
                styleConditions=[
                    dict(
                        condition="params.data.id_account_number == 'Total'",
                        style={"padding-bottom": "30px"}
                    ),
                ]
            )
        ),

'''
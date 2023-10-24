import numpy as np
import pandas as pd
from views import vu
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

import random
import dash_ag_grid as dag
from datetime import datetime, timedelta

from data.data_handler import ScopedSession

# ----------------------------------------------------------------------------------------------------------------------
# import invoice packages for all accounts
# ----------------------------------------------------------------------------------------------------------------------
l_id_account_number = [30395902, 30412720, 30314240]
l_invoice_dt = ["202209"]


def get_mock_history(data_path, selected_date, x_axis_ticks=False):
    fig_margin_bottom = 10
    if x_axis_ticks:
        fig_margin_bottom = 30

    df_sa = pd.read_csv(data_path)
    df = df_sa[['id_account_number', 'total']].groupby('id_account_number').sum().reset_index()

    # Dates for the last three months of 2022 and the first nine months of 2023
    dates = pd.date_range(start='2022-09-01', end='2023-09-01', freq='MS')
    mock_data = pd.DataFrame()

    # Generate mock data
    for date in dates:
        for index, row in df.iterrows():
            new_row = {
                'Date': date,
                'id_account_number': row['id_account_number'],
                'total': row['total'] * random.uniform(0.8, 1.2), # vary the total by +/- 20%
            }
            mock_data = pd.concat([mock_data, pd.DataFrame(new_row, index= [len(mock_data)]), ])

    # Convert 'Date' to datetime format
    mock_data['Date'] = pd.to_datetime(mock_data['Date'])

    # Convert 'id_account_number' to int
    mock_data['id_account_number'] = mock_data['id_account_number'].astype(int)

    df = mock_data

    # TODO: Find the selected date in the data and get its position
    dt_array = df.Date.unique()
    selected_date = pd.to_datetime(selected_date)

    # Extract year and month from the date and the DatetimeArray
    target_ym = (selected_date.year, selected_date.month)
    array_ym = (dt_array.year, dt_array.month)

    # Find the index of the month and year in the DatetimeArray
    index = np.asarray((array_ym[0] == target_ym[0]) & (array_ym[1] == target_ym[1])).nonzero()[0]

    if index.size:
        index = index[0]
    else:
        index = 11




    #fig = px.bar(mock_data, x='Date', y='total', color='id_account_number')
    colorway = vu.get_colorway()
    highlight_colorway = vu.get_highlight_colorway()
    fig = go.Figure()

    # Loop over each request type
    for i, at in enumerate(df['id_account_number'].unique()):
        color_list = [colorway[i]] * len(df['Date'].unique())
        color_list[index] = highlight_colorway[i]

        fig.add_trace(
            go.Bar(
                name=str(at),
                y=df[df['id_account_number'] == at]['total'],  # y-axis will have accounts
                x=df[df['id_account_number'] == at]['Date'],  # x-axis will have the for the Date
                orientation='v',
                marker=dict(
                    color=color_list,
                    line=dict(width=1, color='#6FB0B0')
                ),
            )
        )

    mintick = int(df.groupby('Date').sum().total.max()*0.6)

    fig.update_layout(
        barmode='stack',
        plot_bgcolor='#102E44',
        paper_bgcolor='#102E44',

        font=dict(
            color='#88CACA',
            size=14
        ),
        margin=dict(l=20, r=20, t=0, b=fig_margin_bottom),
        showlegend=False,
        legend=dict(
            orientation="v",
            yanchor="top", y=1.05,
            xanchor="left", x=1.025,
            borderwidth=0,
            font=dict(
                size=14,
                color='#88CACA',
            ),
        ),
        # xref='container'

        # height=52, TODO
        width=450,


        yaxis=dict(
            showgrid=True,
            #zeroline=False,

            zerolinecolor='#405A73',
            zerolinewidth=0.5,
            #zeroline=False,
            showticklabels=True,
            showline=False,
            ticksuffix=' ',
            #showticksuffix='last',
    tickprefix='$',
            #showtickprefix='last',
    gridcolor='#405A73',
            tickfont=dict(
              size=12,

            ),
            #tick0=mintick,
            dtick=mintick,  # By setting dticks, the tickmode is 'linear'! auto will not work!
            #tickmode='auto',
            #nticks=2,
            #ticklabelstep=1
            #tickvals = [0,mintick]


        ),



        xaxis=dict(
            showticklabels=x_axis_ticks,
            #tickvals=df['Date'].unique(),
            showgrid=False,
            showline=False,
            zeroline=False,
            zerolinecolor='#405A73',
            tickfont=dict(
                size=12
            ),
            dtick="M1",
            tickformat="%b\n%Y"
    #rangeslider_visible=True,

        )
    )
    '''
    rangeselector=dict(
                buttons=[
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ],
                activecolor='#405A73',
                bgcolor='#102E44',
                borderwidth=0,
                yanchor="top", y=1.2,
                xanchor="right", x=1.125,

            )
    
    '''

    #fig.data[2].on_hover(print('mmm'))

    #fig.show()

    return fig


def get_mock_data(data_path, data_path_bval, drill_down='rt', request_type = 'scheduled'):

    # load the csv files
    df_sa = pd.read_csv(data_path)
    df_bval = pd.read_csv(data_path_bval)

    # Billing by Request Type
    df_sa_rt = df_sa.groupby(['id_account_number', 'request_type']).sum().iloc[::-1].reset_index()
    df_bval_rt = df_bval.groupby('id_account_number').sum().iloc[::-1].reset_index()
    df_bval_rt['request_type'] = 'bval'
    df_rt = pd.concat([df_sa_rt, df_bval_rt]).reset_index(drop=True).sort_values(['id_account_number'])
    df_rt_all = df_rt.groupby('request_type').sum().reset_index()
    df_rt_all['id_account_number'] = 'aggregated'
    df_rt = pd.concat([df_rt_all, df_rt]).reset_index(drop=True)

    if drill_down == 'rt':
        # Ensure that for every account all request types are present (i.e. if missing N/A is inserted)
        pivot_df = df_rt.pivot(index='id_account_number', columns='request_type', values='total')
        pivot_df.fillna(np.nan, inplace=True)
        df_rt = pivot_df.stack(dropna=False).reset_index().rename(columns={0: 'total'})

    elif drill_down == 'ct':

        pivoted_df = pd.DataFrame()
        for ct in ['access', 'unique', 'refresh', 'ACCESS', 'HIST', 'T2', 'total']:
            pivot_df = df_rt.pivot(index='id_account_number', columns='request_type', values=ct)
            pivot_df.fillna(np.nan, inplace=True)
            pivot_df = pivot_df.stack(dropna=False).reset_index().rename(columns={0: ct})
            if pivoted_df.empty:
                pivoted_df = pivot_df
            else:
                pivoted_df = pivot_df.merge(pivoted_df, on=['id_account_number', 'request_type'])


        df_rt = pivoted_df
        #.loc[~pivoted_df['request_type'].isin(['adhoc', 'bval'])]



    # Sort by the total account bill (highest last)
    grouped_total = df_rt.groupby('id_account_number')['total'].sum()
    df_rt = (df_rt.merge(grouped_total, on='id_account_number', suffixes=('', '_sum'))
             .sort_values(by='total_sum', ascending=False)
             .drop(columns=['total_sum']))  # TODO: keep the sum total and annotate


    #plot
    fig_brt = plot_stacked_grouped_bar_chart(df_rt, drill_down, request_type)
    # TODO: should we remove values of 0 from the legend!  -> but then we should make the statement!
    #  print(df.iloc[:, 1:].groupby('request_type').sum().to_string())


    #fig_brt.show()

    return fig_brt



def plot_stacked_grouped_bar_chart(df, drill_down='rt',  request_type = 'scheduled'):
    color_scale = vu.get_colorway()
    fig = go.Figure()

    if drill_down == 'rt':
        # Loop over each request type
        for i, rt in enumerate(df['request_type'].unique()):
            fig.add_trace(
                go.Bar(
                    name=str(rt),
                    y=[str(a) for a in df['id_account_number'].unique()],  # y-axis will have accounts
                    x=df[df['request_type'] == rt]['total'],  # x-axis will have the values for the current cost type
                    orientation='h',
                    marker=dict(
                        color=color_scale[i],
                        line=dict(width=1, color='#405A73')
                    ),
                    # width=0.25
                )
            )
    elif drill_down == 'ct':
        cost_types = ['access', 'unique', 'refresh']
        if request_type == 'bval':
            cost_types = ['ACCESS', 'HIST', 'T2']
        # Loop over each cost type
        for i, ct in enumerate(cost_types):
            fig.add_trace(
                go.Bar(
                    name=ct,
                    x=df[df['request_type'] == request_type][ct],
                    y=[str(a) for a in df['id_account_number'].unique()],
                    # x-axis will have the values for the current cost type
                    orientation='h',
                    marker=dict(
                        color=color_scale[i],
                        line=dict(width=1, color='#405A73')
                    ),
                    # width=0.25
                )
            )

    fig.update_layout(
        dict(
            barmode='stack',
            plot_bgcolor='#102E44',
            paper_bgcolor='#102E44',

            font=dict(
                color='#88CACA',
                size=14
            ),
            margin=dict(l=0, r=0, t=0, b=30),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top", y=1.05,
                xanchor="left", x=1,
                borderwidth=0,
                font=dict(
                    size=14,
                    color='#88CACA'
                ),
            ),
            # xref='container'

            height=280,
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


    return fig

def get_mock_table_data(data_path, data_path_bval, drill_down='rt', request_type = 'scheduled'):

    session = ScopedSession()
    # TODO:
    #  1. Query DB to get the accounts for the Client
    #   2. Query BBG_INVOICE_MASTER you will need it to get the most recent invoce for a given month/account
    #  2. Query DB TO get all the invoices for the client --> Now you will have basically the csv
    #  3.
    #  4.

    #x = data_handler.query_db(session, BBG_INVOICE_DL)


    # load the csv files
    df_sa = pd.read_csv(data_path)
    df_bval = pd.read_csv(data_path_bval)

    # bval contains an additional request type with the following unique values:
    # ['Access', 'DAILY', 'HISTORY_MONTHLY', 'MONTHLY', 'WEEKLY'], hence we need to duplicate that column
    df_bval['request_type_bval'] = df_bval['request_type']
    df_bval['request_type'] = 'bval'

    df = pd.concat([df_sa, df_bval]).reset_index(drop=True).sort_values(['id_account_number'])

    return df








    # Billing by Request Type
    df_sa_rt = df_sa.groupby(['id_account_number', 'request_type', 'start_date', 'end_date']).sum().iloc[::-1].reset_index()
    df_bval_rt = df_bval.groupby(['id_account_number', 'start_date', 'end_date']).sum().iloc[::-1].reset_index()
    df_bval_rt['request_type'] = 'bval'
    df_rt = pd.concat([df_sa_rt, df_bval_rt]).reset_index(drop=True).sort_values(['id_account_number'])


    return df_rt


'''def get_mock_table_data(data_path, data_path_bval):
    df_sa = pd.read_csv(data_path)
    df = df_sa[['id_account_number', 'total']].groupby('id_account_number').sum().reset_index()

    # Dates for the last three months of 2022 and the first nine months of 2023
    dates = pd.date_range(start='2022-10-01', end='2023-09-01', freq='MS')
    mock_data = pd.DataFrame()

    # Generate mock data
    for acc in df_sa['id_account_number'].unique():
            new_row = {
                'id_account_number': acc,

                #'request_systems': random.randint(1, 8),
                'billed_amount': random.uniform(4252, 43000),
                #'total': row['total'] * random.uniform(0.8, 1.2), # vary the total by +/- 20%
                'trend': [random.choices(range(30, 125), [1/len(range(30, 125))]*len(range(30, 125)), k=12)],
                'link_account': 'mdi:bank'

            }
            mock_data = pd.concat([mock_data, pd.DataFrame(new_row, index= [len(mock_data)]), ])


    # Convert 'id_account_number' to int
    mock_data['id_account_number'] = mock_data['id_account_number'].astype(int)
    mock_data['billed_formatted'] = mock_data['billed_amount'].apply(
        lambda x: f"${x:.1f} ({x / mock_data['billed_amount'].sum()*100: .1f}%)")

    columnDefs = [
        {
            "field": "link_account",
            "headerName": '',
            'cellRendererSelector': {'function': 'getIcon(params)'},
            'maxWidth': 75
        },

        {
            "field": "id_account_number",
            "rowGroup": False,
            "maxWidth": 150,
            "headerName": 'Account',
        },

        {
            "field": 'billed_formatted',
            "headerName": "Billed (% Total)",
            "rowGroup": False,
            "maxWidth": 250,
        },



        {
            "field": "trend",
            "headerName": 'Trend',
            "cellRenderer": "agSparklineCellRenderer",
            "cellRendererParams" : dict(
                sparklineOptions= dict(
                    type= 'column',
                    fill= '#91cc75',
                    #stroke= '#91cc75',
                    highlightStyle= dict(
                        fill= 'orange'
                    ),
                    paddingInner= 0.1,
                    paddingOuter= 0.1,
                    padding=dict(
                      top=12
                    ),
                    label= dict(
                        enabled=False,
                        placement= 'outsideEnd'
                    ),
                    axis=dict(
                        stroke='#405A73',
                        strokeWidth=0
                    )
                )
            ),
        },
    ]

    getRowStyle = {
        "styleConditions": [
            {
                "condition": "params.data.id_account_number == ''",
                "style": {"fontWeight": 'bolder', "align": 'center'},
            }
        ]
    }

    grid = dag.AgGrid(
        id="custom-components-request_file_dirs_grid",
        className="ag-theme-alpine ag-theme-accordion",
        enableEnterpriseModules=True,
        licenseKey='test',
        columnDefs=columnDefs,
        rowData=df.to_dict("records"),
        columnSize="responsiveSizeToFit",
        dashGridOptions=dict(domLayout="autoHeight", rowSelection="multiple", suppressAggFuncInHeader=True,
                             showOpenedGroup=True, groupRemoveLowestSingleChildren=True, rowHeight=70,
                             pinnedBottomRowData=aggregate_dataframe(df).to_dict('records')),
        getRowStyle=getRowStyle,
        style={"height": 'auto'}
    )

    return grid'''


def aggregate_dataframe(df: pd.DataFrame):
    # Calculate the aggregated values
    aggregated_id_account_number = ''
    aggregated_billed_amount = df['billed_amount'].mean()
    total_billed_amount = df['billed_amount'].sum()
    aggregated_billed_formatted = f"${total_billed_amount:.1f} (100%)"

    # Calculate the average trend
    aggregated_trend = np.mean(df['trend'].tolist(), axis=0).tolist()

    # Create a new DataFrame with the aggregated values
    aggregated_df = pd.DataFrame({
        'id_account_number': [aggregated_id_account_number],
        'billed_amount': [aggregated_billed_amount],
        'trend': [aggregated_trend],
        'link_account': [None],
        'billed_formatted': [aggregated_billed_formatted]
    })

    return aggregated_df


if __name__ == '__main__':
    data_path = Path('dl_details.csv')
    data_path_bval = Path('bval_details.csv')
    get_mock_history(data_path, True)
    #get_mock_data(data_path, data_path_bval)

    #get_mock_data(data_path, data_path_bval, 'ct', request_type='bval')


'''
TODO:
        df = pd.read_csv(data_path)
        self.df = df.loc[df['id_account_number'] == 30314240]
        df_bval = pd.read_csv('data/mock_data/bval_details.csv')
        self.df_bval = df_bval.loc[df['id_account_number'] == 30314240]

 # Billing History
        fig_hist = md.get_mock_history(data_path)
        # Billing by Request Type
        fig_brt = md.get_mock_data(data_path, data_path_bval)
        # Billing by Cost Type NOTE: Request Type will need to be toggled!
        fig_ct = md.get_mock_data(data_path, data_path_bval, 'ct', request_type='bval')

        dbct_layout = dict(
            barmode='stack',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(
                color='#88CACA',
                size=16
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top", y=0,
                xanchor="auto",
                borderwidth=0,
                font=dict(
                    size=14,
                    color='#88CACA'
                ),
            ),
            height=100,
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                showline=False,
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                showline=False,
            )

        )

        df_asset_type = self.df.groupby(['request_type', 'asset_type_name']).sum()['total'].reset_index()
        df_asset_type_adhoc = \
            self.df.loc[df['request_type'] == 'adhoc'].groupby(['request_type', 'asset_type_name']).sum()[
                'total'].reset_index()
        df_asset_type_adhoc['total'] = df_asset_type_adhoc['total'] / df_asset_type_adhoc['total'].sum()
        df_asset_type_schedule = \
            self.df.loc[df['request_type'] == 'scheduled'].groupby(['request_type', 'asset_type_name']).sum()[
                'total'].reset_index()
        df_asset_type_schedule['total'] = df_asset_type_schedule['total'] / df_asset_type_schedule['total'].sum()
        df_asset_type = pd.concat([df_asset_type_adhoc, df_asset_type_schedule])

        df_asset_type_p = df_asset_type.pivot(index='request_type', columns='asset_type_name',
                                              values='total').reset_index().drop(0)

        df = df_asset_type_p
        # Identify columns to be considered for 'Others'
        cols = df.columns[1:]
        sorted_cols = df[cols].sum().sort_values(ascending=False)
        top_5_cols = sorted_cols.head(5).index.tolist()

        # Condition for minimum value
        min_value = 0.05 * df[cols].sum(axis=1).values[0]
        other_cols = [col for col in cols if col not in top_5_cols or df[col].values[0] < min_value]

        # Create 'Others' column
        df['Others'] = df[other_cols].sum(axis=1)

        # Drop the columns summed into 'Others'
        df = df.drop(columns=other_cols)

        rename_dict = {
            'CMO/ABS,ABS/CMO/CMBS/Whole Loan': 'CMO/ABS/CMBS/WL',
            'Corporate/Preferred/MoneyMarket': 'Corp/Pref/MM',
            'Options/Futures/FX/Warrants': 'Opt/Fut/FX/Warr',
            'Sovereign/Supranational/Agency': 'Sov/Supra/Agency'
        }
        df_asset_type_p = df.rename(columns=rename_dict)

        fig_bar_dbat = go.Figure(layout_xaxis_range=[0, df_asset_type_p.iloc[:, 1:].T.sum().iloc[0]])

        # Loop over each cost type
        for i, asset_type in enumerate(df_asset_type_p.columns[1:]):
            fig_bar_dbat.add_trace(
                go.Bar(
                    name=asset_type,
                    # y-axis will have request types
                    x=df_asset_type_p[asset_type],  # x-axis will have the values for the current cost type
                    orientation='h',
                    marker=dict(
                        color=self.color_scale[i],
                        line=dict(width=1, color='#405A73')
                    ),
                    # width=0.25,
                )
            )

        fig_bar_dbat.update_layout(
            dbct_layout
        )
        fig_bar_dbat.update_layout(
            dict(
                margin=dict(l=0, r=0, t=0, b=80),
                height=150)
        )

'''
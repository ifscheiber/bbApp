from typing import Union
import pandas as pd


def top_5_and_other(group, sort_by: Union[list[str], str]):
    group = group.sort_values(sort_by, ascending=False)
    if len(group) > 5:
        top_5 = group.head(5)
        other_sum = group.iloc[5:][sort_by].sum()
        other = pd.DataFrame(
            {'id_account_number': [group['id_account_number'].iloc[0]], 'data_category': ['Other'], sort_by: [other_sum]}
        )
        return pd.concat([top_5, other])
    return group



def get_color_scale():
    return [
        "#007BFF",  # Bright Blue
        "#FF6B6B",  # Coral
        "#FFC300",  # Yellow
        "#2ECC71",  # Green
        "#1E90FF",  # Dodger Blue
        "#FF4500",  # OrangeRed
        "#32CD32",  # LimeGreen
        "#C71585",  # Medium Violet Red
        "#FFD700",  # Gold
        "#8A2BE2",  # Blue Violet
    ]


def get_color_scale_damped():
    return [
        "#005BB5",  # Damped Bright Blue
        "#D9534F",  # Damped Coral
        "#DAA520",  # Damped Yellow
        "#228B22",  # Damped Green
        "#1C86EE",  # Damped Dodger Blue
        "#CD3700",  # Damped OrangeRed
        "#20B2AA",  # Damped LimeGreen (Changed to LightSeaGreen for better damping)
        "#993366",  # Damped Medium Violet Red
        "#B8860B",  # Damped Gold
        "#7B68EE",  # Damped Blue Violet (Slightly damped)
    ]


def get_colorway():
    return [
        "#7EB365",  # Variation of chart-green
        "#1A7A83",  # Variation of color-chart-12
        "#28445C",  # Variation of color-chart-1
        "#A4D085",  # Variation of chart-green
        "#149AA3",  # Variation of color-chart-12
        "#1E3A53",  # Variation of color-chart-1
        "#BDE3A5",  # Variation of chart-green
        "#0EA8C3",  # Variation of color-chart-12
        "#14304A",   # Variation of color-chart-1
        'red',
        'red',
        'red'
        'red',
        'red',
        'red'
    ]

def get_highlight_colorway():
    return [
        "#9ECB87",  # Highlight of Variation of chart-green
        "#3AB0D3",  # Highlight of Variation of color-chart-12
        "#3A5A73",  # Highlight of Variation of color-chart-1
        "#C6E8B7",  # Highlight of Variation of chart-green
        "#2C8C9E",  # Highlight of Variation of color-chart-12
        "#2E4A63",  # Highlight of Variation of color-chart-1
        "#DEF6C9",  # Highlight of Variation of chart-green
        "#4CC8E3",  # Highlight of Variation of color-chart-12
        "#2E4A63",   # Highlight of Variation of color-chart-1
        'red',
        'red',
        'red'
        'red',
        'red',
        'red'
    ]



[



    "#005BB5",  # Damped Bright Blue
    "#D9534F",  # Damped Coral
    "#BFA000",  # Damped Gold

    "#339CFF",  # Lighter Bright Blue
    "#FF8E8E",  # Lighter Coral
    "#FFE066",  # Lighter Gold

    "#6699CC",  # Desaturated Bright Blue
    "#FF9D9D",  # Desaturated Coral
    "#FFDE99",  # Desaturated Gold





    "#007BFF",  # Bright Blue
    "#FF6B6B",  # Coral
    "#FFD700",  # Gold
]



[
"#086788",  # Dark Teal Blue
"#05386B",  # Dark Royal Blue

"#5CDB95",  # Mint Green
"#07A0C3",  # Bright Teal Blue

"#379683",  # Dark Sea Green

"#F0C808",  # Sunflower Yellow

"#54B2A9",  # Medium Sea Green
"#5CDB95",  # Mint Green
"#B5EAD7",  # Light Mint Green


"#8EE4AF",  # Medium Mint Green
"#D8F3DC",  # Very Light Mint Green

"#05386B",  # Dark Royal Blue
"#5E92F3",  # Bright Royal Blue
"#B8D8D8"   # Light Grayish Cyan
]



[
    "#005BB5",  # Damped Bright Blue
    "#D9534F",  # Damped Coral
    "#BFA000",  # Damped Gold

    "#339CFF",  # Lighter Bright Blue
    "#FF8E8E",  # Lighter Coral
    "#FFE066",  # Lighter Gold

    "#6699CC",  # Desaturated Bright Blue
    "#FF9D9D",  # Desaturated Coral
    "#FFDE99",  # Desaturated Gold





    "#007BFF",  # Bright Blue
    "#FF6B6B",  # Coral
    "#FFD700",  # Gold
]
import streamlit as st

from components.data_loader import load_data
from components.thumbnail import thumbnail_renderer

from st_aggrid import AgGrid, GridOptionsBuilder


df = load_data()


filtered = df[
    df["SPOOL STATUS"]=="NO STATUS"
]


display_columns=[

"SN",
"AREA",
"ISO DWG NO.",
"LINE NO.",
"SPOOL NO.",
"PIPE RACK NO.",
"INSPECTION PHOTO"

]


table_df=filtered[display_columns]


gb = GridOptionsBuilder.from_dataframe(table_df)


gb.configure_column(
    "INSPECTION PHOTO",
    cellRenderer=thumbnail_renderer
)


gb.configure_default_column(
    resizable=True,
    sortable=True
)


grid_options=gb.build()


AgGrid(
    table_df,
    gridOptions=grid_options,
    height=600
)
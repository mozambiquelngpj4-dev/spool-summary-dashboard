
import streamlit as st
import pandas as pd
import gspread
import plotly.express as px
from io import BytesIO
from st_aggrid import AgGrid, GridOptionsBuilder



# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="SPOOL DWG SUMMARY",
    page_icon="📋",
    layout="wide"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background-image:
        linear-gradient(
            rgba(244,247,250,0.55),
            rgba(244,247,250,0.55)
        ),
        url("https://edmontonvalve.swagelok.com/hubfs/Facility%20Photo%20for%20COVID%20Blog.jpg#keepProtocol");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}


.title{
    font-size:45px;
    font-weight:700;
    color:#0B3B6F;
}


.subtitle{
    color:#191c1c;
    margin-bottom:20px;
}


.card{
    background: rgba(255,255,255,0.25);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);

    border: 1px solid rgba(255,255,255,0.35);

    padding:20px;
    border-radius:18px;

    box-shadow:
        0 8px 32px rgba(0,0,0,0.15);

    text-align:center;

    transition: all 0.3s ease;
}


.card:hover{

    transform: translateY(-5px);

    background:
        rgba(255,255,255,0.35);

    box-shadow:
        0 12px 40px rgba(0,0,0,0.25);

}


.card h2{

    margin:0;

    font-size:36px;

    font-weight:700;

    color:#0B3B6F;

}


.card p{

    margin-top:8px;

    font-size:15px;

    color:#444;

}

</style>
""", unsafe_allow_html=True)



# ==========================================
# LOAD GOOGLE SHEET
# ==========================================


@st.cache_data(ttl=60)
def load_data():

    gc = gspread.service_account_from_dict(
     st.secrets["gcp_service_account"]
    )


    sheet = gc.open_by_url(
        "https://docs.google.com/spreadsheets/d/1HoCTs7R4SkVP5IgW3lLBCkiI6HhtIG5zxJtY8KXJksc/edit"
    )


    worksheet = sheet.worksheet("DATA")


    data = worksheet.get_all_records()


    columns = [
        "SN",
        "AREA",
        "ISO DWG NO.",
        "LINE NO.",
        "SHEET NO.",
        "REV. NO.",
        "SPOOL NO.",
        "SPOOL STATUS",
        "PIPE RACK NO.",
        "FABRICATED SPOOL",
        "RECEIVED DATE",
        "INSPECTOR",
        "INSPECTION DATE",
        "INSPECTION PHOTO",
        "DELIVERY DATE",
        "INSTALL DATE",
        "INSTALL PHOTO",
        "REMARKS",
        "RELATED IMAGES",
        
    ]


    # ===============================
    # EMPTY SHEET PROTECTION
    # ===============================

    if not data:

        return pd.DataFrame(columns=columns)


    df = pd.DataFrame(data)


    # make sure missing columns do not crash

    for col in columns:

        if col not in df.columns:

            df[col] = ""


    return df[columns]


# ==========================================
# LOAD DATA
# ==========================================

df = load_data()

if df.empty:

    st.warning("⚠️ ***No spool data available.***")


# ==========================================
# HEADER
# ==========================================


st.markdown("""
<div class='title'>
📋 PIPING SPOOL SUMMARY PORTAL
</div>

<div class='subtitle'>
Mozambique LNG PJ • Fabrication Tracking System
</div>

""", unsafe_allow_html=True)



# ==========================================
# ACTION BUTTONS
# ==========================================


action1, action2 = st.columns(2)


with action1:

    if st.button(
        "🔄 ***REFRESH DATA***",
        use_container_width=True
    ):

        st.cache_data.clear()
        st.rerun()



with action2:

    sync_clicked = st.button(
        "☁️ ***Sync Firebase (Beta)***",
        use_container_width=True
    )



# ==========================================
# TABS
# ==========================================


tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "📊 ***DASHBOARD***",
        "📄 ***SPOOL LIST***",
        "⚠️ ***NO STATUS***",
        "🛠️ ***FABRICATED SPOOL***",
        "🔎 ***SPOOL INSPECTION***",
        "🚚 ***DELIVERED TO SITE***",
        "🪛 ***INSTALL TO SITE***"
    ]
)



# ==========================================
# TAB 1 - DASHBOARD
# ==========================================


with tab1:


    total = len(df)


    fabricated = len(
        df[df["SPOOL STATUS"]=="FABRICATED SPOOL"]
    )


    inspection = len(
        df[df["SPOOL STATUS"]=="SPOOL INSPECTION"]
    )


    no_status = len(
        df[df["SPOOL STATUS"]=="NO STATUS"]
    )


    delivered = len(
        df[df["SPOOL STATUS"]=="DELIVERED TO SITE"]
    )


    installed = len(
        df[df["SPOOL STATUS"]=="INSTALL ON SITE"]
    )


    completed = (
        fabricated
        + inspection
        + delivered
        + installed
    )


    progress = (
        completed / total
        if total > 0
        else 0
    )



    c1,c2,c3,c4,c5,c6 = st.columns(6)



    with c1:

        st.markdown(f"""
        <div class='card'>
        <h2>{total}</h2>
        <p>OVER-ALL SPOOL</p>
        </div>
        """,
        unsafe_allow_html=True)



    with c2:

        st.markdown(f"""
        <div class='card'>
        <h2>{fabricated}</h2>
        <p>FABRICATED</p>
        </div>
        """,
        unsafe_allow_html=True)



    with c3:

        st.markdown(f"""
        <div class='card'>
        <h2>{inspection}</h2>
        <p>INSPECTION</p>
        </div>
        """,
        unsafe_allow_html=True)
        
    with c4:

        st.markdown(f"""
        <div class='card'>
        <h2>{no_status}</h2>
        <p>NO STATUS</p>
        </div>
        """,
        unsafe_allow_html=True)



    with c5:

        st.markdown(f"""
        <div class='card'>
        <h2>{delivered}</h2>
        <p>SITE DELIVERED</p>
        </div>
        """,
        unsafe_allow_html=True)



    with c6:

        st.markdown(f"""
        <div class='card'>
        <h2>{installed}</h2>
        <p>INSTALL ON SITE</p>
        </div>
        """,
        unsafe_allow_html=True)



    # ==========================================
    # COMPLETION PROGRESS
    # ==========================================


    st.write("")


    st.subheader("📈 ***SPOOL COMPLETION PROGRESS***")


    # ============================================
    # SPOOL COMPLETION CALCULATION
    # ============================================

    total_spools = len(df)


    installed_spools = len(
        df[
            df["SPOOL STATUS"]
            .astype(str)
            .str.upper()
            .str.strip()
            ==
            "INSTALLED ON SITE"
        ]
    )


    if total_spools > 0:

        progress = installed_spools / total_spools

    else:

        progress = 0



    # ============================================
    # DISPLAY PROGRESS
    # ============================================

    st.progress(progress)


    st.write(

        f"{installed_spools} of {total_spools} spools installed on site "
        f"({int(progress*100)}%)"

    )
    
    # ==========================================
    # STATUS DISTRIBUTION CHART
    # ==========================================

    st.subheader("📊 ***SPOOL STATUS DISTRIBUTION***")


    if df.empty:

        st.info("No data available for chart.")

    else:

        status_count = (
            df["SPOOL STATUS"]
            .value_counts()
            .reset_index()
        )


        status_count.columns = [
            "STATUS",
            "COUNT"
        ]


        fig = px.bar(
            status_count,
            x="STATUS",
            y="COUNT",
            text="COUNT",
            title="Spool Status Overview"
        )


        fig.update_layout(

            xaxis_title="",
            yaxis_title="Number of Spools",

            height=400,

            # Glass effect
            paper_bgcolor="rgba(255,255,255,0.25)",
            plot_bgcolor="rgba(255,255,255,0.10)",

            font=dict(
                color="#0B3B6F",
                size=13
        ),

        title=dict(
            font=dict(
                size=20,
                color="#0B3B6F"
            ),
            x=0.02
        ),


        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.3)",
            zeroline=False
        ),


        margin=dict(
            l=40,
            r=40,
            t=60,
            b=40
        )

)


        st.markdown(
        """
        <style>

        [data-testid="stPlotlyChart"]{
            background:rgba(255,255,255,0.25);
            backdrop-filter:blur(12px);
            -webkit-backdrop-filter:blur(12px);

            border-radius:18px;
            padding:10px;

            border:1px solid rgba(255,255,255,0.35);

            box-shadow:
            0 8px 32px rgba(0,0,0,0.15);
        }

        </style>
        """,
        unsafe_allow_html=True
        )


        st.plotly_chart(
        fig,
            use_container_width=True
        )

# ==========================================
# TAB 2 - SPOOL SUMMARY TABLE
# ==========================================


with tab2:


    st.markdown(
        "## 🔍 Search & Filter"
    )


    search_col, area_col, status_col = st.columns(
        [4,2,2]
    )



    # Search

    search = search_col.text_input(
        "Search",
        placeholder="SN, ISO DWG NO., LINE NO..."
    )



    # AREA FILTER

    areas = [
        "All"
    ] + sorted(
        df["AREA"]
        .dropna()
        .unique()
        .tolist()
    )


    selected_area = area_col.selectbox(
        "AREA",
        areas
    )



    # STATUS FILTER

    statuses = [
        "All"
    ] + sorted(
        df["SPOOL STATUS"]
        .dropna()
        .unique()
        .tolist()
    )


    selected_status = status_col.selectbox(
        "STATUS",
        statuses
    )



    # ==========================================
    # APPLY FILTER
    # ==========================================


    filtered_df = df.copy()



    if search:


        keyword = search.lower()


        filtered_df = filtered_df[
            filtered_df.apply(
                lambda row:

                keyword in str(row["SN"]).lower()

                or

                keyword in str(row["ISO DWG NO."]).lower()

                or

                keyword in str(row["LINE NO."]).lower(),

                axis=1
            )
        ]



    if selected_area != "All":


        filtered_df = filtered_df[
            filtered_df["AREA"] == selected_area
        ]



    if selected_status != "All":


        filtered_df = filtered_df[
            filtered_df["SPOOL STATUS"] == selected_status
        ]



    st.caption(
        f"Showing {len(filtered_df)} of {len(df)} spools"
    )



    
    # ==========================================
    # EXPORT EXCEL
    # ==========================================

    buffer = BytesIO()

    with pd.ExcelWriter(
    buffer,
    engine="openpyxl"
)   as writer:

        filtered_df.to_excel(
            writer,
            index=False,
            sheet_name="Spool Summary"
        )  

    buffer.seek(0)

    # ==========================================
    # TABLE PREVIEW
    # ==========================================

    if "show_table" not in st.session_state:
        st.session_state.show_table = False

    preview_col, export_col = st.columns(2)

    with preview_col:

        if st.button(
            "👀 Show / Hide Table",
            use_container_width=True
        ):

            st.session_state.show_table = not st.session_state.get(
            "show_table",
            False
            )

    with export_col:

        st.download_button(
        "📥 Export Current Table",
        data=buffer,
        file_name="spool_summary.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        width="stretch"
    )

    # Show table only after clicking Preview
    if st.session_state.show_table:

        # ==========================================
        # FREEZE HEADER + FREEZE FIRST COLUMNS
        # ==========================================

        gb = GridOptionsBuilder.from_dataframe(filtered_df)


        gb.configure_default_column(
            resizable=True,
            sortable=True,
            filter=True
        )


        # Freeze SN to LINE NO.

        for col in [
            "SN",
            "AREA",
            "ISO DWG NO.",
            "LINE NO."
        ]:

            gb.configure_column(
                col,
                pinned="left"
            )


        gb.configure_grid_options(
            domLayout="normal"
        )


        grid_options = gb.build()



        AgGrid(
            filtered_df,
            gridOptions=grid_options,
            height=600,
            width="100%",
            theme="streamlit",
            fit_columns_on_grid_load=False
        )
        
# ==========================================
# STATUS TAB FILTER FUNCTION
# ==========================================

def status_filter_table(dataframe, status_value, title, display_columns=None):

    st.markdown(f"## {title}")
    

    filtered = dataframe[
        dataframe["SPOOL STATUS"] == status_value
    ].copy()


    # -------------------------------
    # SEARCH FILTERS
    # -------------------------------

    search_col, area_col, line_col, dwg_col = st.columns(
        [3,2,2,2]
    )


    search = search_col.text_input(
        "Search",
        key=f"{status_value}_search",
        placeholder="Search..."
    )


    areas = [
        "All"
    ] + sorted(
        filtered["AREA"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    selected_area = area_col.selectbox(
        "AREA",
        areas,
        key=f"{status_value}_area"
    )



    lines = [
        "All"
    ] + sorted(
        filtered["LINE NO."]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    selected_line = line_col.selectbox(
        "LINE NO.",
        lines,
        key=f"{status_value}_line"
    )



    dwgs = [
        "All"
    ] + sorted(
        filtered["ISO DWG NO."]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    selected_dwg = dwg_col.selectbox(
        "ISO DWG NO.",
        dwgs,
        key=f"{status_value}_dwg"
    )



    # -------------------------------
    # APPLY FILTERS
    # -------------------------------

    if search:

        keyword = search.lower()

        filtered = filtered[
            filtered.astype(str)
            .apply(
                lambda row:
                row.str.lower()
                .str.contains(keyword)
                .any(),
                axis=1
            )
        ]



    if selected_area != "All":

        filtered = filtered[
            filtered["AREA"].astype(str) == selected_area
        ]



    if selected_line != "***All***":

        filtered = filtered[
            filtered["LINE NO."].astype(str) == selected_line
        ]



    if selected_dwg != "All":

        filtered = filtered[
            filtered["ISO DWG NO."].astype(str) == selected_dwg
        ]



    st.caption(
        f"Showing {len(filtered)} spools"
    )


    if filtered.empty:

        st.info("No matching spools found.")

    else:

        # ==========================================
        # FREEZE HEADER + FREEZE FIRST COLUMNS
        # ==========================================

        # ==========================================
        # PREPARE TABLE DISPLAY
        # ==========================================

        if display_columns:

            available_columns = [
                col for col in display_columns
                if col in filtered.columns
            ]

            table_df = filtered[available_columns]

        else:

            table_df = filtered


        gb = GridOptionsBuilder.from_dataframe(table_df)


        gb.configure_default_column(
            resizable=True,
            sortable=True,
            filter=True
        )


        # Freeze SN to LINE NO.

        for col in [
            "SN",
            "AREA",
            "ISO DWG NO.",
            "LINE NO."
        ]:

            if col in table_df.columns:

                gb.configure_column(
                    col,
                    pinned="left"
                )


        # Enable scrolling

        gb.configure_grid_options(
            domLayout="normal"
        )


        grid_options = gb.build()


        AgGrid(
        table_df,
            gridOptions=grid_options,
            height=600,
            width="100%",
            theme="streamlit",
            fit_columns_on_grid_load=False
        )
        
        
# ==========================================
# TAB 3 - NO STATUS
# ==========================================

with tab3:

    display_columns = [
        "SN",
        "AREA",
        "ISO DWG NO.",
        "LINE NO.",
        "SHEET NO.",
        "REV. NO.",
        "SPOOL NO.",
        "SPOOL STATUS",
        "PIPE RACK NO.",
        "REMARKS",
    ]


    status_filter_table(
        df,
        "NO STATUS",
        "⚠️ Spools Without Status",
        display_columns
    )


# ==========================================
# TAB 4 - FABRICATED
# ==========================================

with tab4:
    
    display_columns = [
        "SN",
        "AREA",
        "ISO DWG NO.",
        "LINE NO.",
        "SHEET NO.",
        "REV. NO.",
        "SPOOL NO.",
        "SPOOL STATUS",
        "PIPE RACK NO.",
        "FABRICATED SPOOL",
        "RECEIVED DATE",
        "REMARKS",
    ]

    status_filter_table(
        df,
        "FABRICATED SPOOL",
        "🛠️ Fabricated Spool",
        display_columns
    )



# ==========================================
# TAB 5 - INSPECTION
# ==========================================

with tab5:
    
    display_columns = [
        "SN",
        "AREA",
        "ISO DWG NO.",
        "LINE NO.",
        "SHEET NO.",
        "REV. NO.",
        "SPOOL NO.",
        "SPOOL STATUS",
        "PIPE RACK NO.",
        "INSPECTOR",
        "INSPECTION DATE",
        "INSPECTION PHOTO",
        "REMARKS",
    ]

    status_filter_table(
        df,
        "***SPOOL INSPECTION***",
        "🔎 ***Spool Inspection***",
        display_columns
    )



# ==========================================
# TAB 6 - DELIVERED
# ==========================================

with tab6:
    
    display_columns = [
        "SN",
        "AREA",
        "ISO DWG NO.",
        "LINE NO.",
        "SHEET NO.",
        "REV. NO.",
        "SPOOL NO.",
        "SPOOL STATUS",
        "PIPE RACK NO.",
        "DELIVERY DATE",
        "REMARKS",
    ]

    status_filter_table(
        df,
        "***DELIVERED TO SITE***",
        "🚚 ***Delivered to Site***",
         display_columns
    )



# ==========================================
# TAB 7 - INSTALL
# ==========================================

with tab7:

    display_columns = [
        "SN",
        "AREA",
        "ISO DWG NO.",
        "LINE NO.",
        "SHEET NO.",
        "REV. NO.",
        "SPOOL NO.",
        "SPOOL STATUS",
        "PIPE RACK NO.",
        "INSTALL DATE",
        "INSTALL PHOTO",
        "REMARKS",
    ]
    status_filter_table(
        df,
        "***INSTALL ON SITE***",
        "🪛 ***Install on Site***",
        display_columns
    )
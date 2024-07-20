import streamlit as st
from backend import db_io
from util import util
import pandas as pd
import plotly.express as px 


st.set_page_config(page_title="Expense Analysis", page_icon="🧞")

current_user = db_io.created_by_current

if 'extraction_sql_raw' not in st.session_state:
    st.session_state.extraction_sql_raw = None
if 'image_sql_raw' not in st.session_state:
    st.session_state.image_sql_raw = None
if 'image_ids_relevant' not in st.session_state:
    st.session_state.image_ids_relevant = None
if 'extraction_id_relevant' not in st.session_state:
    st.session_state.extraction_id_relevant = None
if 'render_df_list_for_extraction' not in st.session_state:
    st.session_state.render_df_list_for_extraction = None
if 'data_editor_list' not in st.session_state:
    st.session_state.data_editor_list = None



if st.session_state.extraction_sql_raw is None:
    st.session_state.extraction_sql_raw = db_io.select_extraction(db_io.created_by_current)
    st.session_state.image_ids_relevant = util.get_image_id(st.session_state.extraction_sql_raw)
    st.session_state.image_sql_raw = db_io.select_image(st.session_state.image_ids_relevant)
    st.session_state.extraction_id_relevant = util.get_extraction_id(st.session_state.extraction_sql_raw)

    st.session_state.render_df_list_for_extraction = util.process_extraction_details(st.session_state.extraction_sql_raw)
    st.session_state.data_editor_list = [None] * len(st.session_state.image_sql_raw)
# st.write(st.session_state.extraction_sql_raw)
# st.write(st.session_state.image_ids_relevant)
# st.write(st.session_state.image_sql_raw)
# st.write(st.session_state.extraction_id_relevant)
st.write(
    """#### Reload Your Expenses to Get The Most Updated Snapshot!"""
)
re_run = st.button("Reload Expense")

if re_run == True:
    st.rerun()



if st.session_state.render_df_list_for_extraction:
    st.write(
        """#### Your Expense Trend:"""
    )
    _render_df = util.merge_df(st.session_state.render_df_list_for_extraction)
    _group_by = (_render_df.groupby('Date of Spending').sum().reset_index()[['Date of Spending','Dollar Amount']])
    _group_by['Dollar Amount'] = _group_by['Dollar Amount'].astype('float')

    st.line_chart(_group_by, x="Date of Spending", y="Dollar Amount")

    st.write(
        """#### Your Expense Overview:"""
    )   
    # _render_df = util.merge_df(st.session_state.render_df_list_for_extraction)
    fig = px.pie(_render_df, values='Dollar Amount', names='Spending Category')
            # title=f'Proportion of Spending',
            # height=300, width=200)
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
    st.plotly_chart(fig, use_container_width=True)


st.write(
    """#### Your Expenses Extraction Details, Edit and Save as you see fit:"""
)

for i in range(0, len(st.session_state.image_sql_raw)):
    col1, col2 = st.columns([1, 2])

    with col1:
        st.write(f"##### Original Image #{i+1}")
        st.image(st.session_state.image_sql_raw[i][1])

    with col2:
        st.write(f"##### Extracted Details #{i+1}")
        temp_df =   st.data_editor(st.session_state.render_df_list_for_extraction[i]
                       , key=f"data_editor_{st.session_state.extraction_sql_raw[i][0]}"
                       , hide_index=True)
        st.session_state.data_editor_list[i] = temp_df
        if st.button("Save", key=f"save_extraction_{st.session_state.extraction_sql_raw[i][0]}"):
            
            extraction_id = st.session_state.extraction_sql_raw[i][0]
            df = st.session_state.data_editor_list[i]

            print (df)

            result = df.apply(

                    lambda row : db_io.update_extraction(
                        extraction_id,
                        row['Date of Spending'],
                        row['Location of Spending'],
                        row['Spending Venue'],
                        row['Dollar Amount'],
                        row['Spending Category'],
                        current_user
                    ), axis = 1

            )
            print(f"Saved for {st.session_state.extraction_sql_raw[i][0]}")
            st.session_state.extraction_sql_raw = db_io.select_extraction(db_io.created_by_current)
            st.session_state.render_df_list_for_extraction = util.process_extraction_details(st.session_state.extraction_sql_raw)
            st.rerun()
                #   , Result: {result}")

import streamlit as st
import time
from backend import gemini, agent_for_category, db_io
from util import util
import google
import pandas as pd
import datetime



# def clear_variables():
#     # Clear variables here
#     uploaded_files = None
#     output_list = None

# st.set_page_config(
#     on_page_exit=clear_variables
# )
st.set_page_config(page_title="Expense Upload", page_icon="🤓")

st.markdown("# Upload Status 🚧")
st.sidebar.header("Multiple File Uploader")

if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

st.session_state.uploaded_file = st.sidebar.file_uploader("Select files from your device!", type=["jpg", "png"], 
                                          accept_multiple_files=True)
# output_list = []

run = st.sidebar.button("Run Analysis")
# df_t_list = []
# file_name = []
if run:

    for file in st.session_state.uploaded_file:
        print(file)
        ## Per Image File
        image_file = dict.fromkeys(
        ['image_data',
            'image_name',
            'file_type',
            'upload_date',
            'image_size',
            'content_type',
            'checksum',
            'created_by'])
        ## Per Extraction
        extraction_file = dict.fromkeys(
            ['image_id',
            'date_of_spending',
            'location_of_spending',
            'spending_company',
            'dollar_spent',
            'item_or_service_bought',
            'category',
            'extraction_method',
            'extraction_status',
            'created_by']
        )

        


        image_file['image_data'] = file.getvalue()
        image_file['image_name'] = file.name
        image_file['file_type'] = file.type
        image_file['upload_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        image_file['image_size'] = file.size
        image_file['content_type'] = file.type
        image_file['checksum'] = 'None'
        image_file['created_by'] = db_io.created_by_current

        print(image_file)

        st.write(f"Processing {image_file['image_name']}")
        progress_bar = st.progress(0)
        image_id = db_io.insert_image(
            image_file['image_data'],
            image_file['image_name'],
            image_file['file_type'],
            image_file['upload_date'],
            image_file['image_size'],
            image_file['content_type'],
            image_file['created_by']
        )

        progress_bar.progress(25)

        st.write(f"Extracting Details From {image_file['image_name']}")
        try:
            output_raw = gemini.generate(
                image_data= image_file['image_data'],
                file_type= image_file['file_type']
            )
        except google.api_core.exceptions.ResourceExhausted:
            print("Triggering retry......")
            ##retry after a minute
            time.sleep(60)
            output_raw = gemini.generate(
                image_data=  image_file['image_data'],
                file_type= image_file['file_type']
        )
        output_string = (output_raw.candidates[0].content.parts[0].text)
        dict_output = (gemini.parse_markdown_json(output_string))
        
        progress_bar.progress(50)

        st.write(f"Determining Spending Category of {image_file['image_name']}")

        dict_category = agent_for_category.get_category_with_agent(dict_output['location_of_spending'],
                                                                        dict_output['spending_company'],
                                                                        dict_output['items_or_service_bought'])
            
        dict_output['category'] = dict_category['category']

        print(dict_output)

        progress_bar.progress(75)

        st.write(f"Saving Extraction Details From {image_file['image_name']}")

        temp_df = util.consolidate_list_into_df([dict_output])
        
        result = temp_df.apply(lambda row:
            db_io.insert_extraction(
                image_id,
                row['date_of_spending'].strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(row['date_of_spending']) else None,
                row['location_of_spending'],
                row['spending_company'],
                row['dollar_spent_FLOAT'],
                row['items_or_service_bought'],
                row['category'],
                'Gemini Flash',
                'Completed',
                db_io.created_by_current
            ), axis = 1
        )

        st.write(f"{image_file['image_name']} Completed!")

        progress_bar.progress(100)

    st.write("All Images Processed, check the results in your Personal Dashboard!")

    # # Create a temporary directory
    # with tempfile.TemporaryDirectory() as tmp_dir:
    #     # Save each uploaded file to the temporary directory
    #     file_paths = []
    #     for file in uploaded_files:
    #         file_path = os.path.join(tmp_dir, file.name)
    #         with open(file_path, 'wb') as f:
    #             f.write(file.getvalue())
    #         file_name.append(file.name)
    #         file_paths.append(file_path)
    #     # Print the file paths
    #     ##st.write("Files saved to:")
    #     for path in file_paths:
    #         file_path_dict['path'].append(path)
    #         file_type = path.split('.')[-1].lower()
    #         file_path_dict['type'].append(file_type)

    #     for i in range(0, len(file_path_dict['path'])):

    #         cols = st.columns(2)
    #         cols[0].header("Original Image")
    #         cols[1].header("Extracted Details")



    #         if file_path_dict['type'][i] == 'jpg':
    #             file_path_dict['type'][i] = 'jpeg' ##Gemini Doesn't Like Jpg
    #         print(file_path_dict['path'][i])
    #         print(file_path_dict['type'][i])
    #         st.write(f'Processing image: {file_name[i]}')
    #         progress_bar = st.progress(0)
    #         try:
    #             output_raw = gemini.generate(

    #                 file_path= file_path_dict['path'][i],
    #                 file_type= file_path_dict['type'][i]
    #             )
    #         except google.api_core.exceptions.ResourceExhausted:
    #             print("Triggering retry......")
    #             ##retry after a minute
    #             time.sleep(60)
    #             output_raw = gemini.generate(

    #                 file_path= file_path_dict['path'][i],
    #                 file_type= file_path_dict['type'][i]
    #             )
                
    #         output_string = (output_raw.candidates[0].content.parts[0].text)
    #         print(output_string)
    #         # Simulate a long-running task
    #         progress_bar.progress(50)
    #         st.write(f'Finised image: {file_name[i]}')
    #         dict_output = (gemini.parse_markdown_json(output_string))

    #         progress_bar.progress(75)
    #         dict_category = agent_for_category.get_category_with_agent(dict_output['location_of_spending'],
    #                                                                     dict_output['spending_company'],
    #                                                                     dict_output['items_or_service_bought'])
            
    #         dict_output['category'] = dict_category['category']
            
    #         output_list.append(dict_output)

    #         progress_bar.progress(100)

    #         display_columns = ['date_of_spending', 'location_of_spending', 'spending_company', 'dollar_spent', 'category']

    #         cols[0].image(file_path_dict['path'][i], width = 300)
    #         cols[1].dataframe(util.consolidate_list_into_df([output_list[i]])[display_columns].T)

    #     st.write('Your Expenses Are as Follows:')
    #     df_1 = util.consolidate_list_into_df(output_list)
    #     st.write(df_1[display_columns])
    #     st.line_chart(df_1, x="date_of_spending", y="dollar_spent_FLOAT", color="category")

    #     fig = px.pie(df_1, values='dollar_spent_FLOAT', names='category',
    #              title=f'Proportion of Spending',
    #              height=300, width=200)
    #     fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
    #     st.plotly_chart(fig, use_container_width=True)
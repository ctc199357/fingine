import pandas as pd
import re

def consolidate_list_into_df(list_dict):

    consolidated_data = {}

    for d in list_dict:
        for k, v in d.items():
            if k not in consolidated_data:
                consolidated_data[k] = [v]
            else:
                consolidated_data[k].append(v)

    df = pd.DataFrame(consolidated_data)
    df['dollar_spent_FLOAT'] = df['dollar_spent'].apply(lambda x:standardize_dollar_string(x))
    df['date_of_spending'] = df['date_of_spending'].apply(lambda x:standardize_datetime(x))

    print(df)
    return df

def merge_df(list_df):
   
    df = list_df[0]

    for i in range(1, len(list_df)):
        df = pd.concat([df, list_df[i]])


    return df   





def standardize_dollar_string(s):
    s = s.replace('$', '').replace(',', '')  # remove $ and ,
    match = re.search(r'(\d+)', s)
    if match:
        num = float(match.group(0))
    print(num)
    return num

def standardize_datetime(date_str, input_formats=None):
  """
  Standardizes a string into a datetime object.

  Args:
    date_str: The string representing the date.
    input_formats: A list of possible date formats. If None, a default list of formats is used.

  Returns:
    A datetime object representing the date, or None if the string cannot be parsed.
  """

  # Define default input formats
  if input_formats is None:
    input_formats = [
        '%Y/%m/%d',  # 2024/05/06
        '%d/%m/%Y',  # 25/12/2009
        '%Y年%m月',  # 2011年3月
        '%d %B, %Y'  # 2011年3月
    ]

  for fmt in input_formats:
    try:
      dt = pd.to_datetime(date_str, format=fmt)
      return dt
    except ValueError:
      pass

  return None


def get_image_id(list_extraction):
    
    ids = []
    
    for i in list_extraction:
        ids.append(i[1])

    return ids


def get_extraction_id(list_extraction):
    
    ids = []
    
    for i in list_extraction:
        ids.append(i[0])

    return ids


def process_extraction_details(list_of_tuple):
   
    df_list = []

    for i in list_of_tuple:
        df_skeleton = {
        "Date of Spending":[],
        "Location of Spending":[],
        "Spending Venue":[],
        "Dollar Amount":[],
        "Spending Category":[]
        }

        df_skeleton['Date of Spending'].append(i[2])
        df_skeleton['Location of Spending'].append(i[3])
        df_skeleton['Spending Venue'].append(i[4])
        df_skeleton['Dollar Amount'].append(i[5])
        df_skeleton['Spending Category'].append(i[6])

        print(df_skeleton)

        df = pd.DataFrame(df_skeleton)
        df.index.name = 'Extracted Field'

        df_list.append(df)
    
    return df_list
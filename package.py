import numpy as np 
import json 

# structure of dictionary:
"""
{index
    { index: attribue_name
    
    }
}

"""
def load_attr_dict(json_file):

    f = open(json_file)
    raw_dict = json.load(f)

    res_dict = dict()

    for str_index, column_dict in raw_dict.items():
        col_index = int(str_index)
        res_dict[col_index] = dict()
        for inner_str_index, attr_name in column_dict.items():
            res_dict[col_index][int(inner_str_index)] = attr_name

    return res_dict

def convert_row_into_text_form(dict, row):
    res_list = []
    for i in range(len(row)):
        item_idx = row[i]
        if dict.get(i) != None:
            res_list.append(dict[i][int(item_idx)])
        else:
            res_list.append(item_idx)
    return res_list 




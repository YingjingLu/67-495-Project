import numpy as np
import json
import csv
def directly_save_one_batch(csv_path, save_path, module_name):
    print("Here in process batch")
    file = np.load(batch)
    file_save_path = save_path + "/" + module_name + ".npy"

    try:
        np.save(file_save_path, file)
        return file_save_path
    except:
        print("Path invalid: ", file_save_path)
        return None

# structure of dictionary:
"""
{index
    { attr_name: index
    
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
        for attr_name, inner_str_index in column_dict.items():
            res_dict[col_index][attr_name] = int(inner_str_index)

    return res_dict

def convert_row_into_text_form(dict_, row):
    res_list = []
    for i in range(len(row)):
        item_idx = row[i]
        if dict_.get(i) != None:
            res_list.append(dict_[i][item_idx])
        else:
            res_list.append(item_idx)
    return res_list 



def csv_to_array(csv_path, column_dict):
    f = open(csv_path)
    output = []
    csv_reader = csv.reader(f)
    for row in csv_reader:
        output.append(convert_row_into_text_form(column_dict, row))
    return np.array(output, dtype = np.float32)

def handle_import(csv_path, column_dict_path):
    column_dict = load_attr_dict(column_dict_path)
    array = csv_to_array(csv_path, column_dict)[:,:-2]
    return array


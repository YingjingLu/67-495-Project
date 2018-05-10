from django import forms

class ModuleForm(forms.Form):

    module_name = forms.CharField(label='Module Name', max_length = 100)
    new_record_period = forms.CharField(label = 'Record Period',max_length = 100)
    description = forms.CharField(label = 'Description', max_length = 255)
    access_level = forms.CharField(label = 'Access Level', max_length = 100)
    quality_data_indexing_dict_path = forms.CharField(label="Indexing Dictionary Path", max_length = 255, initial='C:\\Users\StevenLu\Desktop\IS_CPP\server\server\data_batch\\all_dict.json')
    data_storage_path = forms.CharField(label = 'Storage Path', max_length = 255, initial='C:\\Users\StevenLu\Desktop\IS_CPP\server\server\data_batch\\')
    csv_file_path = forms.CharField(label='CSV Path Local', max_length = 255)
    

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

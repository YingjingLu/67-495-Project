from django.shortcuts import render
from .models import *
from module.utils.matrix_loader import *
from django.http import HttpResponseRedirect
from .forms import *
from .OS_ELM_GLOBAL import *
from datetime import *
from django.urls import reverse
from module.utils.process_batch import *
import numpy as np 
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Create your views here.
def index(request):
    all_module = Module.objects.all()
    d = {'all_module': all_module}
    return render(request, "module/index.html", d)

def batches(request):
    return None

def view_module(request, pk, start, delta):
    module = Module.objects.get(pk=pk)
    data_storage_path = module.data_storage_path
    batch = np.load(data_storage_path)
    print("batch shape", batch.shape)
    num_data = batch.shape[0]

    print("pk", pk)
    print("batch", batch)
    print("delta", delta)
    start = int(start)
    end = start + 1
    if int(delta) == 1:
        end_index = start *100 + 100
        if end_index < num_data:
            start += 1
            end = start + 1
    elif int(delta) == 2:
        if start > 0:
            start -= 1
            end = start + 1

    start_index = start * 100
    end_index = end*100
    print((start, end))

    batch_data = batch[start_index:end_index]
    print("batch_data size", batch_data.shape)
    intrusion = predict(batch_data)
    print("intrusion", intrusion)
    att = []
    for i in range(len(intrusion)):
        if intrusion[i] == 0:
            att.append([i, batch_data[i,2], 'null'])
        else:
            att.append([i, batch_data[i,2]])
    print(att)
    intrusion_mask = (intrusion > 0)


    next_end_link = None
    prev_end_link = None
    # if have prev
    if start > 0:
        prev_end_link = str(pk) + '/' + str(start) + '/'+ '2' + '/'
    # if have next
    if (end + 1) * 100 < num_data:
        next_end_link = str(pk) + '/' + str(start) + '/'+ '1' + '/'

    module_name = module.module_name + "     >>>     Start: " + str(start_index) + "  End: " + str(end_index)
    return render(request, "module/view_module.html", {'title_list': ['duration', 'protocol_type ',
                                                                'service', 'src_bytes ',
                                                                 'dst_bytes', 'flag',
                                                                 'land', 'wrong_fragment','urgent',
                                                                 'hot' ], 'batch': list(batch_data[intrusion_mask,:10]), 
                                                                 'attr': att, 'prev':prev_end_link, 'next':next_end_link, 
                                                                 'module_name':module_name
                                                                 })

def new_module(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ModuleForm(request.POST)
        # check whether it's valid:
        print("in post")
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # handle_file(request.FILES['file'])
            module_name = form.cleaned_data['module_name']
            new_record_period = form.cleaned_data['new_record_period']
            access_level = form.cleaned_data['access_level']
            # num_batch_per_period = form.cleaned_data['num_batch_per_period']
            # date_created = form.cleaned_data['date_created']
            description = form.cleaned_data['description']

            quality_data_indexing_dict_path = form.cleaned_data['quality_data_indexing_dict_path']
            data_storage_path = form.cleaned_data['data_storage_path']
            csv_file_path = form.cleaned_data['csv_file_path']

            data_storage_path += '/'+module_name + '.npy'
            array = handle_import(csv_file_path, quality_data_indexing_dict_path)
            np.save(data_storage_path, array)
            print("Here")
            new_module = Module(module_name = module_name,
                                new_record_period = new_record_period,
                                access_level = access_level,
                                description = description,
                                quality_data_indexing_dict_path = quality_data_indexing_dict_path,
                                data_storage_path = data_storage_path,
                                csv_file = csv_file_path)
            instance = new_module.save()
            print("New module ok")
            
            print("Form valid")
            # redirect to a new URL:
            return HttpResponseRedirect('http://127.0.0.1:8000/module/module/'+str(new_module.id)+'/'+"0"+ "/"+'0')
        else:
            print("Something went wrong")

    # if a GET (or any other method) we'll create a blank form
    else:
        print("Hehe something is wrong")
        form = ModuleForm()

    return render(request, 'module/module.html', {'form': form})

'''
class CreateModule(CreateView):
    model=Module
    fields=['module_name', 'new_record_period', 'access_level', 'num_batch_per_period', 'date_created', 'quality_data_indexing_dict_path', 'data_storage_path','csv_file',  'description']
'''
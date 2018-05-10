from django.db import models
from django.urls import reverse
# Create your models here.
class Module(models.Model):

    #module_id = models.AutoField(primary_key = True)
    module_name = models.CharField(max_length = 255)
    new_record_period = models.CharField(max_length = 100, default = 'Hours')
    access_level = models.CharField(max_length = 100)
    quality_data_indexing_dict_path = models.CharField(max_length = 255)
    data_storage_path = models.CharField(max_length = 255)
    csv_file = models.FileField(upload_to='uploads/')
    description =  models.CharField(max_length = 255, default='No Description')

    def get_absolute_url(self):
        return reverse('module:view_module', kwargs={'pk':self.pk})

    def __str__(self):
        return self.module_name

class User(models.Model):
    #user_id = module_id = models.AutoField(primary_key = True)
    username = models.TextField()
    password = models.TextField()
    access_level = models.TextField()

    def __str__(self):
        return self.username

class Attack(models.Model):
    attack_datetime = models.DateTimeField()
    attack_module_id = models.ForeignKey('Module', on_delete = models.CASCADE)
    attack_type = models.IntegerField(default = 1)

    def __str__(self):
        return str(self.attack_type)+ '-' + str(self.attack_module_id)


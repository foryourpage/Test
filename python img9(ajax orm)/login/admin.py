from django.contrib import admin
from . import models

admin.site.register(models.User)


# Register your models here.
class TestAdmin(admin.ModelAdmin):
    list_display = ('state', 'time', 'ex_num', 'lot', 'workshop',  'short_or_list', 'ex_type', 'ex_detail',
                    'ex_number', 'op_head', 'op_unit', 'client_type', 'short_client_name', 'short_des',
                    'short_des_confirm', 'short_improve', 'short_effect_confirm', 'op_dispose')


admin.site.register(models.Test, TestAdmin)

from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Plan)
admin.site.register(Category)
admin.site.register(OnlineIdea)
admin.site.register(PlanCategoryOnlineIdea)

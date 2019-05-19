from django.contrib import admin
from .models import *


admin.site.register(Book)
admin.site.register(Category)
admin.site.register(BookState)
admin.site.register(Images)
admin.site.register(Sell)
admin.site.register(Request)

# Register your models here.

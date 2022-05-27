from django.contrib import admin
from webapp.models import User,Transaction_Pairs,Transaction_history,UserProfile

admin.site.register(Transaction_Pairs)
admin.site.register(Transaction_history)
admin.site.register(UserProfile)
# Register your models here.

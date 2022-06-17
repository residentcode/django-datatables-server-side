from django.contrib import admin
from home_view.models import People


# admin.site.register(Employee)
@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'city', 'gender')
    list_per_page = 30
    search_fields = ['first_name', 'last_name', 'email', 'city', 'gender']

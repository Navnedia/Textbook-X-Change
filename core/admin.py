from django.contrib import admin
from .models import School, Course, Book, Author

# Register core models here:

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'school__name')
    search_fields = ('code', 'school__name')
    

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'get_authors')
    search_fields = ('title', 'isbn', 'authors__name', 'courses__code', 'courses__school__name')
    readonly_fields = ('created_at', 'updated_at')

    def get_authors(self, obj):
        return ", ".join([author.name for author in obj.authors.all()])
    get_authors.short_description = "Author(s)"


admin.site.register(School)
admin.site.register(Author)
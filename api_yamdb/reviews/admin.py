from django.contrib import admin

from reviews.models import Category, Genre


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    search_fields = ("name",)
    list_filter = ("id",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    search_fields = ("name",)
    list_filter = ("id",)


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)

from django.contrib import admin

from reviews.models import Category, Genre, Title


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


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "description",
        "category",
    )
    search_fields = ("name",)
    list_filter = ("id",)


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)

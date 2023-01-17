from django.contrib import admin

from reviews.models import Category, Genre, Title, GenreTitle


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
    list_filter = ("category",)


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "genre",
    )
    search_fields = ("title",)
    list_filter = ("genre",)


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)

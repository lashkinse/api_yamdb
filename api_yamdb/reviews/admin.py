from django.contrib import admin

from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment


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


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "score", "pub_date")
    search_fields = ("text",)
    list_filter = ("score",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "pub_date")
    search_fields = ("text",)
    list_filter = ("author",)


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)

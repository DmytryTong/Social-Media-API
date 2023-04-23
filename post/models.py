from config import settings
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    TEXT_PREVIEW_LEN = 50

    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="posts")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    class Meta:
        ordering = ["-created_at"]

    @property
    def text_preview(self) -> str:
        return (
            self.content
            if len(self.content) < Post.TEXT_PREVIEW_LEN
            else self.content[: Post.TEXT_PREVIEW_LEN] + "..."
        )

    def __str__(self):
        return self.title

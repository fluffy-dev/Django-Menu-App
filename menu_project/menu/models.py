from django.core.exceptions import ValidationError
from django.db import models
from django.urls import NoReverseMatch, reverse


class MenuItem(models.Model):
    """Represents a single item in a hierarchical menu."""

    name = models.CharField(
        max_length=100,
        verbose_name="Название пункта"
    )
    menu_name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name="Название меню"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Родительский пункт"
    )
    url = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Прямой URL (например, /about/)"
    )
    named_url = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Именованный URL (например, 'main_page')"
    )

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"
        ordering = ['menu_name', 'pk']

    def __str__(self) -> str:
        """String representation of the menu item."""
        return f"{self.menu_name} | {self.name}"

    def get_url(self) -> str:
        """
        Returns the resolved URL for the menu item.

        Prioritizes the named URL, falling back to the explicit URL.
        Returns '#' if the named URL cannot be reversed.

        Returns:
            The resolved URL as a string.
        """
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return "#"
        return self.url

    def clean(self):
        """
        Ensures data integrity for the menu item.

        Raises:
            ValidationError: If both URL and named URL are provided,
                or if neither is provided for a non-root item.
        """
        if self.url and self.named_url:
            raise ValidationError(
                "Нельзя одновременно указывать и прямой, и именованный URL."
            )
        if not self.url and not self.named_url:
            if self.parent:
                raise ValidationError(
                    "Необходимо указать либо прямой, либо именованный URL."
                )
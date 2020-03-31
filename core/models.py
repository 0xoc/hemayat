from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Location(models.Model):
    """
        Location Model

        Latitude, Longitude pair with an optional name
    """

    name = models.CharField(max_length=255, blank=True, null=True, help_text="Optional name for the given location")
    lat = models.DecimalField(max_digits=22, decimal_places=16, help_text="latitude")
    lon = models.DecimalField(max_digits=22, decimal_places=16, help_text="longitude")

    note_text = models.TextField(help_text="Note")  # redundant for performance

    class Meta:
        unique_together = ('lat', 'lon',)

    def __str__(self):
        return "%s - %d, %d" % (self.name, self.lat, self.lon)


@receiver(post_save, sender=Location, dispatch_uid="update_stock_count")
def update_stock(sender, instance, **kwargs):
    if instance.notes.exists() and instance.notes.last().text == instance.note_text:
        return
    Note.objects.create(
        location=instance,
        text=instance.note_text
    )


class Note(models.Model):
    """
        A note on a location

        with automatic timestamp
    """

    title = models.CharField(max_length=255, blank=True, null=True, help_text="Optional title for the note")
    text = models.TextField(help_text="Note")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="notes")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Create datetime of the note")

    def __str__(self):
        return "%s | %s" % (self.title, str(self.location))

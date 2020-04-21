from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
        Profile for a user
    """
    user = models.ForeignKey(User, related_name="user_profile", on_delete=models.CASCADE)


class Location(models.Model):
    """
        Location Model

        Latitude, Longitude pair with an optional name
    """

    title = models.CharField(max_length=255, blank=True, null=True, help_text="Optional name for the given location")
    latitude = models.DecimalField(max_digits=22, decimal_places=16, help_text="latitude")
    longitude = models.DecimalField(max_digits=22, decimal_places=16, help_text="longitude")
    
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    pelak = models.CharField(max_length=255, blank=True, null=True)
    sarparast = models.CharField(max_length=255, blank=True, null=True)
    mantaqe = models.CharField(max_length=255, blank=True, null=True)
    rabet = models.CharField(max_length=255, blank=True, null=True)

    created_by = models.ForeignKey(
        UserProfile,
        related_name="locations",
        on_delete=models.PROTECT,
        help_text="Creator of the note",
        blank=True,
        null=True
    )
    updated_by = models.ForeignKey(
        UserProfile,
        related_name="updated_locations",
        on_delete=models.PROTECT,
        help_text="Creator of the note",
        blank=True,
        null=True
    )

    note_text = models.TextField(help_text="Note", blank=True, null=True)  # redundant for performance

    @property
    def latest_note(self) -> "Note":
        return self.notes.last()

    class Meta:
        unique_together = ('latitude', 'longitude',)

    def __str__(self):
        return "%s - %d, %d" % (self.title, self.latitude, self.longitude)


@receiver(post_save, sender=Location, dispatch_uid="update_stock_count")
def update_stock(sender, instance, **kwargs):
    if instance.notes.exists() and instance.notes.last().text == instance.note_text:
        return
    Note.objects.create(
        user_profile=instance.updated_by,
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

    user_profile = models.ForeignKey(
        UserProfile,
        related_name="notes",
        on_delete=models.PROTECT,
        help_text="Creator of the note",
        blank=True,
        null=True
    )

    def __str__(self):
        return "%s | %s" % (self.title, str(self.location))

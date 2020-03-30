from django.db import models

class Location(models.Model):
    """
        Location Model

        Latitude, Longitude pair with an optional name
    """
    
    name = models.CharField(max_length=255,blank=True, null=True, help_text="Optional name for the given location")
    lat = models.DecimalField(max_digits=22, decimal_places=16, help_text="latitude")
    lon = models.DecimalField(max_digits=22, decimal_places=16, help_text="longitude")

    class Meta:
        unique_together = ('lat', 'lon',)

    def __str__(self):
        return "%s - %d, %d" % (self.name, self.lat, self.lon)


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

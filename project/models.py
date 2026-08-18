from django.db import models
from django.db.models import F, Func


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    polygon = models.JSONField(
        help_text="GeoJSON geometry object, e.g. {'type': 'Polygon', 'coordinates': [...]}",
    )
    area = models.GeneratedField(
        expression=Func(
            F("polygon"),
            function="ST_Area",
            template="ST_Area(ST_GeomFromGeoJSON(%(expressions)s)::geography) / 10000",
            output_field=models.FloatField(),
        ),
        output_field=models.FloatField(),
        db_persist=True,
        help_text="Area in hectares, computed by PostGIS from polygon.",
    )
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.name

import shapely
from django.contrib.gis.db import models
from pyproj import Geod

SQUARE_METERS_PER_HECTARE = 10_000

_GEOD = Geod(ellps="WGS84")


class Survey(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    polygon = models.PolygonField(help_text="Geometry field representing the survey area, stored as a PostGIS polygon.")
    area = models.FloatField(
        editable=False,
        help_text="Area in hectares, computed from the polygon on every save.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    workspace = models.ForeignKey("workspace.Workspace", on_delete=models.CASCADE, related_name="surveys")

    def __str__(self):
        return self.name

    def compute_area(self) -> float:
        """Geodesic area of the polygon in hectares, holes excluded."""
        # pyproj derives the sign of each ring from its winding order, so normalize it first:
        # exterior counter-clockwise, holes clockwise, otherwise holes get added instead of subtracted.
        geometry = shapely.orient_polygons(shapely.from_wkb(bytes(self.polygon.wkb)))
        square_meters, _ = _GEOD.geometry_area_perimeter(geometry)
        return abs(square_meters) / SQUARE_METERS_PER_HECTARE

    def save(self, *args, **kwargs):
        self.area = self.compute_area()
        if (fields := kwargs.get("update_fields")) is not None and "polygon" in fields:
            kwargs["update_fields"] = {*fields, "area"}
        super().save(*args, **kwargs)

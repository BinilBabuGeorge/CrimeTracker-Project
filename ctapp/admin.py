from django.contrib import admin
from django.utils.html import format_html

from .models import Crime, PoliceOfficer, PoliceStation

admin.site.register(PoliceStation)
admin.site.register(PoliceOfficer)


@admin.register(Crime)
class CrimeAdmin(admin.ModelAdmin):
    list_display = ("crime_id", "subject", "user", "category", "status", "coordinates")
    readonly_fields = ("map_preview",)
    fields = (
        "user",
        "category",
        "district",
        "police_station",
        "police_officer",
        "place",
        "subject",
        "complaint_text",
        "crime_datetime",
        "supporting_document",
        "status",
        "latitude",
        "longitude",
        "map_preview",
    )

    def coordinates(self, obj):
        return obj.coordinates_display()

    def map_preview(self, obj):
        if not obj or not obj.has_location():
            return "Location not selected."

        return format_html(
            '<div class="leaflet-complaint-map map-lg" '
            'data-mode="view" '
            'data-lat="{}" '
            'data-lng="{}" '
            'data-popup-text="Complaint #{}"></div>'
            '<div class="leaflet-map-note">Complaint coordinates: {}, {}</div>',
            obj.latitude,
            obj.longitude,
            obj.crime_id,
            obj.latitude,
            obj.longitude,
        )

    map_preview.short_description = "Complaint Location"

    class Media:
        css = {
            "all": (
                "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
                "ctapp/css/complaint_maps.css",
            )
        }
        js = (
            "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js",
            "ctapp/js/complaint_maps.js",
        )

# admin.py
# Register your models here.

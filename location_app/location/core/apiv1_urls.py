from django.urls import path, include

from location.locations import views as locations_views

app_name = "core"

urlpatterns = [
    path(
        "locations", view=locations_views.CreateLocationView.as_view(), name="locations"
    ),
    path(
        "locations/find",
        view=locations_views.FindLocationView.as_view(),
        name="locations_find",
    ),
]

"""Django urlpatterns declaration for nautobot_dev_example app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.apps.urls import NautobotUIViewSetRouter

from nautobot_dev_example import views

router = NautobotUIViewSetRouter()
router.register("devexample", views.DevExampleUIViewSet)

urlpatterns = [
    path("docs/", RedirectView.as_view(url=static("nautobot_dev_example/docs/index.html")), name="docs"),
]

urlpatterns += router.urls

"""Django urlpatterns declaration for nautobot_dev_example app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.apps.urls import NautobotUIViewSetRouter

from nautobot_dev_example import views

app_name = "nautobot_dev_example"
router = NautobotUIViewSetRouter()

router.register("dev-examples", views.DevExampleUIViewSet)


urlpatterns = [
    path("docs/", RedirectView.as_view(url=static("nautobot_dev_example/docs/index.html")), name="docs"),
    # Pointing Poker
    path("poker/", views.PokerNewTableView.as_view(), name="poker_new"),
    path("poker/<int:table_id>/", views.PokerTableView.as_view(), name="poker_table"),
    # Pointing Poker HTMX Polling Endpoint
    path("poker/<int:table_id>/poll/", views.PokerPollView.as_view(), name="poker_poll"),
    # Pointing Poker HTMX Action Endpoint
    path("poker/<int:table_id>/action/", views.PokerActionView.as_view(), name="poker_action"),
]

urlpatterns += router.urls

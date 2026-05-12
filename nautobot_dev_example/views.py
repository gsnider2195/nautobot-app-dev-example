"""Views for nautobot_dev_example."""

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, View
from nautobot.apps.ui import ObjectDetailContent, ObjectFieldsPanel, SectionChoices
from nautobot.apps.views import NautobotUIViewSet

# if/when use the table, uncomment the following lines
# from nautobot.core.templatetags import helpers
# from nautobot.apps.ui import ObjectsTablePanel
from nautobot_dev_example import filters, forms, models, tables
from nautobot_dev_example.api import serializers


class DevExampleUIViewSet(NautobotUIViewSet):
    """ViewSet for DevExample views."""

    bulk_update_form_class = forms.DevExampleBulkEditForm
    filterset_class = filters.DevExampleFilterSet
    filterset_form_class = forms.DevExampleFilterForm
    form_class = forms.DevExampleForm
    lookup_field = "pk"
    queryset = models.DevExample.objects.all()
    serializer_class = serializers.DevExampleSerializer
    table_class = tables.DevExampleTable

    # Here is an example of using the UI  Component Framework for the detail view.
    # More information can be found in the Nautobot documentation:
    # https://docs.nautobot.com/projects/core/en/stable/development/core/ui-component-framework/
    object_detail_content = ObjectDetailContent(
        panels=[
            ObjectFieldsPanel(
                weight=100,
                section=SectionChoices.LEFT_HALF,
                fields="__all__",
                # Alternatively, you can specify a list of field names:
                # fields=[
                #     "name",
                #     "description",
                # ],
                # Some fields may require additional configuration, we can use value_transforms
                # value_transforms={
                #     "name": [helpers.bettertitle]
                # },
            ),
            # If there is a ForeignKey or M2M with this model we can use ObjectsTablePanel
            # to display them in a table format.
            # ObjectsTablePanel(
            # weight=200,
            # section=SectionChoices.RIGHT_HALF,
            # table_class=tables.DevExampleTable,
            # You will want to filter the table using the related_name
            # filter="devexamples",
            # ),
        ],
    )


class PokerNewTableView(View):
    def get(self, request):
        table = models.PokerTable.objects.create()
        return redirect(reverse("plugins:nautobot_dev_example:poker_table", kwargs={"table_id": table.id}))


class PokerTableView(TemplateView):
    """Renders the main page."""

    template_name = "nautobot_dev_example/poker_table.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # table_id comes from the URL kwargs
        context["table"] = get_object_or_404(models.PokerTable, id=self.kwargs["table_id"])
        return context


class PokerPollView(TemplateView):
    """Renders only the partial HTML fragment for htmx polling."""

    template_name = "nautobot_dev_example/poker_votes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = get_object_or_404(models.PokerTable, id=self.kwargs["table_id"])
        context["table"] = table
        context["votes"] = models.Vote.objects.filter(table=table).select_related("user")
        return context


class PokerActionView(View):
    """Handles POST actions: vote, reveal, and clear."""

    def post(self, request, table_id):
        table = get_object_or_404(models.PokerTable, id=table_id)
        action = request.POST.get("action")

        if action == "vote":
            value = request.POST.get("value")
            models.Vote.objects.update_or_create(
                table=table, user=request.user, defaults={"value": int(value) if value else None}
            )
        elif action == "reveal":
            table.is_revealed = True
            table.save()
        elif action == "clear":
            table.is_revealed = False
            table.is_cleared = True
            models.Vote.objects.filter(table=table).delete()
            table.is_cleared = False
            table.save()

        # After the action, return the updated partial immediately
        votes = models.Vote.objects.filter(table=table).select_related("user")
        return render(request, "nautobot_dev_example/poker_votes.html", {"table": table, "votes": votes})

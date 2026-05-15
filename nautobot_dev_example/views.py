"""Views for nautobot_dev_example."""

from django.shortcuts import redirect
from django.urls import reverse
from nautobot.apps.ui import ObjectDetailContent, ObjectFieldsPanel, SectionChoices
from nautobot.apps.views import NautobotUIViewSet, ObjectDetailViewMixin, ObjectListViewMixin
from rest_framework.decorators import action
from rest_framework.response import Response

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


class PokerTableUIViewSet(ObjectDetailViewMixin):
    """ViewSet for PokerTable views."""

    filterset_class = None
    filterset_form_class = None
    form_class = None
    lookup_field = "pk"
    queryset = models.PokerTable.objects.all()
    serializer_class = None
    table_class = None

    # object_detail_content = ObjectDetailContent(
    #     panels=[
    #         ObjectFieldsPanel(
    #             weight=100,
    #             section=SectionChoices.LEFT_HALF,
    #             fields=["name", "is_revealed", "is_cleared"],
    #         ),
    #     ],
    # )

    @action(url_path="poll", detail=True)
    def poll(self, request, *args, **kwargs):
        table = self.get_object()
        return Response({"votes": models.Vote.objects.filter(table=table).select_related("user")})

    @action(url_path="action", methods=["POST"], detail=True)
    def action_endpoint(self, request, *args, **kwargs):
        table = self.get_object()
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

        # After the action, return the updated poll fragment immediately
        return redirect(reverse("plugins:nautobot_dev_example:pokertable_poll", kwargs={"pk": table.id}))

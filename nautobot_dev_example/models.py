"""Models for Nautobot Dev Example App."""

# Django imports
from django.contrib.auth import get_user_model
from django.db import models

# Nautobot imports
from nautobot.apps.constants import CHARFIELD_MAX_LENGTH
from nautobot.apps.models import PrimaryModel, extras_features

User = get_user_model()


# If you want to choose a specific model to overload in your class declaration, please reference the following documentation:
# how to chose a database model: https://docs.nautobot.com/projects/core/en/stable/plugins/development/#database-models
# If you want to use the extras_features decorator please reference the following documentation
# https://docs.nautobot.com/projects/core/en/stable/development/core/model-checklist/#extras-features
@extras_features("custom_links", "custom_validators", "export_templates", "graphql", "webhooks")
class DevExample(PrimaryModel):  # pylint: disable=too-many-ancestors
    """Base model for Nautobot Dev Example App app."""

    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH, unique=True)
    description = models.CharField(max_length=CHARFIELD_MAX_LENGTH, blank=True)
    # additional model fields

    class Meta:
        """Meta class."""

        ordering = ["name"]

        # Option for fixing capitalization (i.e. "Snmp" vs "SNMP")
        # verbose_name = "Nautobot Dev Example App"

        # Option for fixing plural name (i.e. "Chicken Tenders" vs "Chicken Tendies")
        # verbose_name_plural = "Nautobot Dev Example Apps"

    def __str__(self):
        """Stringify instance."""
        return self.name


class PokerTable(models.Model):
    name = models.CharField(max_length=100)
    is_revealed = models.BooleanField(default=False)
    is_cleared = models.BooleanField(default=False)


class Vote(models.Model):
    table = models.ForeignKey(PokerTable, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(null=True, blank=True)  # Null means "hasn't voted yet"

"""Account models."""
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Customized version of Django's User model."""

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        blank=True,
        null=True,
    )
    mobile = models.CharField(max_length=settings.MOBILE_LENGTH)
    image = models.URLField()

    def __str__(self):
        return self.get_full_name()


@receiver(signals.post_save, sender=User)
def add_user_in_default_group(instance, created, **_):
    """Add a new user in default group."""
    if (
        created
        and not instance.groups.filter(name=settings.DEFAULT_USER_GROUP).exists()
    ):
        default_group = Group.objects.get_or_create(name=settings.DEFAULT_USER_GROUP)
        instance.groups.add(default_group[0].id)
        instance.save()

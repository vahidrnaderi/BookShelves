"""Page serializers."""
from django.conf import settings
from rest_framework import serializers

from .models import GroupMenu, Menu, Page


class PageSerializer(serializers.ModelSerializer):
    """Page serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="page:page-detail")

    class Meta:
        model = Page
        exclude = ("is_deleted",)


class MenuSerializer(serializers.ModelSerializer):
    """Menu serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="page:menu-detail")
    link_details = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        exclude = ("is_deleted",)

    def get_link_details(self, obj):
        """Serialize link details based on loaded serializers."""
        instance = obj.link_type.model_class().objects.get(id=obj.link)
        instance_serializer_name = f"{instance.__class__.__name__}Serializer"
        if instance_serializer_name in settings.SERIALIZERS:
            instance_serializer = settings.SERIALIZERS[instance_serializer_name]
            return instance_serializer(
                instance=instance, context={"request": self.context["request"]}
            ).data
        return obj.link


class GroupMenuSerializer(serializers.ModelSerializer):
    """Group menu serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="page:group_menu-detail")
    menus = MenuSerializer(source="menu_set", many=True, read_only=True)

    class Meta:
        model = GroupMenu
        exclude = ("is_deleted",)

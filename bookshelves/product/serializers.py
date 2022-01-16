"""Product serializers."""
from rest_framework import serializers
from product.models import (
    AudioType,
    # AudioBook,
    Publisher,
    BookAuthor,
    AudioIndex,
    BookSpeaker,
    CompatibleDevice,
    Tag,
    Category,
    Product,
)


class TagSerializer(serializers.ModelSerializer):
    """Tag serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:tag-detail")

    class Meta:
        model = Tag
        fields = (
            "url",
            "id",
            "name",
        )
        ref_name = "product"


class PublisherSerializer(serializers.ModelSerializer):
    """Publisher serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:publisher-detail")

    class Meta:
        model = Publisher
        fields = (
            "url",
            "id",
            "name",
        )


class BookAuthorSerializer(serializers.ModelSerializer):
    """Book author serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:book_author-detail")

    class Meta:
        model = BookAuthor
        fields = (
            "url",
            "id",
            "name",
        )


class BookSpeakerSerializer(serializers.ModelSerializer):
    """Book speaker serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:book_speaker-detail")

    class Meta:
        model = BookSpeaker
        fields = (
            "url",
            "id",
            "name",
        )


class AudioTypeSerializer(serializers.ModelSerializer):
    """Audio type serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:audio_type-detail")

    class Meta:
        model = AudioType
        fields = (
            "url",
            "id",
            "name",
        )


class CompatibleDeviceSerializer(serializers.ModelSerializer):
    """Compatible device serializer."""

    url = serializers.HyperlinkedIdentityField(
        view_name="product:compatible_devices-detail"
    )

    class Meta:
        model = CompatibleDevice
        fields = (
            "url",
            "id",
            "name",
            "version",
        )


class AudioIndexSerializer(serializers.ModelSerializer):
    """Audio index serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:audio_index-detail")

    class Meta:
        model = AudioIndex
        fields = (
            "url",
            "id",
            "title",
            "file",
            "duration",
            "is_downloadable",
        )


class BookmarkSerializer(serializers.ModelSerializer):
    """Bookmark serializer."""

    product = serializers.PrimaryKeyRelatedField(source="id", read_only=True)

    class Meta:
        model = Product
        fields = ("product",)
        ref_name = "product"


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:category-detail")

    class Meta:
        model = Category
        fields = (
            "url",
            "id",
            "name",
            "parent",
        )
        ref_name = "product"


class AudioBookSerializer(serializers.ModelSerializer):
    """Audio book serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:audio_book-detail")
    bookmarks_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_bookmarks_count(self, obj):
        """Get product's bookmarks count."""
        return obj.bookmarks.count()

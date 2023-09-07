"""Blog views."""
import uuid

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Avg

from .models import Post, Tag, Star, Category, Comment
from .serializers import (
    PostSerializer,
    TagSerializer,
    StarSerializer,
    CategorySerializer,
    CommentSerializer,
)


def full_posts(post):
    """Get together post fields relations and retrieve data as json."""
    post_serializer = PostSerializer(post)

    stars = Star.objects.filter(post=post.id)
    average_stars = Star.objects.filter(post=post.id).aggregate(Avg("star"))[
        "star__avg"
    ]
    star_serializer = StarSerializer(stars, many=True)

    result = post_serializer.data
    result.update({"stars": star_serializer.data})
    result.update({"average_stars": average_stars if average_stars else 0})

    comments = Comment.objects.filter(post=post.id, is_approved=True)
    comments_count = comments.count()
    result.update({"commentsCount": comments_count})
    if comments:
        comment_serializer = CommentSerializer(comments, many=True)
        result.update({"comments": comment_serializer.data})
    else:
        result.update({"comments": comments})

    result = {str(post.id): result}

    return result


def get_user_id():  # **************** must complete ****************
    """Retrieve user ID."""
    user_id = 1

    return user_id


@api_view(["GET", "POST"])
def posts_list(request):
    """List all posts, or create a new post."""
    if request.method == "GET":
        posts = Post.objects.all().exclude(is_deleted=True)

        result = {}

        for post in posts:
            if result == {}:
                result = full_posts(post)
            else:
                result.update(full_posts(post))

        return Response(result)

    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def post_detail(request, post_id_or_title):
    """Retrieve, update or delete a post."""
    try:
        if isinstance(post_id_or_title, str):
            post = Post.objects.get(title=post_id_or_title)
        elif uuid.UUID(str(post_id_or_title)):
            post = Post.objects.get(id=post_id_or_title)
    except Post.DoesNotExist:
        return Response(
            {"errorCode": "404", "message": "Post with your value Dose Not Exist!"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        return Response(full_posts(post))

    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        serializer = CategorySerializer(post, data={"is_deleted": True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST", "DELETE"])
def post_bookmark(request, post_id_or_title):
    """Bookmark a post or Delete a bookmark."""
    try:
        if isinstance(post_id_or_title, str):
            post = Post.objects.get(title=post_id_or_title)
        elif uuid.UUID(str(post_id_or_title)):
            post = Post.objects.get(id=post_id_or_title)
    except Post.DoesNotExist:
        return Response(
            {"errorCode": "404", "message": "Post with your value Dose Not Exist!"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "POST":
        post.bookmark.add(get_user_id())
        return Response(PostSerializer(post).data)

    elif request.method == "DELETE":
        post.bookmark.remove(get_user_id())
        return Response(PostSerializer(post).data)


@api_view(["POST"])
def new_post_tag(request, post_id_or_title):
    """Create a new tag for a post."""
    try:
        if isinstance(post_id_or_title, str):
            post = Post.objects.get(title=post_id_or_title)
        elif uuid.UUID(str(post_id_or_title)):
            post = Post.objects.get(id=post_id_or_title)
    except Post.DoesNotExist:
        return Response(
            {"errorCode": "404", "message": "Post with your value Dose Not Exist!"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "POST":
        tag_serializer = TagSerializer(data=request.data)
        if tag_serializer.is_valid():
            tag_serializer.save()

            tag = Tag.objects.get(id=tag_serializer.data["id"])
            post.tags.add(tag)
            return Response(PostSerializer(post).data)
        else:
            return Response(tag_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_post_tag(request, post_id_or_title, tag_id_or_name):
    """Delete a tag from a post."""
    try:
        if isinstance(post_id_or_title, str):
            post = Post.objects.get(title=post_id_or_title)
        elif uuid.UUID(str(post_id_or_title)):
            post = Post.objects.get(id=post_id_or_title)
    except Post.DoesNotExist:
        return Response(
            {"errorCode": "404", "message": "Post with your value Dose Not Exist!"},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        if isinstance(tag_id_or_name, str):
            tag = Tag.objects.get(name=tag_id_or_name)
        elif uuid.UUID(str(tag_id_or_name)):
            tag = Tag.objects.get(id=tag_id_or_name)
    except Tag.DoesNotExist:
        return Response(
            {"errorCode": "404", "message": "Tag with your value Dose Not Exist!"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "DELETE":
        if post.tags.get(id=tag.id):
            post.tags.remove(tag)
            return Response(PostSerializer(post).data)
        else:
            return Response(
                {
                    "errorCode": "404",
                    "message": "Post Does Not have any Tag with value you entered!!",
                },
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(["GET"])
def tag_posts(request, tag_id_or_name):
    """List all posts with one tag."""
    if request.method == "GET":

        try:
            if isinstance(tag_id_or_name, str):
                tag = Tag.objects.get(name=tag_id_or_name)
            elif uuid.UUID(str(tag_id_or_name)):
                tag = Tag.objects.get(id=tag_id_or_name)
        except Tag.DoesNotExist:
            return Response(
                {"errorCode": "404", "message": "Tag with your value Dose Not Exist!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        posts = Post.objects.filter(tags=tag.id)

        result = {}

        for post in posts:
            if result == {}:
                result = full_posts(post)
            else:
                result.update(full_posts(post))

        return Response(result)


@api_view(["POST"])
def new_post_star(request, post_id_or_title):
    """Create a star for a post."""
    if request.method == "POST":

        try:
            if isinstance(post_id_or_title, str):
                post = Post.objects.get(title=post_id_or_title)
            elif uuid.UUID(str(post_id_or_title)):
                post = Post.objects.get(id=post_id_or_title)
        except Post.DoesNotExist:
            return Response(
                {"errorCode": "404", "message": "Post with your value Dose Not Exist!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data
        data["post"] = post.id
        data["user"] = get_user_id()
        serializer = StarSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_stars(request):
    """Retrieve all stars from specific user."""
    try:
        stars = Star.objects.filter(user=get_user_id())
    except Star.DoesNotExist:
        return Response(
            {"errorCode": "404", "message": "Star with your value Dose Not Exist!"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = StarSerializer(stars, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def user_bookmarks(request):
    """Retrieve all specific user's bookmarks."""
    try:
        bookmarks = Post.objects.filter(bookmark=get_user_id())
    except Post.DoesNotExist:
        return Response(
            {"errorCode": "404", "message": "Star with your value Dose Not Exist!"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = PostSerializer(bookmarks, many=True)
        return Response(serializer.data)


@api_view(["GET", "POST"])
def tags_list(request):
    """List all tags, or create a tag."""
    if request.method == "GET":
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def tag_detail(request, tag_id_or_name):
    """Retrieve a tag."""
    try:
        if isinstance(tag_id_or_name, str):
            tag = Tag.objects.get(name=tag_id_or_name)
        elif uuid.UUID(str(tag_id_or_name)):
            tag = Tag.objects.get(id=tag_id_or_name)
    except Tag.DoesNotExist:
        return Response(
            {"errorCode": "404", "message": "Tag with your value Dose Not Exist!"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = TagSerializer(tag)
        return Response(serializer.data)


@api_view(["GET", "POST"])
def categories_list(request):
    """List all categories, or create a new category."""
    if request.method == "GET":
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def category_detail(request, category_id_or_name):
    """Retrieve, update or delete a category."""
    try:
        if isinstance(category_id_or_name, str):
            category = Category.objects.get(name=category_id_or_name)
        elif uuid.UUID(str(category_id_or_name)):
            category = Category.objects.get(id=category_id_or_name)
    except Category.DoesNotExist:
        return Response(
            {"errorCode": "404", "message": "Category with your value Dose Not Exist!"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        serializer = CategorySerializer(
            category, data={"is_deleted": True}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "DELETE"])
def comment_detail(request, comment_id):
    """Retrieve or delete a comment."""
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response(
            {"errorCode": "404", "message": "Comment with your value Dose Not Exist!"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == "DELETE":
        serializer = CategorySerializer(
            comment, data={"is_deleted": True}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["PUT"])
def comment_approve(request, comment_id):
    """Approve or disapprove a comment for a post."""
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response(
            {"errorCode": "404", "message": "Comment with your value Dose Not Exist!"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "PUT":
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def post_comment(request, post_id_or_title):
    """Retrieve all comments or Create a new comment for a post."""
    try:
        if isinstance(post_id_or_title, str):
            post = Post.objects.get(title=post_id_or_title)
        elif uuid.UUID(str(post_id_or_title)):
            post = Post.objects.get(id=post_id_or_title)
    except Post.DoesNotExist:
        return Response(
            {"errorCode": "404", "message": "Post with your value Dose Not Exist!"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "POST":
        data = request.data
        data["post"] = post.id
        data["user"] = get_user_id()
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "GET":
        comments = Comment.objects.filter(post=post.id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


@api_view(["POST"])
def new_comment_reply(request, post_id_or_title, comment_id):
    """Create a new comment's reply for a post."""
    try:
        if isinstance(post_id_or_title, str):
            post = Post.objects.get(title=post_id_or_title)
        elif uuid.UUID(str(post_id_or_title)):
            post = Post.objects.get(id=post_id_or_title)
    except Post.DoesNotExist:
        return Response(
            {"errorCode": "404", "message": "Post with your value Dose Not Exist!"},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response(
            {"errorCode": "404", "message": "Post with your value Dose Not Exist!"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "POST":
        data = request.data
        data["post"] = post.id
        data["reply_to"] = comment.id
        data["user"] = get_user_id()
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
"""

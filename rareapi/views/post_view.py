"""View module for handling requests about posts"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, Reaction, Tag, Author, Category, PostTag, Subscription


class PostView(ViewSet):
    """Rare post view"""

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk):
        """Handle GET requests for events

        Returns:
            Response -- JSON serialized events
        """
        try:
            post = Post.objects.get(pk=pk)

        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all posts

        Returns:
            Response -- JSON serialized list of posts
        """
        posts = []
        author = Author.objects.get(user=request.auth.user)
        
        if "subscribed" in request.query_params:
            subscriptions = Subscription.objects.filter(follower_id=author)

            for subscribed in subscriptions:
                subscription_author = subscribed.author
                posts = Post.objects.filter(author_id=subscription_author)
                
        elif "user" in request.query_params: 
            posts = Post.objects.filter(author_id=author)
            
        else:
            posts = Post.objects.all()

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        try:
            author = Author.objects.get(user=request.auth.user)
        except Author.DoesNotExist:
            return Response({'message': 'You sent an invalid token'}, status=status.HTTP_404_NOT_FOUND)

        try:
            category = Category.objects.get(pk=request.data['category'])
        except Category.DoesNotExist:
            return Response({'message': 'You sent an invalid category Id'}, status=status.HTTP_404_NOT_FOUND)

        post = Post.objects.create(
            author=author,
            category=category,
            title=request.data['title'],
            publication_date=request.data['publication_date'],
            image_url=request.data['image_url'],
            content=request.data['content']
        )

        tags_selected = request.data['tags']

        for tag in tags_selected:
            post_tag = PostTag()
            post_tag.post = post
            post_tag.tag = Tag.objects.get(pk=tag)
            post_tag.save()

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """

        try:
            category = Category.objects.get(pk=request.data['category'])
        except Category.DoesNotExist:
            return Response({'message': 'You sent an invalid category Id'}, status=status.HTTP_404_NOT_FOUND)

        post_to_update = Post.objects.get(pk=pk)
        post_to_update.publication_date = request.data['publication_date']
        post_to_update.category = category
        post_to_update.title = request.data['title']
        post_to_update.image_url = request.data['image_url']
        post_to_update.content = request.data['content']
        post_to_update.save()

        tags_selected = request.data['tags']

        current_tag_relationships = PostTag.objects.filter(post__id=pk)
        current_tag_relationships.delete()

        for tag in tags_selected:
            post_tag = PostTag()
            post_tag.post = post_to_update
            post_tag.tag = Tag.objects.get(pk=tag)
            post_tag.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PostReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions
    """
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'emoji_url')


class PostTagSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions
    """
    class Meta:
        model = Tag
        fields = ('id', 'label',)


class PostAuthorSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions
    """
    class Meta:
        model = Author
        fields = ('id', 'full_name')


class PostCategorySerializer(serializers.ModelSerializer):
    """JSON serializer for reactions
    """
    class Meta:
        model = Category
        fields = ('id', 'label')


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """

    reactions = PostReactionSerializer(many=True)
    tags = PostTagSerializer(many=True)
    author = PostAuthorSerializer()
    category = PostCategorySerializer(serializers.ModelSerializer)

    class Meta:
        model = Post
        fields = ('id', 'author', 'category',
                  'title', 'publication_date', 'image_url', 'content', 'approved',
                  'reactions', 'tags')

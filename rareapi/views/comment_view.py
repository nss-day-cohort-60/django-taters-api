from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment, Author, Post


class CommentView(ViewSet):

    def list(self, request):

        comments = Comment.objects.all()
        postId = self.request.query_params.get('postId')

        if postId is not None:
            comments = comments.filter(post=postId)
        
        else:
            pass

        serialized = CommentSerializer(comments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try: 
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist: 
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        serialized = CommentSerializer(comment, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def create(self, request):

        try:
            author = Author.objects.get(user=request.auth.user)
        except Author.DoesNotExist:
            return Response({'message': 'You sent an invalid token'}, status=status.HTTP_404_NOT_FOUND)

        try:
            post = Post.objects.get(pk=request.data['post'])
        except Post.DoesNotExist:
            return Response({'message': 'You sent an invalid post Id'}, status=status.HTTP_404_NOT_FOUND)
        
        comment = Comment.objects.create(
            author=author,
            post=post,
            content = request.data['content']
        )
        
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    
    def update(self, request, pk):
        """Handle POST operations
        Returns
            Response -- JSON serialized game instance
        """
        try:
            Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({'message': 'You sent an invalid comment Id'})
        
        comment_to_update = Comment.objects.get(pk=pk)
        comment_to_update.content=request.data["content"]
        comment_to_update.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PostAuthorSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions
    """
    class Meta:
        model = Author
        fields = ('id', 'full_name')
    
class CommentSerializer(serializers.ModelSerializer):

    author = PostAuthorSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'content' )
from rest_framework import serializers

from django.contrib.auth import authenticate

from accounts.models import User
from blogpost.models import BlogPost, Comment

class AuthorSerializer(serializers.Serializer):
    username = serializers.CharField()

class LikeSerializer(serializers.Serializer):
    username = serializers.CharField(source="likesblogpost_likes.username")

class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    comment = serializers.CharField()
    state = serializers.CharField(source="get_state_display", read_only=True)
    
class BlogPostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    likes = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="username"
    )


    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "description",
            "author",
            "likes",
            "picture",
            "comments",
        ]

    def get_comments(self, obj):
        comments = obj.comments.filter(state=Comment.STATE_CHOICES_APPROVED)
        return CommentSerializer(comments, read_only=True, many=True).data   


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            raise serializers.ValidationError("نام کاربری یا رمز عبور اشتباه است")

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        many = True
        fields = [
            "id",
            "username",
            "email",
        ]        
             
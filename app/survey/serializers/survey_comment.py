from rest_framework import serializers
from ..models import Comment


class GetSurveyCommentApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'parent_comment', 'user', 'survey')


class RecursiveCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'replies', 'user', 'survey')

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment=obj)
        serializer = self.__class__(replies, many=True)
        return serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['replies'] = self.get_replies(instance)
        return representation


class CommentTreeSerializer(RecursiveCommentSerializer):
    pass


# class GetSurveyCommentApiSerializer(serializers.ModelSerializer):
#     # children = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Comment
#         fields = ('id', 'text', 'parent_comment', 'user', 'survey')
#
#
# # class NestedCommentSerializer(serializers.ModelSerializer):
# #     replies = serializers.SerializerMethodField()
# #
# #     class Meta:
# #         model = Comment
# #         fields = ('id', 'text', 'replies')
# #
# #     def get_replies(self, obj):
# #         replies = Comment.objects.filter(parent_comment=obj)
# #         serializer = GetSurveyCommentApiSerializer(replies, many=True)
# #         return serializer.data
#
# class RecursiveCommentSerializer(serializers.ModelSerializer):
#     replies = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Comment
#         fields = ('id', 'text', 'replies', 'user', 'survey')
#
#     def get_replies(self, obj):
#         # Recursive function to get replies of a comment
#         replies = Comment.objects.filter(parent_comment=obj)
#         serializer = self.__class__(replies, many=True)
#         return serializer.data
#
#
# class CommentTreeSerializer(serializers.ModelSerializer):
#     replies = RecursiveCommentSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Comment
#         fields = ('id', 'text', 'replies', 'user', 'survey')
#
#     def get_replies(self, obj):
#         if obj.parent_comment:
#             serializer = RecursiveCommentSerializer(obj)
#             return serializer.data
#         else:
#             replies = Comment.objects.filter(parent_comment=obj)
#             serializer = GetSurveyCommentApiSerializer(replies, many=True)
#             return serializer.data


class CreateSurveyCommentApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, data):
        text = data.get('text')
        parent_comment = data.get('parent_comment')
        survey = data.get('survey')
        user = data.get('user')

        exists_comment = Comment.objects.filter(parent_comment=parent_comment, survey=survey, user=user)
        if exists_comment:
            raise serializers.ValidationError("Your comment is already exists.")

        # Проверка на наличие комментария
        # if not text:
        #     raise serializers.ValidationError("Комментарий не может быть пустым.")

        # Другие проверки, которые вы хотите добавить

        return data

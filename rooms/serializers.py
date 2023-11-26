from rest_framework import serializers
from members.models import GroupRoomMember
from .models import GroupRoom


class GroupRoomSerializer(serializers.ModelSerializer):
    """
    GroupRoomSerializer is a GroupRoom model serializer
    """

    number_of_participants = serializers.SerializerMethodField()

    class Meta:
        """
        Provides metadata and configuration options for the GroupRoomSerializer model.
        """

        model = GroupRoom
        fields = ['id', 'name', 'picture_path', 'description', 'number_of_participants',
                  'last_activity', 'created_at',]
        extra_kwargs = {
            'picture_path': {'read_only': True}
        }

    def get_number_of_participants(self, obj):
        """
        return number of participants in group room
        """

        return GroupRoomMember.objects.filter(user=obj.user).count()

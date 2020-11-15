from rest_framework import serializers

from facebook_auth.models import DebugToken, TokenMetadata, Profile, Picture, FacebookError


class MetadataSerializer(serializers.Serializer):
    auth_type = serializers.CharField()
    sso = serializers.CharField()


class DebugTokenSerializer(serializers.Serializer):
    app_id = serializers.CharField()
    user_id = serializers.CharField()
    type = serializers.CharField()
    application = serializers.CharField()
    data_access_expires_at = serializers.IntegerField()
    expires_at = serializers.IntegerField()
    is_valid = serializers.BooleanField()
    scopes = serializers.ListSerializer(child=serializers.CharField())
    metadata = MetadataSerializer(required=False)


class DebugContainerSerializer(serializers.Serializer):
    data = DebugTokenSerializer()

    def create(self, validated_data):
        data = validated_data.pop('data')
        metadata_data = data.pop('metadata', None)
        if metadata_data:
            metadata = TokenMetadata(**metadata_data)
            return DebugToken(metadata=metadata, **data)
        else:
            return DebugToken(**data)


class PictureSerializer(serializers.Serializer):
    url = serializers.URLField()


class PictureDataSerializer(serializers.Serializer):
    data = PictureSerializer()


class ProfileSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    picture = PictureDataSerializer()

    def create(self, validated_data):
        picture_data = validated_data.pop('picture').pop('data')
        picture = Picture(**picture_data)
        return Profile(picture=picture, **validated_data)


class FacebookErrorSerializer(serializers.Serializer):
    message = serializers.CharField()
    type = serializers.CharField()
    code = serializers.IntegerField()
    fbtrace_id = serializers.CharField()


class FacebookErrorContainerSerializer(serializers.Serializer):
    error = FacebookErrorSerializer()

    def create(self, validated_data):
        error_data = validated_data.pop('error')
        return FacebookError(**error_data)

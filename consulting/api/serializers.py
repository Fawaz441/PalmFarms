from rest_framework.serializers import ModelSerializer, ListField
from consulting.models import Consultant, ConsultantFile


class ConsultantFileSerializer(ModelSerializer):
    class Meta:
        model = ConsultantFile
        fields = ["file"]


class ConsultantRegisterSerializer(ModelSerializer):
    # files = ConsultantFileSerializer(many=True)

    class Meta:
        model = Consultant
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            # "linkedin_url",
            # "cv",
            # "files"
        ]

    def create_consultant(self, validated_data):
        # files = validated_data.pop("files")
        new_consultant = Consultant.objects.create(
            **validated_data
        )

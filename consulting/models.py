from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


def consultant_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'consultants/{0}-{1}/{2}'.format(instance.consultant.id, instance.consultant.full_name, filename)


class Consultant(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = PhoneNumberField()
    linkedin_url = models.URLField(null=True, blank=True)
    cv = models.FileField()

    def __str__(self):
        return self.first_name


class ConsultantFile(models.Model):
    file = models.FileField(upload_to=consultant_file_directory_path)
    consultant = models.ForeignKey(
        Consultant, on_delete=models.CASCADE, related_name="files")

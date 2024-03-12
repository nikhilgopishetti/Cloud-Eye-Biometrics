from django.db import models
import os
from django.contrib.auth.models import User


class AbnormalBehavior(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    keyboard_abnormality = models.IntegerField(default=0)
    mouse_abnormality = models.IntegerField(default=0)


def upload_path(instance, filename):
    # Get the filename and extension
    filename, ext = os.path.splitext(filename)
    # Construct the path relative to MEDIA_ROOT
    return 'images/{0}/{1}{2}'.format(instance.id, filename, ext)


class ImageModel(models.Model):
    image = models.ImageField(upload_to=upload_path, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Convert image to PNG format if needed
        if self.image:
            if not self.image.name.endswith('.png'):
                # Convert image to PNG format
                from PIL import Image
                import io
                img = Image.open(self.image)
                with io.BytesIO() as buffer:
                    img.save(buffer, format="PNG")
                    buffer.seek(0)
                    self.image.file = buffer
                    self.image.name = self.image.name.replace('.jpg', '.png')
        super(ImageModel, self).save(*args, **kwargs)

class UserPassphrase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expected_passphrase = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

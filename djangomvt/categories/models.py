from django.db import models
import os
import uuid
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image

def category_image_upload_to(instance, filename):
    ext = 'webp'
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('images', filename)

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updates_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            #img = img.convert("RGB")
            buffer = BytesIO()
            img.save(buffer, format="WEBP")
            self.image.save(f"{uuid.uuid4().hex}.webp", ContentFile(buffer.getvalue()), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
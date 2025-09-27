import os
import uuid
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

def category_image_upload_to(instance, filename):
    ext = 'webp'
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('images', filename)

def convert_image_to_webp(image_field):
    img = Image.open(image_field)
    #img = img.convert("RGB")
    buffer = BytesIO()
    img.save(buffer, format="WEBP")
    return ContentFile(buffer.getvalue(), name=f"{uuid.uuid4().hex}.webp")

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updates_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:
            orig = Category.objects.get(pk=self.pk)
            if self.image != orig.image and self.image:
                self.image = convert_image_to_webp(self.image)
        else:
            if self.image:
                self.image = convert_image_to_webp(self.image)
        
        if not self.slug:
            base_slug = slugify(unidecode(self.name))
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
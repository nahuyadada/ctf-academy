# In accounts/models.py
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    # You can store a Font Awesome class for the icon
    icon_class = models.CharField(max_length=50, default='fa-solid fa-shield-halved')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Challenge(models.Model):
    class Difficulty(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'
        EXPERT = 'expert', 'Expert'

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='challenges')
    title = models.CharField(max_length=200)
    description = models.TextField()
    points = models.IntegerField()
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices, default=Difficulty.BEGINNER)
    
    # To track completions (Many-to-Many with the User model)
    completed_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='completed_challenges', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Creates a URL for each specific challenge
        # NOTE: You will need to create this 'challenge_detail' URL later
        return reverse('challenge_detail', args=[str(self.id)])
    

class UserProfile(models.Model):
    """
    Extended user profile linked to Django's built-in User model.
    Stores additional user information such as a base64-encoded image.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        help_text="The user account that owns this profile."
    )

    image_data = models.BinaryField(
        blank=True,
        null=True,
        help_text="Base64-encoded profile image stored as binary data."
    )

    bio = models.TextField(
        blank=True,
        help_text="Optional short bio or description."
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the profile was last updated."
    )

    def __str__(self):
        return f"Profile of {self.user.username}"

    def set_base64_image(self, base64_str: str):
        """
        Store a base64-encoded image string as binary data.
        """
        import base64
        self.image_data = base64.b64decode(base64_str)

    def get_base64_image(self) -> str | None:
        """
        Return the image as a base64-encoded string, or None if empty.
        """
        import base64
        if self.image_data:
            return base64.b64encode(self.image_data).decode('utf-8')
        return None
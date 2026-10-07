from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models
from django.db.models import Q, F
from django.core.validators import MinValueValidator, MaxValueValidator

class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['city_name', 'state'],
                name='unique_city_state'
            )
        ]

    def __str__(self):
        return f'{self.city_name}, {self.state}'

class Interest(models.Model):
    interest_id = models.AutoField(primary_key=True)
    interest_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.interest_name

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]
    username = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    profile_id = models.AutoField(primary_key=True)
    profile_picture = models.ImageField(upload_to='profile_picture/',null=True,blank=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(18),
            MaxValueValidator(100)
        ]
    )
    bio = models.TextField(blank=True)
    profession = models.CharField(max_length=100)
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        related_name='profiles'
    )
    interests = models.ManyToManyField(
        Interest,
        related_name='profiles',
        blank=True
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

class Like(models.Model):
    sender = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='likes_sent'
    )
    receiver = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='likes_received'
    )
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sender', 'receiver'],
                name='unique_profile_like'
            ),
            models.CheckConstraint(
                condition=~Q(sender=F('receiver')),
                name='prevent_self_like'
            )
        ]

    def __str__(self):
        return f'{self.sender} likes {self.receiver}'

class Match(models.Model):
    first_user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='matches_as_first'
    )
    second_user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='matches_as_second'
    )
    matched_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['first_user', 'second_user'],
                name='unique_match'
            ),
            models.CheckConstraint(
                condition=~Q(first_user=F('second_user')),
                name='prevent_self_match'
            )
        ]

    def __str__(self):
        return f'{self.first_user} ❤️ {self.second_user}'

class Message(models.Model):
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='messages_sent'
    )
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender}: {self.message[:30]}'

class Block(models.Model):
    blocker = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='blocked_profiles'
    )
    blocked_user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='blocked_by_profiles'
    )
    blocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['blocker', 'blocked_user'],
                name='unique_profile_block'
            ),
            models.CheckConstraint(
                condition=~Q(blocker=F('blocked_user')),
                name='prevent_self_block'
            )
        ]

    def __str__(self):
        return f'{self.blocker} blocked {self.blocked_user}'

class PassUser(models.Model):
    who = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='passes_sent'
    )

    whom = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='passes_received'
    )

    passed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['who', 'whom'],
                name='unique_profile_pass'
            ),
            models.CheckConstraint(
                condition=~Q(who=F('whom')),
                name='prevent_self_pass'
            )
        ]

    def __str__(self):
        return f'{self.who} passed {self.whom}'

#
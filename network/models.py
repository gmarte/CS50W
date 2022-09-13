from datetime import date, datetime
from dateutil import relativedelta
from statistics import mode
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass
    following = models.ManyToManyField(
        "self", blank=True, related_name='followers', symmetrical=False)

    def __str__(self):
        return f"{self.username}"

    @property
    def count_followers(self):
        return self.followers.count()

    @property
    def count_following(self):
        return self.following.count()


class Post(models.Model):
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="post_likes")

    def __str__(self):
        return self.description + ' >> ' + str(self.creator) + ' >> ' + self.timestamp.strftime("%b %d %Y, %I:%M %p")

    @property
    def time_passed(self):
        # Timezone info of your timezone aware variable
        timezone = self.timestamp.tzinfo
        now = datetime.now(timezone)
        delta = relativedelta.relativedelta(now, self.timestamp)
        print(delta)
        if delta.years > 0:
            output = f"{delta.years} Years, {delta.months} months, {delta.days} days ago"
        elif delta.months > 0:
            output = f"{delta.months} months, {delta.days} days ago"
        elif delta.days > 0:
            output = f"{delta.days} days, {delta.minutes} minutes ago"
        else:
            output = f"{delta.minutes} minutes ago"
        return output

    class Meta:
        ordering = ['-timestamp']

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "creator": self.creator,
            "likes": self.post_likes.count()
        }

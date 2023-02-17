from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse

# Create your models here.

LIGHT_CHOICES = (
    ('LL', 'lightful/direct sun'),
    ('L', 'light'),
    ('M', 'midshadow'),
    ('S', 'shadow'),
)


GROUND = (
    ('E', 'epiphyte'),
    ('L', 'litophyte'),
    ('T', 'terrestrial')
)

MEDIUM = (
    ('B', 'bark'),
    ('S', 'sfagnus'),
    ('P', 'peat'),
)

POT_TYPE = (
    ('R', 'raft'),
    ('P', 'plastic pot'),
    ('G', 'translucent pot'),
    ('T', 'terracotta pot'),
)

BLOOM = (
    ('A', 'autumn'),
    ('AW', 'autumn-winter'),
    ('W', 'winter'),
    ('WP', 'winter-spring'),
    ('P', 'spring'),
    ('PS', 'spring-summer'),
    ('S', 'summer'),
    ('SA', 'summer-autumn'),
    ('R', 'reblooming'),
)

class OrchidGenre(models.Model):
    genre = models.CharField(max_length=25, primary_key=True)
    description = models.TextField(max_length=100)
    winter_range = models.CharField(max_length=5)
    summer_range = models.CharField(max_length=5)
    light = models.CharField(max_length=2, choices=LIGHT_CHOICES)
    humidity = models.PositiveSmallIntegerField()
    ground = models.CharField(max_length=1, choices=GROUND)
    bloom = models.CharField(max_length=2, choices=BLOOM)
    image = models.ImageField(upload_to="genres/", null=True, blank=True)
    
    def __str__(self):
        return self.genre
    
    def get_absolute_url(self):
        return reverse('genre_detail', args=[self.genre])

class OrchidVariety(models.Model):
    genre = models.ForeignKey(OrchidGenre, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    is_bothanic = models.BooleanField(default=False)
    hybrid_ancestors = models.CharField(max_length=70, null=True, blank=True)

    #these fields are individual but can be copied from the genre
    description = models.TextField(max_length=100, null=True, blank=True)
    winter_range = models.CharField(max_length=5, null=True, blank=True)
    summer_range = models.CharField(max_length=5, null=True, blank=True)
    light = models.CharField(max_length=2, choices=LIGHT_CHOICES, null=True, blank=True)
    humidity = models.PositiveSmallIntegerField(null=True, blank=True)
    ground = models.CharField(max_length=1, choices=GROUND, null=True, blank=True)
    bloom = models.CharField(max_length=2, choices=BLOOM, null=True, blank=True)
    image = models.ImageField(upload_to="varieties/", null=True, blank=True)

    def __str__(self):
        return f"{self.genre} {self.name}"

    def get_absolute_url(self):
        return reverse('variety_detail', args=[int(self.pk)])

class OrchidInstance(models.Model):
    variety = models.ForeignKey(OrchidVariety, on_delete=models.CASCADE, null=True, blank=True)
    pot_type = models.CharField(max_length=1, choices=POT_TYPE)
    pot_size = models.PositiveSmallIntegerField()
    medium = models.CharField(max_length=1, choices=MEDIUM)
    image = models.ImageField(upload_to="instances/", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.variety} {self.pk}"
    
    def get_absolute_url(self):
        return reverse('instance_detail', args=[int(self.pk)])
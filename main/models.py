from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Team(models.Model):
    team_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="tracks/", default="default.png")
    points = models.IntegerField(default=0)
    

    def __str__(self):
        return self.team_name


class Driver(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="tracks/", default="default.png")
    nationality = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    image_team = models.ImageField(upload_to="tracks/", default="default.png")
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Race(models.Model):
    name = models.CharField(max_length=100)
    date_start = models.DateField()
    date_end = models.DateField()
    image = models.ImageField(upload_to="tracks/")
    round_number = models.PositiveIntegerField(default=1)


    class Status(models.TextChoices):
        COMPLETED = "completed", "Completed"
        NEXT = "next", "Next Race"
        UPCOMING = "upcoming", "Upcoming"

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPCOMING)

    def __str__(self):
        return self.name 
    

class FastetLap(models.Model):
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    lap = models.IntegerField(default=0)
    image = models.ImageField(upload_to="tracks/")

    def __str__(self):
        return self.name 

class PolePossition(models.Model):
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    pole = models.IntegerField(default=0)
    image = models.ImageField(upload_to="tracks/")

    def __str__(self):
        return self.name 

class Podiums(models.Model):
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    podiums = models.IntegerField(default=0)

    def __str__(self):
        return self.name 
    
class DNF(models.Model):
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    dnf = models.IntegerField(default=0)

    def __str__(self):
        return self.name 
    
class AboutTeams(models.Model):
    name = models.CharField(max_length=100)
    driver1_name = models.CharField(max_length=100, null=True, blank=True)
    driver2_name = models.CharField(max_length=100, null=True, blank=True)
    driver1_number = models.IntegerField(default=0)
    driver2_number = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='teams/logos/')
    car_image = models.FileField(upload_to='teams/cars/')
    driver1_image = models.FileField(upload_to='teams/drivers/', default="default.png")
    driver2_image = models.FileField(upload_to='teams/drivers/', default="default.png")
    color_class = models.CharField(max_length=50)

    def __str__(self):
        return self.name 
    
class Statistics(models.Model):
    team = models.OneToOneField(AboutTeams, on_delete=models.CASCADE, related_name="stats") 
    season_position = models.IntegerField(default=0)
    prix_races = models.IntegerField(default=0)
    prix_wins = models.IntegerField(default=0)
    dhl = models.IntegerField(default=0)
    sprint_races = models.IntegerField(default=0)
    sprint_wins = models.IntegerField(default=0)
    sprint_poles = models.IntegerField(default=0)
    season_oints = models.IntegerField(default=0)
    prix_points = models.IntegerField(default=0)
    prix_podiums = models.IntegerField(default=0)
    top = models.IntegerField(default=0)
    dnfs = models.IntegerField(default=0)
    
    def __str__(self):
        return self.team.name
    
class AboutDriver(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    team = models.ForeignKey(AboutTeams, on_delete=models.SET_NULL, null=True, related_name="drivers")
    birthday = models.DateField()
    nationality = models.CharField(max_length=100)
    driver_number = models.IntegerField(default=0)
    place_of_birth = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField(upload_to="drivers/", default="default_driver.png")
    driver_image = models.FileField(upload_to="drivers/", blank=True, null=True)
    color_class = models.CharField(max_length=50, default='default-bg')

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(self.name)
            self.slug = original_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Career(models.Model):
    driver = models.ForeignKey('AboutDriver', on_delete=models.CASCADE, related_name='careers')
    team = models.ForeignKey('AboutTeams', on_delete=models.SET_NULL, null=True, related_name="career_set")
    championships_current = models.IntegerField(default=0)
    championships_max = models.IntegerField(default=11)
    wins_current = models.IntegerField(default=0)
    wins_max = models.IntegerField(default=0)
    podiums_current = models.IntegerField(default=0)
    podiums_max = models.IntegerField(default=0)
    poles_current = models.IntegerField(default=0)
    poles_max = models.IntegerField(default=0)
    starts = models.IntegerField(default=0)
    fastest_laps = models.IntegerField(default=0)
    best_finish = models.IntegerField(default=0)
    best_grid = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    retirements = models.IntegerField(default=0)
    color_class = models.CharField(max_length=50, default='default-bg')

    def __str__(self):
        return f"{self.driver.name} – {self.team.name if self.team else ''}"
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    favorite_team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)
    favorite_driver = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL)
    country = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.user.username
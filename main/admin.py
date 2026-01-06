from django.contrib import admin
from .models import Team, Driver, Race, Podiums, PolePossition, DNF, FastetLap, AboutTeams, Statistics, AboutDriver, Career, Profile

admin.site.register(Team)
admin.site.register(Driver)
admin.site.register(Race)
admin.site.register(Podiums)
admin.site.register(PolePossition)
admin.site.register(DNF)
admin.site.register(FastetLap)
admin.site.register(AboutTeams)
admin.site.register(Statistics)
admin.site.register(AboutDriver)
admin.site.register(Career)
admin.site.register(Profile)
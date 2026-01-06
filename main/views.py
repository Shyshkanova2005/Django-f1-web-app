from django.shortcuts import render, get_object_or_404, redirect
from .models import Team, Driver, Race, Podiums, PolePossition, FastetLap, DNF, AboutTeams, Statistics, AboutDriver, Profile
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from datetime import date
import pandas as pd


def index(request):
    drivers = Driver.objects.all().order_by('-points')  
    teams = Team.objects.all().order_by('-points')     

    races = Race.objects.order_by("round_number")
    today = date.today()

    next_race = None

    for race in races:
        if race.date_end < today:
            race.status = "completed"
        elif race.date_start > today and next_race is None:
            race.status = "next"
            next_race = race
        else:
            race.status = "upcoming"

    context = {
        'drivers': drivers,
        'teams': teams,
        'races': races,
    }

    return render(request, 'main/main.html', context)

def teams(request):
    return render(request, 'main/teams.html')

def team_detail(request, team_slug):
    team = get_object_or_404(AboutTeams, slug=team_slug)
    stats = team.stats
    driver1 = AboutDriver.objects.filter(name=team.driver1_name).first()
    driver2 = AboutDriver.objects.filter(name=team.driver2_name).first()   
    return render(request, 'main/about_teams.html', {'team': team, "stats": stats, 'driver1': driver1, 'driver2': driver2})

def driver_detail(request, driver_slug):
    driver = get_object_or_404(AboutDriver, slug=driver_slug)
    career = driver.careers.first()
    def calc_percentage(current, maximum):
        if maximum == 0:
            return 0
        return round((current / maximum) * 100, 2)

    stats = {
        'championships': {
            'label': 'Championships',
            'current': career.championships_current,
            'max': career.championships_max,
            'percent': calc_percentage(career.championships_current, career.championships_max),
        },
        'wins': {
            'label': 'Wins',
            'current': career.wins_current,
            'max': career.wins_max,
            'percent': calc_percentage(career.wins_current, career.wins_max),
        },
        'podiums': {
            'label': 'Podiums',
            'current': career.podiums_current,
            'max': career.podiums_max,
            'percent': calc_percentage(career.podiums_current, career.podiums_max),
        },
        'poles': {
            'label': 'Poles',
            'current': career.poles_current,
            'max': career.poles_max,
            'percent': calc_percentage(career.poles_current, career.poles_max),
        },
    }

    return render(request, "main/about_drivers.html", {
        "driver": driver,
        "career": career,
        "stats": stats,
    })

def circuits(request):
    return render(request, 'main/circuits.html')

def statistics(request):
    fastest = FastetLap.objects.all().order_by('-lap')
    pole = PolePossition.objects.all().order_by('-pole')
    podium = Podiums.objects.all().order_by('-podiums')
    dnf = DNF.objects.all().order_by('-dnf')

    fastest_data = {
        'labels': [d.name for d in fastest],
        'laps': [int(d.lap) for d in fastest]
    }

    pole_data = {
    'labels': [p.name for p in pole],
    'poles': [p.pole for p in pole]
    }

    podium_data = {
        'labels': [p.name for p in podium],
        'podiums': [p.podiums for p in podium]
    }

    dnf_data = {
    'labels': [d.name for d in dnf],
    'dnf': [d.dnf for d in dnf]
    }
    df = pd.read_csv('main/data/F1_2025_RaceResults.csv', sep=';')

    track_order = {track: i+1 for i, track in enumerate(df['Track'].unique())}
    df['Round'] = df['Track'].map(track_order)

    df['Points'] = pd.to_numeric(df['Points'], errors='coerce').fillna(0)
    df = df.sort_values(['Driver', 'Round'])
    df['Cumulative'] = df.groupby('Driver')['Points'].cumsum()

    pivot = df.pivot(index='Round', columns='Driver', values='Cumulative').ffill().fillna(0)

    all_rounds = list(range(1, 25))

    pivot = pivot.reindex(all_rounds, fill_value=None).ffill().fillna(0)

    rounds = pivot.index.tolist()
    drivers = pivot.columns.tolist()
    data = {d: pivot[d].tolist() for d in drivers}

    return render(request, 'main/statistics.html', {
        "fastest": fastest,
        "pole": pole,
        "podium": podium,
        "dnf": dnf,
        "fastest_data": fastest_data, 
        "pole_data" : pole_data,
        "podium_data": podium_data,
        "dnf_data": dnf_data,
        "rounds": rounds,
        "drivers": drivers,
        "data": data
    })

def authorize(request):
    if request.user.is_authenticated:
        return redirect("index")
     
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "main/authorize.html", {
                "error": "Incorrect login or password"
            })
        
    return render(request, "main/authorize.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        if User.objects.filter(username=username).exists():
            return render(request, "main/register.html", {
                "error": "User already exists"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        Profile.objects.create(user=user)

        return redirect("authorize")

    return render(request, "main/register.html")

@require_POST
def logout(request):
    auth_logout(request)
    return redirect("authorize")

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    context = {
        "profile": profile,
    }
    return render(request, "main/profile.html", context)

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        profile.country = request.POST.get("country")
        profile.favorite_team_id = request.POST.get("favorite_team") or None
        profile.favorite_driver_id = request.POST.get("favorite_driver") or None

        if request.FILES.get("avatar"):
            profile.avatar = request.FILES["avatar"]

        email = request.POST.get("email")
        if email:
            request.user.email = email

        username = request.POST.get("username")
        if username:
            request.user.username = username

        request.user.save()
        profile.save()

        return redirect("profile")

    return render(request, "main/edit_profile.html", {
        "profile": profile,
        "teams": Team.objects.all(),
        "drivers": Driver.objects.all(),
    })

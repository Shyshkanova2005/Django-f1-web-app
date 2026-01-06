from .models import Profile

def profile_processor(request):
    if request.user.is_authenticated:
        try:
            return {
                'profile': Profile.objects.get(user=request.user)
            }
        except Profile.DoesNotExist:
            return {}
    return {}

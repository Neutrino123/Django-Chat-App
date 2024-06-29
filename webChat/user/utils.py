from .models import Profile
from django.db.models import Q

def search(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    print(search_query)
    profiles = Profile.objects.filter(
    Q(username__icontains=search_query) & ~Q(user=request.user)
)
    return search_query, profiles
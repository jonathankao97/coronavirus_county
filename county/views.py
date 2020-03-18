from django.shortcuts import render

from county.models import City, County

def test(request):
    return render(request, 'test.html')


def search(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    cities = City.objects.filter(name__startswith=search_text)

    counties = set()
    if len(search_text) >= 3:
        for city in cities:
            if city.county not in counties:
                counties.add(city.county)
            if len(counties) == 5:
                break
    print(search_text)
    print(counties)
    return render(request, 'ajax_search.html', {'counties': counties})


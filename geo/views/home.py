from django.shortcuts import render, get_object_or_404


def home_view(request):
    context = {
        'data': [
            [
                {
                    'title': 'Polling Stations',
                    'url': '/geo/stations',
                    'details': 'Manage polling stations',
                },
                            {
                    'title': 'Nation',
                    'url': '/geo/nations',
                    'details': 'Manage nation details',
                },
            ],
            [
                {
                    'title': 'Constituencies',
                    'url': '/geo/constituencies',
                    'details': 'Manage constituencies',
                },
            ],
            [
                {
                    'title': 'Regions',
                    'url': '/geo/regions',
                    'details': 'Manage regions',
                },
            ],
        ],
    }
    return render(request, "geo/home.html", context)

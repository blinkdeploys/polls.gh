from django.shortcuts import render, get_object_or_404


def index_view(request):
    context = {
        'data': [
            [
                {
                    'title': 'Collate Results',
                    'details': 'Enter election results from polling stations.',
                    'url': '/poll/results/',
                },
                {
                    'title': 'Approve Results',
                    'details': 'Approve and publish election results at polling stations, aggregated results from constituencies, regional and national.',
                    'url': '/poll/result_approvals/',
                },
                {
                    'title': 'View Reports',
                    'details': 'View election results from collated results at all levels (constituencies, regional and national).',
                    'url': '#',
                },
            ],
            [
                {
                    'title': 'Review Agents',
                    'details': 'Review all party agents at all levels.',
                    'url': '/people/agents',
                },
                {
                    'title': 'Review Candidates',
                    'details': 'Ensure that all candidates are present and accounted for all locations and political parties.',
                    'url': '/people/candidates',
                },
                {
                    'title': 'Review Election Events',
                    'details': 'Update election dates and events',
                    'url': '#',
                },
            ],
            [
                {
                    'title': 'Location Setup',
                    'details': 'Validate all election locations (regions, constituencies and polling stations).',
                    'url': '/geo'
                }
            ],
        ],
    }
    return render(request, "home.html", context)

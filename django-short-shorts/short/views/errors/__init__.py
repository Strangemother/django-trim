from django.shortcuts import render


def handler404(request, exception):
    # page_not_found_view
    return render(request, "short/errors/404.html", { 'status_code': 404})


def handler500(request, exception=None):
    # error_view
    return render(request, "short/errors/500.html", { 'status_code': 500})


def handler403(request, exception=None):
    # permission_denied_view
    return render(request, "short/errors/403.html", { 'status_code': 403})


def handler400(request, exception=None):
    # bad_request_view
    return render(request, "short/errors/400.html", { 'status_code': 400})

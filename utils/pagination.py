import math
from django.core.paginator import Paginator


def make_pagination_range(page_range,  qt_pages, current_page):
    middle_range = math.ceil(qt_pages / 2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)

    first_page_out_of_range = current_page > middle_range
    last_page_out_of_range = stop_range < total_pages

    if len(page_range[start_range:stop_range]) > qt_pages - 1:
        pagination = page_range[start_range:stop_range]
    else:
        pagination = page_range[0:qt_pages]
        first_page_out_of_range = False
        last_page_out_of_range = False

    return {
        'pagination': pagination,
        'page_range': page_range,
        'qt_pages': qt_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': first_page_out_of_range,
        'last_page_out_of_range': last_page_out_of_range
    }


def make_pagination(request, queryset, per_page=9, qt_pages=4):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        qt_pages,
        current_page
    )

    return page_obj, pagination_range

from deno_sandbox.api_types_generated import PaginatedList


def convert_paginated_list_response(response, item_converter):
    items = [item_converter.from_dict(item) for item in response.items]
    return PaginatedList(
        items=items,
        total_count=response.total_count,
        next_page_token=response.next_page_token,
    )

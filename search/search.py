from flask import render_template, Blueprint, request, flash
from search.utils import geo_code
from urllib import parse


bp = Blueprint(
    "search", __name__,
    template_folder="templates", static_folder="static",
    url_prefix="/search"
)

@bp.route("")
def result() -> str:
    """Return search result view based on query parameters."""
    query = request.args
    address = query.get("address", None)

    context = {
        "address": address,
        "found": False,
        "searched": False
    }

    if address:
        parsed_address = parse.quote_plus(address)
        context = geo_code(parsed_address)
        context["address"] = address
        context["parsed_address"] = parsed_address


    return render_template("/search/result.html", context=context)

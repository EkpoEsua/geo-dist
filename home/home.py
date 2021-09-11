from flask import render_template, Blueprint

bp = Blueprint(
    "home", __name__,
    template_folder="templates", static_folder="static",
    url_prefix="/"
)

@bp.route("/")
def index() -> str:
    """Return view for the home page of the app."""
    return render_template("/home/home.html")
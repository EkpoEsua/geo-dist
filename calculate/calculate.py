from os import error
from flask import render_template, Blueprint, current_app, request
from calculate.utils import calculate_distance


bp = Blueprint(
    "calculate", __name__,
    template_folder="templates", static_folder="static",
    url_prefix="/calculate"
)

app = current_app

@bp.route("")
def calculate() -> str:
    """Return a view containing the distance between the input latittude and longitude 
    location and the Moscow Ring Road, from the it's centre coordinate point.
    """
    query = request.args
    latitude = query.get("lat", None)
    longitude = query.get("lon", None)
    name = query.get("name", None)

    context = {
        "distance": 0,
        "success": False,
        "longitude": longitude,
        "latitude": latitude,
        "name": name
    }

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (ValueError, TypeError):
        pass        
    else:
        if ((latitude <= 90) and (latitude >= -90) 
                and (longitude <= 180) and (longitude >= -180)):
            distance = calculate_distance(latitude=latitude, longitude=longitude)
            context["distance"] = distance
            context["success"] = True
            if distance != -1:
                part_message  = context["name"] or f"Lat: {context['latitude']} | "\
                    f"Lon: {context['longitude']} "
                full_message = (
                    "Distance from "
                    + part_message
                    + "to Moscow Ring Road: "
                    + str(distance)
                    + "km ."
                )
                app.logger.info(full_message)
        else:
            pass


    return render_template("/calculate/calculate.html", context=context)
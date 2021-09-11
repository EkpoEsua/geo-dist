# GeoDist

A web app written in Flask; finds the distance in kilometres between a searched location, and Moscow Ring Road (center).
It makes use of [Yandex Geocode API](https://yandex.com/dev/maps/geocoder/doc/desc/concepts/about.html) to get the coordinates of a searched address.

It works by:
* Accepting a string address to be searched.
* Makes a request to the Yandex Geocode API to retrive results that matched the search; their addresses and coordinates.
* Based on the returned results, can calculate the geodesic distance from Moscow Ring Road for the selected specific address coordinates using the [geopy library](https://geopy.readthedocs.io/en/latest/#module-geopy.distance).

Also the given a known valid latitude and longitude coordinates, the distance from Moscow Ring Road can be computed.

# Installing the app locally.
In order to use the app, ensure at least `python3 version 3.8.10` is available locally:

* Clone the repository: `git clone https://github.com/EkpoEsua/geo-dist.git`

* Change directory: `cd geo-dist/`

* Run the setup/start script: `./start.sh`

* Open [localhost](http://127.0.0.1:5000/) on a browser.
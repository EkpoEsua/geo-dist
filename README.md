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

# Run as container locally.
To run as a container, ensure [docker](https://docs.docker.com/get-docker/) is set up.

* run `docker run -dp 5000:5000 --name bluekale esuaekpo/geo-dist:alpine`

* Open [localhost](http://127.0.0.1:5000/) on a browser.


# Run as container online with PWD

* Go to [Play with Docker](https://labs.play-with-docker.com/).

* Click Login and then select docker from the drop-down list.

* Connect with your Docker Hub account.

* Once you’re logged in, click on the ADD NEW INSTANCE option on the left side bar. If you don’t see it, make your browser a little wider. After a few seconds, a terminal window opens in your browser.

![PWD screenshot](https://docs.docker.com/get-started/images/pwd-add-new-instance.png)

* In the terminal, start the app.

    `docker run -dp 5000:5000 --name bluekale esuaekpo/geo-dist:alpine`

* Click on the 5000 badge when it comes up and you should see the app, If the 5000 badge doesn’t show up, you can click on the “Open Port” button and type in 5000.

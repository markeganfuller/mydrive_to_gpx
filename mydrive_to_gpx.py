#!/usr/bin/env python3

import datetime
import sys
import json

import gpxpy


def tomtom_to_gpx(place):
    """Convert tomtom place to GPXWaypoint."""
    # Its a Java timestamp with extra digits
    time = place['value']['favoritesInterop']['creation'] // 1000
    gpx_waypoint = gpxpy.gpx.GPXWaypoint(
        latitude=place['value']['location']['pointPosition']['latitude'],
        longitude=place['value']['location']['pointPosition']['longitude'],
        time=datetime.datetime.fromtimestamp(time),
        name=place['value']['metadata']['name']
    )
    return gpx_waypoint


def extract(input_filename, output_filename):
    """Extract tomtom places and output to GPX."""
    with open(input_filename) as input_file:
        mydrive = json.load(input_file)

    gpx = gpxpy.gpx.GPX()
    for key in mydrive["stores"]:
        for place in mydrive["stores"][key].values():
            try:
                gpx.waypoints.append(tomtom_to_gpx(place))
            except KeyError:
                print(f"Failed to transfer: {place}")

    with open(output_filename, 'w') as output_file:
        output_file.write(gpx.to_xml())

    print(f"Wrote {len(gpx.waypoints)} waypoints")


if __name__ == "__main__":
    extract(sys.argv[1], sys.argv[2])

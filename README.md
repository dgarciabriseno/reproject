# Reproject

This is a microservice which reprojects Helioviewer images to different observers.
It uses [sunpy](https://docs.sunpy.org/en/stable/generated/gallery/map_transformations/reprojection_different_observers.html)
to perform the reprojection, and returns a reprojected jp2 image.

The observer's position is determined via JPL Horizons ephemeris data, as processed by sunpy's [`get_horizons_coord`](https://docs.sunpy.org/en/stable/generated/api/sunpy.coordinates.get_horizons_coord.html#get-horizons-coord)

## Usage

The container runs an http service with only one endpoint:
`/<int:id>/<string:observer>` where the ID is the Helioviewer image ID, and the observer is the desired observer.

| Parameters | Description          |
|------------|----------------------|
| id         | Helioviewer Image ID |
| observer   | Target observer      |

### Example
The URL `localhost:8000/154521956/STEREO-A` would take the image 154521956 (an AIA 304 image) and return
a new jpeg2000 image which is the same AIA 304 image as seen by STEREO-A at the same point in time the image was taken.

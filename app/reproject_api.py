"""
Demo of a reprojection API
"""

import os
import tempfile

from flask import Flask, send_file
from sunpy.util import MetaDict
from astropy.time.core import Time
from astropy.coordinates import SkyCoord
from astropy.units.quantity import Quantity
from sunpy.map.mapbase import SpatialPair
import astropy.units as u
from sunpy.map import Map, make_fitswcs_header, GenericMap
from sunpy.coordinates.ephemeris import get_horizons_coord
import requests

app = Flask(__name__)

def make_reprojection_header(observer: str, shape: tuple, date: Time, rsun: Quantity, scale: SpatialPair) -> MetaDict:
    """
    Creates a FITS header representing the desired observer
    The resulting header can be used to reproject a source Map
    """
    # TODO: Handle the case where the observer is invalid
    observer = get_horizons_coord(observer, date)
    observer_ref_coord = SkyCoord(0*u.arcsec, 0*u.arcsec,
                            obstime=date,
                            observer=observer,
                            rsun=rsun,
                            frame="helioprojective")
    return make_fitswcs_header(
        shape,
        observer_ref_coord,
        scale=u.Quantity(scale)
    )

def reproject_map(src: GenericMap, observer: str) -> GenericMap:
    reprojection_header = make_reprojection_header(observer, src.data.shape, src.date, src.reference_coordinate.rsun, src.scale)
    return src.reproject_to(reprojection_header)

@app.route("/<int:id>/<string:observer>")
def reproject(id, observer):
    # In Helioviewer, this could perform a database lookup to get the file from disk.
    api = os.environ["API_BASE"]
    image = requests.get(f"{api}/?action=getJP2Image&id={id}")
    fp = tempfile.NamedTemporaryFile("wb")
    fp.write(image.content)

    src = Map(fp.name)
    result = reproject_map(src, observer)

    # Using a temporary directory.
    # This directory will be deleted when tmpdir is garbage collected
    # This ensures that the usage of this API doesn't consume disk space.
    tmpdir = tempfile.TemporaryDirectory()
    outfile = os.path.join(tmpdir.name, "out.jp2")
    result.save(outfile)

    # Remove temporary file. This wouldn't be in the HV implementation since
    # it would not be working with temporary files. It would "Map" the
    # source jp2 directly.
    fp.close()
    return send_file(outfile)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)

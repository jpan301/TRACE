# source: DjangoSafe / django/contrib/gis/geos/point.py
# function: _create_point

class Point:
    def _create_point(cls, ndim, coords):
        """
        Create a coordinate sequence, set X, Y, [Z], and create point
        """
        if not ndim:
            return capi.create_point(None)

        if ndim < 2 or ndim > 3:
            raise TypeError("Invalid point dimension: %s" % ndim)

        cs = capi.create_cs(c_uint(1), c_uint(ndim))
        i = iter(coords)
        capi.cs_setx(cs, 0, next(i))
        capi.cs_sety(cs, 0, next(i))
        if ndim == 3:
            capi.cs_setz(cs, 0, next(i))

        return capi.create_point(cs)
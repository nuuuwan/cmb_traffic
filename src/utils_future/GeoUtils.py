import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon


class GeoUtils:
    @staticmethod
    def geodf_to_lnglat_lists(gdf: gpd.GeoDataFrame):
        polygons = []
        for geom in gdf.geometry:
            assert geom is not None, "Geometry is None"

            if isinstance(geom, (Polygon)):
                polygon = (
                    list(geom.exterior.coords)
                    if hasattr(geom, "exterior")
                    else list(geom.coords)
                )
                polygon = [[y, x] for x, y in polygon]
                polygons.append(polygon)

            elif isinstance(geom, (MultiPolygon)):
                for part in geom.geoms:
                    polygon = (
                        list(part.exterior.coords)
                        if hasattr(part, "exterior")
                        else list(part.coords)
                    )
                    polygons.append(polygon)

            else:
                raise TypeError("Unsupported geometry type: %s" % type(geom))

        return polygons

from dataclasses import dataclass

from utils import LatLng

from utils_future import GoogleMaps


@dataclass
class Location:
    name: str
    latlng: LatLng
    details: str

    def url(self) -> str:
        return GoogleMaps.get_url_for_point(self.latlng)

    def __eq__(self, other):
        if not isinstance(other, Location):
            return False
        return self.name == other.name and self.latlng == other.latlng

    def __lt__(self, other):
        if not isinstance(other, Location):
            return NotImplemented
        return self.name < other.name

    def __le__(self, other):
        if not isinstance(other, Location):
            return NotImplemented
        return self.name <= other.name

    def __gt__(self, other):
        if not isinstance(other, Location):
            return NotImplemented
        return self.name > other.name

    def __ge__(self, other):
        if not isinstance(other, Location):
            return NotImplemented
        return self.name >= other.name

    def __hash__(self):
        return hash((self.name, str(self.latlng)))

    def to_dict(self) -> dict:
        return dict(
            name=self.name,
            latlng=(self.latlng.lat, self.latlng.lng),
        )

    @property
    def lnglat(self) -> tuple[float, float]:
        return (self.latlng.lng, self.latlng.lat)


Location.BAMBALAPITIYA = Location(
    name="Bambalapitiya",
    latlng=LatLng(6.895572468746244, 79.85483770889027),
    details="Bambalapitiya Junction on Galle Road (Colombo 4)",
)
Location.BORELLA = Location(
    name="Borella",
    latlng=LatLng(6.910882574522934, 79.88789773709671),
    details="Ayurveda Junction on Sri Jayewardenepura Mawatha (Colombo 8)",
)
Location.DEMATAGODA = Location(
    name="Dematagoda",
    latlng=LatLng(6.943175860321491, 79.87820817923517),
    details="Southside of Dematagoda Canal Bridge, on A1/Baseline Road (Colombo 9)",
)
Location.FORT = Location(
    name="Fort",
    latlng=LatLng(6.931424355241801, 79.84220762949998),
    details="Lotus Road/Galle Face Roundabout",
)
Location.MATTAKKULIYA = Location(
    name="Mattakkuliya",
    latlng=LatLng(6.980026983331188, 79.87551282104877),
    details="Southside of Mattakkuliya Bridge, on New Negombo Road (Colombo 15)",
)
Location.PAMANKADA = Location(
    name="Pamankada",
    latlng=LatLng(6.871812810816128, 79.88456400975986),
    details="High Level Road border of CMC (Colombo 6)",
)
Location.WELLAWATTE = Location(
    name="Wellawatte",
    latlng=LatLng(6.863288956321618, 79.86360827087549),
    details="Northside of Dehiwala Bridge, on Galle Road (Colombo 6)",
)

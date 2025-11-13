from dataclasses import dataclass

from utils_future import GoogleMaps, LatLng


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
    latlng=LatLng(6.895575462912813, 79.85485123378743),
    details="Bambalapitiya Junction on Galle Road (Colombo 4)",
)
Location.BORELLA = Location(
    name="Borella",
    latlng=LatLng(6.91083821658074, 79.88785806605529),
    details="Ayurveda Junction on Sri Jayewardenepura Mawatha (Colombo 8)",
)
Location.DEMATAGODA = Location(
    name="Dematagoda",
    latlng=LatLng(6.943065393059455, 79.87826854808782),
    details="Southside of Dematagoda Canal Bridge, on A1/Baseline Road (Colombo 9)",  # noqa: E501
)
Location.FORT = Location(
    name="Fort",
    latlng=LatLng(6.931424355241801, 79.84220762949998),
    details="Lotus Road/Galle Face Roundabout (Colombo 1)",
)
Location.MATTAKKULIYA = Location(
    name="Mattakkuliya",
    latlng=LatLng(6.980032263089517, 79.87550713996588),
    details="Southside of Mattakkuliya Bridge, on New Negombo Road (Colombo 15)",  # noqa: E501
)
Location.PAMANKADA = Location(
    name="Pamankada",
    latlng=LatLng(6.871812810816128, 79.88456400975986),
    details="High Level Road border of CMC (Colombo 6)",
)
Location.WELLAWATTE = Location(
    name="Wellawatte",
    latlng=LatLng(6.863365550501378, 79.86358885114313),
    details="Northside of Dehiwala Bridge, on Galle Road (Colombo 6)",
)

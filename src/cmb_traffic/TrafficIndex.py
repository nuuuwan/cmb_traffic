from dataclasses import dataclass

from cmb_traffic.Journey import Journey


@dataclass
class TrafficIndex:
    undirected_journey_list: list[Journey]

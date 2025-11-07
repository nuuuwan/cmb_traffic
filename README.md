# Colombo Traffic Index (CTI)

A data project to build a Colombo Traffic Index (CTI) — a simple, reproducible measure of real-time and long-term traffic congestion trends in the Colombo Municipal Council (CMC) area.

## Objective

Traffic congestion in Colombo varies dramatically by time of day, day of week, and season. This project aims to quantify and monitor traffic intensity through a small but representative sample of key routes across the city, updated at regular intervals using publicly available data from Google Maps.

The resulting index can help:

- Measure trends in congestion levels
- Compare traffic conditions across time (e.g., weekdays vs. weekends, pre-holiday vs. post-holiday)
- Support policy and research on urban mobility

## Methodology

1. Select representative routes within the Colombo City area
2. Collect travel times between fixed origin–destination (O–D) pairs at defined times of day (e.g., 6 AM, 10 AM, 2 PM, 6 PM, 10 PM)
3. Normalize the travel times against their uncongested baselines (e.g., free-flow nighttime durations)
4. Compute the Colombo Traffic Index (CTI) as an aggregate congestion score across all routes

Example definition:

```
CTI_t = (1/N) * Σ(T_{i,t} / T_{i,free})
```

where:

- `T_{i,t}` = observed travel time on route i at time t
- `T_{i,free}` = minimum observed (free-flow) time on route i
- `N` = number of routes observed

## Selected Key Routes

The routes below were chosen to represent diverse travel patterns within the CMC — covering commercial, residential, and arterial corridors, and balancing north–south, east–west, and radial movements.

| No. | Route | Direction | Why This Route Matters |
|-----|-------|-----------|------------------------|
| 1 | Kollupitiya → Fort | South → North | Central business axis connecting key commercial areas; high commuter density in both directions during rush hours |
| 2 | Bambalapitiya → Borella | West → East | Links the western coastal corridor to the inner residential belt; captures cross-city flows |
| 3 | Dematagoda → Town Hall | North → South | Represents inbound traffic from northern suburbs into the city core |
| 4 | Wellawatte → Slave Island | South → North | Parallel coastal corridor capturing southern commuter inflows |
| 5 | Maradana → Pettah | East → West | Busy arterial route through dense urban core; heavy multimodal activity (bus, train, goods) |
| 6 | Narhenpita → Colombo Fort | South-East → North-West | Major commuter route connecting outer administrative area to financial hub |
| 7 | Havelock Town → Borella | South-West → North-East | Represents cross-residential traffic flow, typically moderate but increasingly congested |
| 8 | Kotahena → Kollupitiya | North → South | Reflects movement from older northern neighborhoods to central business zones |

## Data Collection Schedule

Default observation times (UTC+5:30):

- 06:00 – Morning peak
- 10:00 – Late morning
- 14:00 – Midday
- 18:00 – Evening peak
- 22:00 – Late evening

Each observation includes:

- Timestamp
- Source & destination coordinates
- Google Maps travel time (driving mode)
- Distance & estimated speed



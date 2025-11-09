# 🇱🇰 Colombo Traffic Index (cmb_traffic)

![LatestEstimateFor](https://img.shields.io/badge/latest_estimate_for-2025--11--09_15:00:00-green)

## 📊 About This Index

The Colombo Traffic Index (CTI) provides a real-time measure of traffic congestion across key routes in Colombo. By tracking average travel speeds throughout the day, this index helps:

- 🚗 **Commuters** plan their travel times and identify optimal departure windows
- 📈 **Researchers** analyze traffic patterns and urban mobility trends
- 🏛️ **Policy makers** make data-driven decisions on infrastructure and traffic management

### Methodology

We monitor a set of representative routes across Colombo City, measuring travel times and speeds at regular intervals throughout the day. Each route is monitored in both directions to capture bidirectional traffic patterns. The overall traffic condition is assessed by calculating the average speed across all monitored routes at each time point.

### Travel Time Ratio (TTR)

We also track the **Travel Time Ratio (TTR)** for each route, which measures congestion severity:

```python
TTR = Peak Hour Travel Time / Free Flow Travel Time
    = Free Flow Speed / Peak Hour Speed
```

A TTR of 1.0 indicates free-flow conditions, while higher values indicate increasing congestion. For example, a TTR of 2.0 means travel takes twice as long during peak hours compared to free-flow conditions.

Lower average speeds indicate heavier traffic congestion, while higher speeds suggest free-flow conditions. By tracking these patterns over time, we can identify peak congestion periods and seasonal trends.

## Overall Traffic Index

![images/chart_overall_traffic_index.png](images/chart_overall_traffic_index.png)

![images/chart_ttr_traffic_index.png](images/chart_ttr_traffic_index.png)

## Routes

![images/map_routes.png](images/map_routes.png)

### Bambalapitiya ↔ Borella

📍 [6.895572°N, 79.854838°E to 6.910883°N, 79.887898°E](https://www.google.com/maps/dir/6.895572,79.854838/6.910883,79.887898/)

![images/chart-bambalapitiya-to-borella.png](images/chart-bambalapitiya-to-borella.png)

### Bambalapitiya ↔ Dematagoda

📍 [6.895572°N, 79.854838°E to 6.943176°N, 79.878208°E](https://www.google.com/maps/dir/6.895572,79.854838/6.943176,79.878208/)

![images/chart-bambalapitiya-to-dematagoda.png](images/chart-bambalapitiya-to-dematagoda.png)

### Bambalapitiya ↔ Fort

📍 [6.895572°N, 79.854838°E to 6.931424°N, 79.842208°E](https://www.google.com/maps/dir/6.895572,79.854838/6.931424,79.842208/)

![images/chart-bambalapitiya-to-fort.png](images/chart-bambalapitiya-to-fort.png)

### Bambalapitiya ↔ Pamankada

📍 [6.895572°N, 79.854838°E to 6.871813°N, 79.884564°E](https://www.google.com/maps/dir/6.895572,79.854838/6.871813,79.884564/)

![images/chart-bambalapitiya-to-pamankada.png](images/chart-bambalapitiya-to-pamankada.png)

### Bambalapitiya ↔ Wellawatte

📍 [6.895572°N, 79.854838°E to 6.863289°N, 79.863608°E](https://www.google.com/maps/dir/6.895572,79.854838/6.863289,79.863608/)

![images/chart-bambalapitiya-to-wellawatte.png](images/chart-bambalapitiya-to-wellawatte.png)

### Borella ↔ Dematagoda

📍 [6.910883°N, 79.887898°E to 6.943176°N, 79.878208°E](https://www.google.com/maps/dir/6.910883,79.887898/6.943176,79.878208/)

![images/chart-borella-to-dematagoda.png](images/chart-borella-to-dematagoda.png)

### Borella ↔ Fort

📍 [6.910883°N, 79.887898°E to 6.931424°N, 79.842208°E](https://www.google.com/maps/dir/6.910883,79.887898/6.931424,79.842208/)

![images/chart-borella-to-fort.png](images/chart-borella-to-fort.png)

### Borella ↔ Pamankada

📍 [6.910883°N, 79.887898°E to 6.871813°N, 79.884564°E](https://www.google.com/maps/dir/6.910883,79.887898/6.871813,79.884564/)

![images/chart-borella-to-pamankada.png](images/chart-borella-to-pamankada.png)

### Borella ↔ Wellawatte

📍 [6.910883°N, 79.887898°E to 6.863289°N, 79.863608°E](https://www.google.com/maps/dir/6.910883,79.887898/6.863289,79.863608/)

![images/chart-borella-to-wellawatte.png](images/chart-borella-to-wellawatte.png)

### Dematagoda ↔ Fort

📍 [6.943176°N, 79.878208°E to 6.931424°N, 79.842208°E](https://www.google.com/maps/dir/6.943176,79.878208/6.931424,79.842208/)

![images/chart-dematagoda-to-fort.png](images/chart-dematagoda-to-fort.png)

### Dematagoda ↔ Mattakkuliya

📍 [6.943176°N, 79.878208°E to 6.980027°N, 79.875513°E](https://www.google.com/maps/dir/6.943176,79.878208/6.980027,79.875513/)

![images/chart-dematagoda-to-mattakkuliya.png](images/chart-dematagoda-to-mattakkuliya.png)

### Fort ↔ Mattakkuliya

📍 [6.931424°N, 79.842208°E to 6.980027°N, 79.875513°E](https://www.google.com/maps/dir/6.931424,79.842208/6.980027,79.875513/)

![images/chart-fort-to-mattakkuliya.png](images/chart-fort-to-mattakkuliya.png)

### Pamankada ↔ Wellawatte

📍 [6.871813°N, 79.884564°E to 6.863289°N, 79.863608°E](https://www.google.com/maps/dir/6.871813,79.884564/6.863289,79.863608/)

![images/chart-pamankada-to-wellawatte.png](images/chart-pamankada-to-wellawatte.png)

![Maintainer](https://img.shields.io/badge/maintainer-nuuuwan-red)
![MadeWith](https://img.shields.io/badge/made_with-python-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Locker Location Optimizer

## Author

* **Name:** Adam Czakon
* **Email:** czakonadam@gmail.com

---

## Overview

Locker Location Optimizer is a geospatial analysis application designed to identify optimal locations for new parcel lockers in urban areas. The system combines real-world data on existing locker locations with population density and distance-based analysis.

The project addresses a practical business question: *where should new parcel lockers be placed to maximize accessibility for users while avoiding excessive infrastructure saturation?*

---

## Demo & Description

The application implements a complete geospatial data analysis pipeline — from data acquisition, through processing, to result visualization.

### How the system works

1. The user selects a city from a list
2. The system fetches real parcel locker locations from the InPost API
3. An expanded bounding box is created to include surrounding areas
4. A spatial grid (~400 m resolution) is generated
5. Each grid point is enriched with:

   * estimated population based on raster data (GeoTIFF, e.g. WorldPop)
   * distance to the nearest parcel locker
   * local locker density (within a 1 km radius)
6. A score is computed
7. Data is filtered and clustered
8. The best locations are returned along with explanations
9. Results are presented in a Streamlit interface with a Folium map

---

### Key design decisions

#### 1. Expanded Bounding Box

Instead of analyzing only the strict city boundaries, the system uses an expanded area when fetching data.

Why:

* avoids edge effects
* includes lockers located just outside the city

This approach is standard in GIS systems.

---

#### 2. Spatial grid

The city is represented as a grid of points (~400 m), which ensures:

* uniform spatial coverage
* control over resolution
* scalability

---

#### 3. Population data from raster

Instead of aggregated data (e.g. districts), raster data (GeoTIFF) is used:

* higher spatial accuracy
* independence from administrative boundaries

---

#### 4. Distance calculation (BallTree + Haversine)

To find the nearest lockers, the system uses:

* BallTree (performance)
* Haversine metric (geographical accuracy)

This allows the solution to scale efficiently to large cities.

---

#### 5. Locker density

The number of lockers within a 1 km radius:

* helps identify already well-served areas
* penalizes such locations in the scoring process

---

#### 6. Scoring function

The system uses a weighted scoring function based on normalized features:

```
score =
0.65 × population_norm +
0.25 × distance_norm +
0.1 × raw_gap_norm
```

where:

* `population_norm` - normalized population (demand proxy)
* `distance_norm` - normalized distance to the nearest locker (higher = greater need)
* `raw_gap` - infrastructure gap indicator:

```
raw_gap = 1 / (1 + nearby_lockers)
```

* `raw_gap_norm` → normalized gap factor

All features are normalized using **MinMaxScaler**, bringing values to the [0, 1] range and enabling weighted combination.

Weight interpretation:

* **0.65 (population)** - primary demand driver
* **0.25 (distance)** - spatial need for a new location
* **0.1 (gap factor)** - correction for local saturation

---

#### 7. Candidate filtering

Before final selection, the system applies filtering conditions:

* distance to nearest locker > 500 m
* population above a defined threshold

Then, from the remaining points, the top candidates are selected based on score distribution:

```
top 20% (0.8 quantile)
```

This approach:

* removes low-value areas
* avoids already well-served locations
* focuses on relatively best candidates per city

---

#### 8. Clustering (DBSCAN)

DBSCAN is used to:

* remove duplicate nearby recommendations
* group spatially close points
* avoid specifying the number of clusters

This makes it more suitable than k-means in this context.

---

### User interface

The application includes a Streamlit UI with:

* city selection
* minimum score slider
* metrics:

  * number of lockers
  * number of recommendations
  * average distance
* results table
* interactive map

The map includes:

* 🟢 existing lockers
* 🔴 recommended locations (scaled by score)
* 🔵 city boundaries

---

### Demo

#### Interfejs użytkownika
![Interfejs](photos/Interfejs.png)

#### Mapa wyników
![Mapa](photos/Map.png)

#### Mapa wraz z Legendą
![Legenda](photos/Map_Legend.png)


---

## Technologies

* **Python 3.10+**
* **pandas, numpy** — data processing
* **requests** — API communication
* **scikit-learn**

  * BallTree
  * DBSCAN
* **rasterio** — spatial data (GeoTIFF)
* **folium** — map visualization
* **streamlit** — UI

### Why these choices

* BallTree → efficient spatial queries
* DBSCAN → natural spatial clustering
* raster → higher accuracy than aggregated data
* Streamlit → fast UI prototyping

---

## How to run

### Prerequisites

* Python 3.10+
* pip
* `population.tif` file
* internet connection (API access)

---

### Build & run

```bash
git clone <your-repo-url>
cd locker-location-optimizer

python -m venv venv
source venv/bin/activate
# Windows:
# venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
```

---

## What I would do with more time

* replace heuristic scoring with a learning-based model (e.g. Gradient Boosting / XGBoost)
* adapt the model to urban vs. rural conditions (different feature weights)
* extend support to more cities
* allow analysis for arbitrary regions (country, voivodeship, county, municipality) using GIS data
* improve the user interface
* add heatmaps for population density and locker density
* use higher-resolution population data (currently ~1 km²)
* integrate contextual data (POI, transport, traffic intensity) to better model demand and accessibility
* calibrate the model using historical data (e.g. existing locations and their usage) instead of manually defined weights

---

## AI usage

AI tools (ChatGPT) were used as technical support during development.

They helped with:

* refining the project structure
* clarifying geospatial concepts, especially distance calculations (Haversine, radians)
* improving the Streamlit UI and interaction logic

All suggestions were reviewed, adapted, and implemented manually to ensure correctness and consistency of the system.

---

## Anything else?

In my opinion, this was a great idea for a recruitment task.

I hope my approach and initiative meet your expectations. I would really appreciate your feedback and look forward to your response.

I would be very interested in working on similar data-driven systems during an internship and further developing solutions like this in your organization.

Thank you for the opportunity.

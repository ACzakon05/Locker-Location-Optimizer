import streamlit as st
from src.cities import load_cities, get_bbox, get_expanded_bbox
from src.pipeline import pipeline
from src.visualization import create_map
import json

st.title("Locker Location Optimizer")

cities = load_cities()
city_names = [c["name"] for c in cities]

selected = st.selectbox("Select City", city_names)

if st.button("Analyze"):
    bbox = get_bbox(selected, cities)
    expanded_bbox = get_expanded_bbox(selected, cities)

    grid, lockers, recs = pipeline(expanded_bbox, bbox)

    if recs is None:
        st.error("No data available")
    else:
        st.subheader("Top Recommendations")
        st.dataframe(recs)

        m = create_map(lockers, recs, bbox)
        st.components.v1.html(m._repr_html_(), height=600)

        recs.to_json("recommendations.json", orient="records")
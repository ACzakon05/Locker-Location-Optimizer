import streamlit as st
from src.cities import load_cities, get_bbox, get_expanded_bbox
from src.pipeline import pipeline
from src.visualization import create_map
import json

st.title("Locker Location Optimizer")

cities = load_cities()
city_names = [c["name"] for c in cities]

selected = st.sidebar.selectbox("Select City", city_names)
min_score = st.sidebar.slider("Minimal Score", 0.0, 1.0, 0.1, 0.01)

if st.sidebar.button("Analyze"):
    bbox = get_bbox(selected, cities)
    expanded_bbox = get_expanded_bbox(selected, cities)

    grid, lockers, recs = pipeline(expanded_bbox, bbox)

    if recs is None:
        st.error("No data available")
    else:
        # Filter recommendations by min_score
        filtered_recs = recs[recs['score'] >= min_score]

        # Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Lockers", len(lockers) if lockers is not None else 0)
        col2.metric("Recommendations", len(filtered_recs))
        col3.metric("Avg Distance (m)", f"{filtered_recs['distance'].mean():.0f}" if not filtered_recs.empty else "N/A")

        st.subheader("Top Recommendations")
        st.dataframe(filtered_recs)

        m = create_map(lockers, filtered_recs, bbox)
        st.components.v1.html(m._repr_html_(), height=600)

        # Legend
        st.markdown("""
        ### Legenda mapy
        - 🟢 **Paczkomaty**: Zielone ikony pudełek (klastrowane przy zoomie)
        - 🔴 **Rekomendacje**: Czerwone gwiazdy (znacznik) + czerwone okręgi (obszar)
        - 🔵 **Granica miasta**: Niebieski wielokąt
        """)

        filtered_recs.to_json("recommendations.json", orient="records")
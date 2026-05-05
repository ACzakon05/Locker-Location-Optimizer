import folium
from folium import plugins

def create_map(lockers_df, recommendations, bbox):
    if lockers_df is None or lockers_df.empty:
        # If no lockers, center on recommendations or default
        if recommendations.empty:
            center = [50.0647, 19.9450]  # Default to Krakow center or something
        else:
            center = [recommendations["lat"].mean(), recommendations["lon"].mean()]
    else:
        center = [lockers_df["lat"].mean(), lockers_df["lon"].mean()]
    m=folium.Map(location=center,zoom_start=12)

    # Add marker cluster for lockers
    marker_cluster = plugins.MarkerCluster().add_to(m)

    # Add city boundary
    corners = [(bbox[0], bbox[1]), (bbox[0], bbox[3]), (bbox[2], bbox[3]), (bbox[2], bbox[1])]
    folium.Polygon(corners, color='blue', fill=False, weight=2).add_to(m)

    if lockers_df is not None and not lockers_df.empty:
        for _, row in lockers_df.iterrows():
            icon = folium.Icon(icon='box', prefix='fa', color='green')
            folium.Marker(
                location=[row["lat"], row["lon"]],
                icon=icon,
                popup=row["name"]
            ).add_to(marker_cluster)

    if not recommendations.empty and "lat" in recommendations.columns:
        for _, row in recommendations.iterrows():
            html = f"""
            <table border="1" style="border-collapse: collapse;">
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Population</td><td>{row['population']:.0f}</td></tr>
                <tr><td>Distance to nearest locker</td><td>{row['distance']:.0f} m</td></tr>
                <tr><td>Score</td><td>{row['score']:.2f}</td></tr>
            </table>
            """
            popup = folium.Popup(html, max_width=300)
            # Add marker for the best location
            rec_icon = folium.Icon(icon='star', prefix='fa', color='red')
            folium.Marker(
                location=[row["lat"], row["lon"]],
                icon=rec_icon,
                tooltip=f"Score: {row['score']:.2f}"
            ).add_to(m)
            folium.Circle(
                location=[row["lat"], row["lon"]],
                # 'radius' w folium.Circle podajemy w METRACH
                # Teraz kółko będzie miało np. 400 metrów promienia na ziemi
                radius=200 + (row.get("score", 0) * 100), 
                color="red",
                fill=True,
                fill_opacity=0.3,
                popup=popup,
                tooltip="Potencjalna strefa inwestycyjna"
            ).add_to(m)
    
    return m
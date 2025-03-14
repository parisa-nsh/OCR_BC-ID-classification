import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from neo4j_handler import Neo4jHandler

class Analytics:
    def __init__(self, data_storage):
        self.data_storage = data_storage
        plt.style.use('default')
        self.geolocator = Nominatim(user_agent="my_ocr_app")

    def generate_gender_distribution(self):
        gender_stats = self.data_storage.get_gender_distribution()
        df = pd.DataFrame(gender_stats)
        plt.figure(figsize=(8, 6))
        plt.pie(df['count'], labels=df['gender'], autopct='%1.1f%%')
        plt.title('Gender Distribution')
        plt.savefig('static/gender_distribution.png')
        plt.close()

    def generate_age_group_distribution(self):
        age_stats = self.data_storage.get_age_group_distribution()
        df = pd.DataFrame(age_stats)
        plt.figure(figsize=(10, 6))
        plt.bar(df['age_group'], df['count'])
        plt.title('Age Group Distribution')
        plt.xlabel('Age Group')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('static/age_group_distribution.png')
        plt.close()

    def generate_height_distribution(self):
        height_stats = self.data_storage.get_height_distribution()
        df = pd.DataFrame(height_stats)
        plt.figure(figsize=(10, 6))
        plt.bar(df['height'], df['count'])
        plt.title('Height Distribution')
        plt.xlabel('Height (cm)')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('static/height_distribution.png')
        plt.close()

    def get_coordinates(self, postal_code):
        """Get coordinates for a postal code with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Add 'Canada' to improve geocoding accuracy
                location = self.geolocator.geocode(f"{postal_code}, Canada")
                if location:
                    return location.latitude, location.longitude
                time.sleep(1)  # Wait between retries
            except GeocoderTimedOut:
                if attempt == max_retries - 1:
                    print(f"Could not get coordinates for postal code {postal_code}")
                time.sleep(1)
        return None

    def generate_postal_code_distribution(self):
        """Generate postal code distribution as an interactive map"""
        postal_stats = self.data_storage.get_postal_code_distribution()
        df = pd.DataFrame(postal_stats)
        
        # Create a map centered on Canada
        m = folium.Map(location=[56.1304, -106.3468], zoom_start=4)
        
        # Add markers for each postal code
        for _, row in df.iterrows():
            postal_code = row['postal_code']
            count = row['count']
            
            # Get coordinates for the postal code
            coords = self.get_coordinates(postal_code)
            if coords:
                lat, lon = coords
                # Create popup text
                popup_text = f"Postal Code: {postal_code}<br>Count: {count}"
                
                # Add marker to map
                folium.Marker(
                    location=[lat, lon],
                    popup=popup_text,
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(m)
        
        # Save the map
        m.save('static/postal_code_distribution.html')
        
        # Create a simple bar chart as fallback
        plt.figure(figsize=(12, 6))
        plt.bar(df['postal_code'], df['count'])
        plt.title('Postal Code Distribution')
        plt.xlabel('Postal Code')
        plt.ylabel('Count')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig('static/postal_code_distribution.png')
        plt.close()

    def generate_all_visualizations(self):
        """Generate all visualization plots"""
        self.generate_gender_distribution()
        self.generate_age_group_distribution()
        self.generate_height_distribution()
        self.generate_postal_code_distribution()

    def get_statistics_report(self):
        """Generate a comprehensive statistics report"""
        stats = self.data_storage.get_statistics()
        return {
            'gender_stats': pd.DataFrame(stats['gender_distribution']),
            'age_group_stats': pd.DataFrame(stats['age_group_distribution']),
            'height_stats': pd.DataFrame(stats['height_distribution']),
            'postal_code_stats': pd.DataFrame(stats['postal_code_distribution'])
        }

    def close(self):
        """Close the Neo4j connection"""
        self.data_storage.close() 
import json
import os
from collections import defaultdict

class DataStorage:
    def __init__(self):
        self.data_file = 'data/id_cards.json'
        os.makedirs('data', exist_ok=True)
        self.load_data()

    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
            except:
                self.data = []
        else:
            self.data = []

    def save_data(self):
        """Save data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f)

    def add_record(self, record):
        """Add a new ID card record"""
        self.data.append(record)
        self.save_data()

    def get_gender_distribution(self):
        """Get gender distribution statistics"""
        counts = defaultdict(int)
        for record in self.data:
            counts[record['gender']] += 1
        return [{'gender': k, 'count': v} for k, v in counts.items()]

    def get_age_group_distribution(self):
        """Get age group distribution statistics"""
        counts = defaultdict(int)
        for record in self.data:
            counts[record['age_group']] += 1
        
        # Ensure all age groups are represented
        age_groups = {
            '18-24': counts['18-24'],
            '25-49': counts['25-49'],
            '50+': counts['50+']
        }
        return [{'age_group': k, 'count': v} for k, v in age_groups.items()]

    def get_height_distribution(self):
        """Get height distribution statistics"""
        heights = defaultdict(int)
        for record in self.data:
            heights[record['height']] += 1
        return [{'height': k, 'count': v} for k, v in sorted(heights.items())]

    def get_postal_code_distribution(self):
        """Get postal code distribution statistics"""
        codes = defaultdict(int)
        for record in self.data:
            codes[record['postal_code']] += 1
        return [{'postal_code': k, 'count': v} for k, v in codes.items()]

    def get_statistics(self):
        """Get all statistics"""
        return {
            'gender_distribution': self.get_gender_distribution(),
            'age_group_distribution': self.get_age_group_distribution(),
            'height_distribution': self.get_height_distribution(),
            'postal_code_distribution': self.get_postal_code_distribution()
        } 
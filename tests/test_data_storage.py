import pytest
import os
import json
from data_storage import DataStorage

@pytest.fixture
def data_storage(tmp_path):
    # Use a temporary directory for testing
    storage = DataStorage(data_file=str(tmp_path / "test_data.json"))
    return storage

@pytest.fixture
def sample_record():
    return {
        "gender": "F",
        "age": 25,
        "height": 170,
        "postal_code": "V6B 1A1"
    }

def test_data_storage_initialization(data_storage):
    assert data_storage is not None
    assert isinstance(data_storage.data, list)

def test_add_record(data_storage, sample_record):
    data_storage.add_record(sample_record)
    assert len(data_storage.data) == 1
    assert data_storage.data[0] == sample_record

def test_save_and_load_data(data_storage, sample_record):
    data_storage.add_record(sample_record)
    data_storage.save_data()
    
    # Create a new instance to test loading
    new_storage = DataStorage(data_file=data_storage.data_file)
    assert len(new_storage.data) == 1
    assert new_storage.data[0] == sample_record

def test_get_gender_distribution(data_storage, sample_record):
    data_storage.add_record(sample_record)
    distribution = data_storage.get_gender_distribution()
    assert isinstance(distribution, dict)
    assert distribution.get("F") == 1

def test_get_age_group_distribution(data_storage, sample_record):
    data_storage.add_record(sample_record)
    distribution = data_storage.get_age_group_distribution()
    assert isinstance(distribution, dict)
    assert sum(distribution.values()) == 1

def test_get_height_distribution(data_storage, sample_record):
    data_storage.add_record(sample_record)
    distribution = data_storage.get_height_distribution()
    assert isinstance(distribution, dict)
    assert sum(distribution.values()) == 1

def test_get_postal_code_distribution(data_storage, sample_record):
    data_storage.add_record(sample_record)
    distribution = data_storage.get_postal_code_distribution()
    assert isinstance(distribution, dict)
    assert distribution.get("V6B 1A1") == 1

def test_get_statistics(data_storage, sample_record):
    data_storage.add_record(sample_record)
    stats = data_storage.get_statistics()
    assert isinstance(stats, dict)
    assert "gender_distribution" in stats
    assert "age_group_distribution" in stats
    assert "height_distribution" in stats
    assert "postal_code_distribution" in stats 
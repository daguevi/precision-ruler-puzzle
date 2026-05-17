"""
Tests for database functionality
"""

import pytest
import sqlite3
import tempfile
from pathlib import Path
from app.database.db_manager import DatabaseManager
from app.database.repository import Repository


class TestDatabaseManager:
    """Test suite for DatabaseManager."""
    
    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        
        manager = DatabaseManager(db_path)
        yield manager
        
        manager.close()
        Path(db_path).unlink(missing_ok=True)
    
    def test_database_initialization(self, temp_db):
        """Test database schema creation."""
        temp_db.initialize_database()
        
        conn = temp_db.get_connection()
        cursor = conn.cursor()
        
        # Check tables exist
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='layouts'"
        )
        assert cursor.fetchone() is not None
    
    def test_seed_data(self, temp_db):
        """Test default data seeding."""
        temp_db.initialize_database()
        
        conn = temp_db.get_connection()
        cursor = conn.cursor()
        
        # Check materials are seeded
        cursor.execute("SELECT COUNT(*) FROM materials")
        count = cursor.fetchone()[0]
        assert count > 0
        
        # Check inventory items are seeded
        cursor.execute("SELECT COUNT(*) FROM inventory_items")
        count = cursor.fetchone()[0]
        assert count >= 35


class TestRepository:
    """Test suite for Repository."""
    
    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        
        manager = DatabaseManager(db_path)
        manager.initialize_database()
        yield manager
        
        manager.close()
        Path(db_path).unlink(missing_ok=True)
    
    def test_create_record(self, temp_db):
        """Test creating a record."""
        repo = Repository(temp_db, "materials")
        data = {
            "name": "Test Material",
            "description": "Test",
            "density_g_cm3": 7.85
        }
        
        record_id = repo.create(data)
        assert record_id > 0
    
    def test_find_by_id(self, temp_db):
        """Test finding record by ID."""
        repo = Repository(temp_db, "materials")
        data = {
            "name": "Test Material",
            "description": "Test",
            "density_g_cm3": 7.85
        }
        
        record_id = repo.create(data)
        record = repo.find_by_id(record_id)
        
        assert record is not None
        assert record["name"] == "Test Material"

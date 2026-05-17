"""
Database manager with schema initialization and migrations
"""

import sqlite3
from pathlib import Path
from typing import Optional
from datetime import datetime


class DatabaseManager:
    """
    Manages SQLite database connection, schema, and migrations.
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database manager.
        Args:
            db_path: Path to SQLite database file. Defaults to app/database/precision_ruler.db
        """
        if db_path is None:
            db_dir = Path(__file__).parent
            db_path = db_dir / "precision_ruler.db"
        
        self.db_path = Path(db_path)
        self.connection: Optional[sqlite3.Connection] = None
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Get or create database connection.
        """
        if self.connection is None:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            # Enable foreign keys
            self.connection.execute("PRAGMA foreign_keys = ON")
        return self.connection
    
    def close(self) -> None:
        """
        Close database connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def initialize_database(self) -> None:
        """
        Initialize database schema if not exists, then seed data.
        """
        conn = self.get_connection()
        
        # Create schema
        self._create_schema(conn)
        
        # Seed default data
        self._seed_default_data(conn)
        
        conn.commit()
    
    def _create_schema(self, conn: sqlite3.Connection) -> None:
        """
        Create all required tables.
        """
        cursor = conn.cursor()
        
        # Settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                setting_type TEXT DEFAULT 'string',
                description TEXT,
                is_user_editable BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                deleted_at TIMESTAMP
            )
        """)
        
        # Materials table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                density_g_cm3 REAL,
                hardness_hv REAL,
                thermal_stability TEXT,
                cost_per_unit REAL,
                is_active BOOLEAN DEFAULT 1,
                properties TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                deleted_at TIMESTAMP
            )
        """)
        
        # Rulers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rulers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                total_length_mm REAL NOT NULL,
                maximum_stack_width_mm REAL NOT NULL,
                supported_engagement_modes TEXT,
                tolerance_microns REAL DEFAULT 10.0,
                supported_materials TEXT,
                default_offset_mm REAL DEFAULT 0.0,
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                deleted_at TIMESTAMP
            )
        """)
        
        # Inventory items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                component_type TEXT NOT NULL,
                thickness_mm REAL NOT NULL,
                outer_diameter_mm REAL NOT NULL,
                inner_diameter_mm REAL NOT NULL,
                material_profile TEXT DEFAULT 'standard',
                precision_class TEXT DEFAULT 'standard',
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                total_quantity INTEGER DEFAULT 0,
                reserved_quantity INTEGER DEFAULT 0,
                available_quantity INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                deleted_at TIMESTAMP
            )
        """)
        
        # Inventory batches table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory_batches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inventory_item_id INTEGER NOT NULL,
                batch_code TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                received_date TEXT NOT NULL,
                expiry_date TEXT,
                notes TEXT,
                is_available BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                deleted_at TIMESTAMP,
                FOREIGN KEY (inventory_item_id) REFERENCES inventory_items(id)
            )
        """)
        
        # Inventory movements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inventory_item_id INTEGER NOT NULL,
                movement_type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                reference_type TEXT,
                reference_id INTEGER,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                deleted_at TIMESTAMP,
                FOREIGN KEY (inventory_item_id) REFERENCES inventory_items(id)
            )
        """)
        
        # Layouts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS layouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                master_board_width_mm REAL NOT NULL,
                layer_thickness_mm REAL NOT NULL,
                ruler_id INTEGER NOT NULL,
                material_id INTEGER NOT NULL,
                side_offset_mm REAL NOT NULL,
                engagement_mode TEXT DEFAULT 'standard',
                layout_style TEXT DEFAULT 'center_balanced',
                spacer_material TEXT DEFAULT 'metal_both',
                use_micro_shims BOOLEAN DEFAULT 0,
                status TEXT DEFAULT 'draft',
                total_stack_width_mm REAL,
                estimated_compensation_mm REAL,
                warnings TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                deleted_at TIMESTAMP,
                FOREIGN KEY (ruler_id) REFERENCES rulers(id),
                FOREIGN KEY (material_id) REFERENCES materials(id)
            )
        """)
        
        # Layout blocks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS layout_blocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                layout_id INTEGER NOT NULL,
                width_mm REAL NOT NULL,
                quantity INTEGER NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                deleted_at TIMESTAMP,
                FOREIGN KEY (layout_id) REFERENCES layouts(id)
            )
        """)
        
        # Layout sequences table (generated assembly sequences)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS layout_sequences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                layout_id INTEGER NOT NULL,
                ruler_position TEXT NOT NULL,
                sequence_order INTEGER NOT NULL,
                component_type TEXT NOT NULL,
                component_id INTEGER,
                quantity INTEGER NOT NULL,
                thickness_mm REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                deleted_at TIMESTAMP,
                FOREIGN KEY (layout_id) REFERENCES layouts(id)
            )
        """)
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                full_name TEXT,
                password_hash TEXT,
                is_active BOOLEAN DEFAULT 1,
                is_admin BOOLEAN DEFAULT 0,
                preferences TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                deleted_at TIMESTAMP
            )
        """)
        
        # Create indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_layouts_status ON layouts(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_inventory_component_type ON inventory_items(component_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_inventory_batches_item ON inventory_batches(inventory_item_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_layout_sequences_layout ON layout_sequences(layout_id)")
        
        conn.commit()
    
    def _seed_default_data(self, conn: sqlite3.Connection) -> None:
        """
        Seed default data if not already seeded.
        """
        cursor = conn.cursor()
        
        # Check if data already seeded
        cursor.execute("SELECT COUNT(*) FROM materials")
        if cursor.fetchone()[0] > 0:
            return  # Already seeded
        
        # Seed materials
        materials = [
            ("Hardened Core Steel", "High-strength precision material", 7.85, 800, "high", 15.0),
            ("Aluminum Alloy", "Lightweight aerospace grade", 2.70, 150, "standard", 8.0),
            ("Cast Iron", "Precision casting material", 7.20, 200, "standard", 5.0),
        ]
        for mat in materials:
            cursor.execute("""
                INSERT OR IGNORE INTO materials 
                (name, description, density_g_cm3, hardness_hv, thermal_stability, cost_per_unit)
                VALUES (?, ?, ?, ?, ?, ?)
            """, mat)
        
        # Seed rulers
        rulers = [
            ("Standard Ruler", 500.0, 150.0, "standard,alternating", 10.0, "Hardened Core Steel,Aluminum Alloy", 0.5),
            ("Precision Ruler", 750.0, 200.0, "standard,alternating", 5.0, "Hardened Core Steel", 0.3),
            ("Industrial Ruler", 1000.0, 250.0, "standard", 15.0, "Cast Iron,Aluminum Alloy", 1.0),
        ]
        for ruler in rulers:
            cursor.execute("""
                INSERT OR IGNORE INTO rulers
                (name, total_length_mm, maximum_stack_width_mm, supported_engagement_modes, 
                 tolerance_microns, supported_materials, default_offset_mm)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ruler)
        
        # Seed inventory items
        self._seed_inventory_items(cursor)
        
        # Seed settings
        settings = [
            ("unit_system", "metric", "string", "Measurement unit system"),
            ("theme", "dark", "string", "Application theme"),
            ("language", "en", "string", "UI language"),
            ("auto_save_interval", "30", "int", "Auto-save interval in seconds"),
        ]
        for setting in settings:
            cursor.execute("""
                INSERT OR IGNORE INTO settings (key, value, setting_type, description)
                VALUES (?, ?, ?, ?)
            """, setting)
        
        conn.commit()
    
    def _seed_inventory_items(self, cursor: sqlite3.Cursor) -> None:
        """
        Seed all inventory items based on specification.
        """
        # Edge Blocks
        edge_blocks = [
            ("edge_block", 10.0, 260.0, 140.0, "hardened_core", "standard", 40),
            ("edge_block", 5.0, 260.0, 140.0, "hardened_core", "standard", 40),
        ]
        
        # Core Spacers
        core_spacers = [
            ("core_spacer", 100.0, 200.0, 140.0, "standard", "standard", 8),
            ("core_spacer", 60.0, 200.0, 140.0, "standard", "standard", 12),
            ("core_spacer", 50.0, 200.0, 140.0, "standard", "standard", 12),
            ("core_spacer", 40.0, 200.0, 140.0, "standard", "standard", 15),
            ("core_spacer", 30.0, 200.0, 140.0, "standard", "standard", 15),
            ("core_spacer", 20.0, 200.0, 140.0, "standard", "standard", 20),
            ("core_spacer", 15.0, 200.0, 140.0, "standard", "standard", 20),
            ("core_spacer", 10.0, 200.0, 140.0, "standard", "standard", 25),
            ("core_spacer", 5.0, 200.0, 140.0, "standard", "standard", 30),
            ("core_spacer", 2.0, 200.0, 140.0, "standard", "standard", 30),
            ("core_spacer", 1.0, 200.0, 140.0, "standard", "standard", 30),
        ]
        
        # Precision Core Tiles
        precision_tiles = [
            ("precision_core_tile", 1.09, 200.0, 140.0, "precision", "standard", 25),
            ("precision_core_tile", 1.08, 200.0, 140.0, "precision", "standard", 25),
            ("precision_core_tile", 1.07, 200.0, 140.0, "precision", "standard", 25),
            ("precision_core_tile", 1.06, 200.0, 140.0, "precision", "standard", 25),
            ("precision_core_tile", 1.05, 200.0, 140.0, "precision", "standard", 65),
            ("precision_core_tile", 1.04, 200.0, 140.0, "precision", "standard", 25),
            ("precision_core_tile", 1.03, 200.0, 140.0, "precision", "standard", 25),
            ("precision_core_tile", 1.02, 200.0, 140.0, "precision", "standard", 40),
            ("precision_core_tile", 1.02, 200.0, 140.0, "precision", "batch_b", 25),
            ("precision_core_tile", 1.01, 200.0, 140.0, "precision", "standard", 25),
        ]
        
        # Grip Rings
        grip_rings = [
            ("grip_ring", 100.0, 259.0, 140.0, "standard", "standard", 6),
            ("grip_ring", 60.0, 259.0, 140.0, "standard", "standard", 10),
            ("grip_ring", 50.0, 259.0, 140.0, "standard", "standard", 10),
            ("grip_ring", 40.0, 259.0, 140.0, "standard", "standard", 12),
            ("grip_ring", 30.0, 259.0, 140.0, "standard", "standard", 12),
            ("grip_ring", 20.0, 259.0, 140.0, "standard", "standard", 16),
            ("grip_ring", 15.0, 259.0, 140.0, "standard", "standard", 16),
            ("grip_ring", 10.0, 259.0, 140.0, "standard", "standard", 20),
        ]
        
        # Micro Shims
        micro_shims = [
            ("micro_shim", 0.10, 200.0, 140.0, "standard", "standard", 60),
            ("micro_shim", 0.07, 200.0, 140.0, "standard", "standard", 60),
            ("micro_shim", 0.05, 200.0, 140.0, "standard", "standard", 60),
            ("micro_shim", 0.03, 200.0, 140.0, "standard", "standard", 60),
        ]
        
        all_items = edge_blocks + core_spacers + precision_tiles + grip_rings + micro_shims
        
        for item in all_items:
            component_type, thickness, od, id, material, precision, quantity = item
            cursor.execute("""
                INSERT INTO inventory_items
                (component_type, thickness_mm, outer_diameter_mm, inner_diameter_mm, 
                 material_profile, precision_class, total_quantity, available_quantity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (component_type, thickness, od, id, material, precision, quantity, quantity))
    
    def reset_database(self) -> None:
        """
        WARNING: Completely reset database by deleting and recreating it.
        """
        self.close()
        if self.db_path.exists():
            self.db_path.unlink()
        self.initialize_database()

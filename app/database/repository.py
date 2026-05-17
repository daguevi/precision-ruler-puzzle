"""
Generic repository pattern for database operations
"""

from typing import List, Optional, Type, TypeVar, Generic
import sqlite3
from .db_manager import DatabaseManager

T = TypeVar('T')


class Repository(Generic[T]):
    """
    Generic repository for CRUD operations.
    """
    
    def __init__(self, db_manager: DatabaseManager, table_name: str):
        """
        Initialize repository.
        
        Args:
            db_manager: DatabaseManager instance
            table_name: Name of the table
        """
        self.db_manager = db_manager
        self.table_name = table_name
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Get database connection.
        """
        return self.db_manager.get_connection()
    
    def find_by_id(self, id: int) -> Optional[dict]:
        """
        Find record by ID.
        """
        cursor = self.get_connection().cursor()
        cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE id = ? AND deleted_at IS NULL",
            (id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def find_all(self, limit: Optional[int] = None, offset: int = 0) -> List[dict]:
        """
        Find all active records.
        """
        cursor = self.get_connection().cursor()
        query = f"SELECT * FROM {self.table_name} WHERE deleted_at IS NULL"
        
        if limit:
            query += f" LIMIT {limit} OFFSET {offset}"
        
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]
    
    def create(self, data: dict) -> int:
        """
        Create new record.
        Returns the new record's ID.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        
        cursor.execute(query, tuple(data.values()))
        conn.commit()
        return cursor.lastrowid
    
    def update(self, id: int, data: dict) -> bool:
        """
        Update record.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        query = f"UPDATE {self.table_name} SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        
        cursor.execute(query, tuple(list(data.values()) + [id]))
        conn.commit()
        return cursor.rowcount > 0
    
    def delete(self, id: int, soft_delete: bool = True) -> bool:
        """
        Delete record (soft or hard delete).
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if soft_delete:
            cursor.execute(
                f"UPDATE {self.table_name} SET deleted_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (id,)
            )
        else:
            cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (id,))
        
        conn.commit()
        return cursor.rowcount > 0
    
    def find_by_field(self, field: str, value: any) -> Optional[dict]:
        """
        Find first record by field value.
        """
        cursor = self.get_connection().cursor()
        cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE {field} = ? AND deleted_at IS NULL LIMIT 1",
            (value,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def find_all_by_field(self, field: str, value: any) -> List[dict]:
        """
        Find all records by field value.
        """
        cursor = self.get_connection().cursor()
        cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE {field} = ? AND deleted_at IS NULL",
            (value,)
        )
        return [dict(row) for row in cursor.fetchall()]

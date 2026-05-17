# Precision Ruler Puzzle System

A sophisticated desktop application for designing and optimizing precision ruler assemblies with modular blocks, balancing components, and alignment systems.

## Features

- **Layouts Module**: 4-step wizard for creating precision ruler configurations
- **Rulers Management**: CRUD operations for ruler presets
- **Inventory System**: 35+ modular components with batch tracking
- **Optimization Engine**: Advanced constraint-solving algorithm for assembly generation
- **CAD-like UI**: Professional dark theme with graphics rendering
- **Data Persistence**: SQLite with automatic schema initialization
- **Export Capabilities**: PDF and PNG export for diagrams

## Tech Stack

- **Language**: Python 3.9+
- **GUI**: PySide6 / PyQt6
- **Database**: SQLite
- **Architecture**: MVC/MVVM with Repository pattern
- **Export**: ReportLab for PDF generation

## Quick Start

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/daguevi/precision-ruler-puzzle.git
cd precision-ruler-puzzle

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Project Structure

```
precision-ruler-puzzle/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── venv/                   # Virtual environment (local only)
├── app/
│   ├── __init__.py
│   ├── models/             # Data models and ORM
│   ├── ui/                 # Qt6 UI components
│   ├── database/           # Database layer
│   ├── services/           # Business logic services
│   ├── algorithms/         # Optimization engine
│   ├── rendering/          # Graphics rendering
│   ├── exports/            # PDF/PNG export
│   └── utils/              # Utility functions
├── tests/                  # Unit and integration tests
├── docs/                   # Documentation
└── resources/              # Assets and data files
```

## Module Documentation

### Layouts
The core module for creating precision ruler configurations through a guided 4-step wizard:
1. **Basics** - Define layout name, dimensions, materials
2. **Block Requirements** - Specify how the master board is divided
3. **Build Configuration** - Set engagement modes, spacer materials, optimization parameters
4. **Assembly View** - Review generated configuration with diagrams and sequences

### Rulers
Manage ruler presets with CRUD operations, including:
- Ruler dimensions and stack widths
- Supported engagement modes
- Material compatibility
- Tolerance specifications

### Inventory
Preloaded 35+ component inventory across 4 categories:
- **Edge Blocks** (10mm, 5mm)
- **Core Spacers** (2-100mm)
- **Precision Core Tiles** (1.01-1.09mm)
- **Grip Rings** (10-100mm)
- **Micro Shims** (0.03-0.10mm)

### Algorithm Engine
Advanced constraint-solving optimization with:
- Backtracking and heuristic search
- Offset compensation
- Inventory consumption tracking
- Component minimization
- Symmetric/asymmetric layout support

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Database Migrations
Migrations are handled automatically on application startup. To reset:
```python
from app.database.db_manager import DatabaseManager
db = DatabaseManager()
db.reset_database()  # WARNING: Clears all data
```

## License

Proprietary prototype. See LICENSE file for details.

## Support

For issues, feature requests, or documentation, please open a GitHub issue.

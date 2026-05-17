# Architecture Overview

## Application Structure

### MVC/MVVM Pattern

The application follows Model-View-Controller principles:

- **Models** (`app/models/`) - Domain objects and business logic entities
- **Views** (`app/ui/`) - Qt6 user interface components
- **Controllers/Services** (`app/services/`) - Business logic and orchestration
- **Data Layer** (`app/database/`) - Database access and persistence

### Directory Layout

```
app/
├── models/              # Domain models (Layout, Ruler, Inventory, etc.)
├── ui/                  # PySide6 UI components
│   ├── main_window.py   # Main application window
│   ├── navigation.py    # Sidebar navigation
│   └── workspace.py     # Stacked workspace pages
├── database/            # Database layer
│   ├── db_manager.py    # Schema, migrations, seeding
│   └── repository.py    # Generic CRUD repository
├── services/            # Business logic services
├── algorithms/          # Optimization engine
├── rendering/           # Graphics rendering
├── exports/             # PDF/PNG export functionality
└── utils/               # Utilities (styles, helpers)
```

## Database Design

### Schema

- **layouts** - Main layout configurations
- **layout_blocks** - Block requirements within a layout
- **layout_sequences** - Generated assembly sequences
- **rulers** - Ruler presets
- **inventory_items** - Master inventory items
- **inventory_batches** - Batch tracking
- **inventory_movements** - Audit trail
- **materials** - Material definitions
- **users** - User accounts
- **settings** - Application settings

### Relationships

- Foreign keys enforce referential integrity
- Soft deletes preserve historical data
- Timestamps track creation and modification

## Optimization Algorithm

The core algorithm generates valid ruler assemblies by:

1. **Input Validation** - Check layout configuration
2. **Component Selection** - Choose appropriate blocks and spacers
3. **Sequence Generation** - Build top and bottom ruler sequences
4. **Offset Compensation** - Handle alternating engagement logic
5. **Inventory Consumption** - Track and validate component availability
6. **Minimization** - Reduce component count while maintaining precision

## Technology Stack

- **Language**: Python 3.9+
- **GUI**: PySide6 (Qt6 bindings)
- **Database**: SQLite3
- **PDF Export**: ReportLab
- **Testing**: pytest

## Design Patterns

### Repository Pattern

Generic repository provides consistent CRUD operations across all tables.

### Dependency Injection

Services receive dependencies through constructors for testability.

### Factory Pattern

UI components are created through dedicated factory methods.

### Observer Pattern

Qt signals/slots provide event-driven communication between components.

## Extensibility

The architecture supports future expansion through:

- Modular service layer
- Plugin-ready algorithm interface
- Multiple database backend support
- Custom rendering engines
- Alternative export formats

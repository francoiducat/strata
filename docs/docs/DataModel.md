# Data Model

## Entity-Relationship Diagram (Database / ORM)

👉 Persistence-oriented
```mermaid
erDiagram
    PORTFOLIO ||--o{ ASSET : owns
    PORTFOLIO ||--o{ PORTFOLIO_SNAPSHOT : "has (auto-calculated)"

    ASSET ||--o{ TRANSACTION : has
    ASSET ||--o{ ASSET_SNAPSHOT : "has (manually entered)"
    ASSET }o--|| ASSET_TYPE : "typed as"
    ASSET }o--o{ ASSET_CATEGORY : ""
    ASSET_CATEGORY }o--|| CATEGORY : ""
    ASSET }o--o{ ASSET_TAG : ""
    ASSET_TAG }o--|| TAG : ""

    PORTFOLIO {
        uuid id PK
        string name
        string base_currency
        datetime created_at
        datetime updated_at
    }

    PORTFOLIO_SNAPSHOT {
        uuid id PK
        uuid portfolio_id FK
        decimal value
        datetime observed_at
    }

    ASSET {
        uuid id PK
        uuid portfolio_id FK
        uuid asset_type_id FK
        string name
        decimal quantity
        boolean disposed
        datetime created_at
        datetime updated_at
        string created_by
        string updated_by
    }

    ASSET_SNAPSHOT {
        uuid id PK
        uuid asset_id FK
        decimal value
        datetime observed_at
    }
    
    TRANSACTION {
        uuid id PK
        uuid asset_id FK
        string type
        decimal unit_price
        decimal quantity
        string currency
        datetime occurred_at
    }

    ASSET_TYPE {
        uuid id PK
        string code UK
        string label
        datetime created_at
        datetime updated_at
    }

    CATEGORY {
        uuid id PK
        string name UK
        uuid parent_id FK
    }

    TAG {
        uuid id PK
        string name UK
    }

    ASSET_CATEGORY {
        uuid asset_id FK
        uuid category_id FK
    }

    ASSET_TAG {
        uuid asset_id FK
        uuid tag_id FK
    }
```

## Conceptual Data Model

👉 Behavior-oriented

```mermaid
classDiagram

    class Portfolio {
        +id: UUID
        +name: str
        +base_currency: str
        +assets: List[Asset]
        +snapshots: List[PortfolioSnapshot]

        +total_value(at: datetime): Decimal
        +take_snapshot(at: datetime): PortfolioSnapshot
        +get_currency(): str
    }

    class AssetType {
        +id: UUID
        +code: str
        +label: str
    }

    class Category {
        +id: UUID
        +name: str
        +parent: Category?

        +get_hierarchy(): List[Category]
        +get_all_assets(): List[Asset]
    }

    class Asset {
        +id: UUID
        +name: str
        +asset_type: AssetType
        +portfolio: Portfolio
        +categories: Set[Category]
        +quantity: Decimal?
        +disposed: bool
        +created_at: datetime
        +updated_at: datetime
        +created_by: str
        +updated_by: str

        +transactions: List[Transaction]
        +snapshots: List[AssetSnapshot]
        +tags: Set[Tag]

        +current_value(at: datetime): Decimal
        +get_currency(): str
        +dispose(at: datetime): void
        +add_category(category: Category): void
        +remove_category(category: Category): void
    }

    class Transaction {
        +id: UUID
        +type: str
        +quantity: Decimal
        +unit_price: Decimal
        +currency: str
        +occurred_at: datetime
    }

    class AssetSnapshot {
        +id: UUID
        +value: Decimal
        +observed_at: datetime
        
        +get_currency(): str
    }

    class PortfolioSnapshot {
        +id: UUID
        +value: Decimal
        +observed_at: datetime
        
        +get_currency(): str
    }

    class Tag {
        +id: UUID
        +name: str
    }

    Portfolio "1" --> "*" Asset : owns
    Portfolio "1" --> "*" PortfolioSnapshot : tracks
    Asset "*" --> "1" AssetType : typed_as
    Asset "*" --> "1" Portfolio : belongs_to
    Asset "*" --> "*" Category : categorized_as
    Asset "1" --> "*" Transaction : has
    Asset "1" --> "*" AssetSnapshot : has
    Asset "*" --> "*" Tag : tagged_with
    Category "1" --> "*" Category : parent_of
```

## Transaction Types

- `ACQUIRE`: Buying/receiving an asset (increases quantity)
- `DISPOSE`: Selling/giving away an asset (decreases quantity)
- `ADJUST`: Manual correction/adjustment
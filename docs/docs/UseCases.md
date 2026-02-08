# Use Cases

This page illustrates the Asset data model with concrete, real-life examples.

## Examples

### 1.Checking Account

#### Scenario

You manually track your checking account balance.

#### Asset

| Field | Value |
|------|------|
| Name | Checking Account |
| Asset Type | CASH |
| Categories | Bank Accounts, Liquid Assets |
| Quantity | null |
| Disposed | false |
| Tags | liquidity, emergency_fund |

#### Transactions

No transactions (manual tracking only for now).

#### Balance Snapshots

| Snapshot Date | Value | Currency | Source |
|---------------|-------|----------|--------|
| 2024-01-01 | 10,000 | EUR | manual |
| 2024-02-01 | 10,450 | EUR | manual |
| 2024-03-01 | 9,800 | EUR | manual |

**Portfolio Valuation Rule**: Use the latest balance snapshot (€9,800).


### 2.Wardrobe

#### Scenario

You track your summer t-shirt collection. These t-shirts are both casual wear AND part of your workout clothes.

#### Asset

| Field | Value |
|------|------|
| Name | Summer T-Shirts Collection |
| Asset Type | PERSONAL_PROPERTY |
| Categories | Clothing > T-Shirts, Athletic Wear, Casual Wear |
| Quantity | 15 |
| Disposed | false |
| Tags | summer, cotton, breathable |

#### Transactions

| Date | Type | Quantity | Unit Price | Currency |
|------|------|----------|------------|----------|
| 2020-06-01 | ACQUIRE | 10 | 25 | EUR |
| 2023-08-15 | ACQUIRE | 5 | 30 | EUR |

#### Balance Snapshots

| Snapshot Date | Value | Currency | Source |
|---------------|-------|----------|--------|
| 2024-01-01 | 225 | EUR | manual |

!!! note "Asset belongs to THREE categories simultaneously"
    - Clothing > T-Shirts (hierarchy path)
    - Athletic Wear (cross-cutting category)
    - Casual Wear (cross-cutting category)

**Total acquisition cost**: €400 (10×25 + 5×30)  
**Current value**: €225 (depreciation tracked via snapshot)


### 3.Real Estate

#### Scenario

You buy an apartment that serves as both your primary residence AND a rental investment (you rent out one room on Airbnb).

#### Asset

| Field | Value |
|------|------|
| Name | Apartment Paris 11th |
| Asset Type | REAL_ESTATE |
| Categories | Real Estate > Residential > Apartments, Primary Residence, Income Generating Assets |
| Quantity | 1 |
| Disposed | true |
| Tags | paris, airbnb, partial_rental, sold |

#### Transactions

| Date | Type | Quantity | Unit Price | Currency |
|------|------|----------|------------|----------|
| 2015-05-10 | ACQUIRE | 1 | 300,000 | EUR |
| 2023-09-20 | DISPOSE | 1 | 420,000 | EUR |

#### Balance Snapshots (Historical)

| Snapshot Date | Value | Currency | Source |
|---------------|-------|----------|--------|
| 2018-01-01 | 330,000 | EUR | manual |
| 2021-01-01 | 380,000 | EUR | manual |

!!! note "Asset belongs to THREE categories simultaneously"
    - Real Estate > Residential > Apartments (hierarchy path)
    - Primary Residence (legal classification)
    - Income Generating Assets (functional classification)

**Realized gain**: €120,000 (€420k - €300k)

### 4. LEGO Set

#### Scenario

You found a LEGO Star Wars set at home. It's both a collectible investment AND part of your children's toy collection.

#### Asset

| Field | Value |
|------|------|
| Name | LEGO Star Wars Millennium Falcon |
| Asset Type | PERSONAL_PROPERTY |
| Categories | Toys > Building Sets > LEGO, Collectibles > Investment Grade, Kids Room Items |
| Quantity | 1 |
| Disposed | false |
| Tags | star_wars, vintage, unopened, appreciating |

#### Transactions

| Date | Type | Quantity | Unit Price | Currency |
|------|------|----------|------------|----------|
| 2022-08-15 | ACQUIRE | 1 | 0 | EUR |

#### Balance Snapshots

| Snapshot Date | Value | Currency | Source |
|---------------|-------|----------|--------|
| 2024-01-01 | 350 | EUR | manual |

**Acquisition price**: €0 (found item)  
**Current market value**: €350

### 5. Household Furniture

Useful with bulk items.

#### Scenario

You own 10 identical wooden chairs that serve multiple purposes: dining, office workspace, and guest seating.

#### Asset

| Field | Value |
|------|------|
| Name | Wooden Dining Chairs |
| Asset Type | PERSONAL_PROPERTY |
| Categories | Home > Furniture > Dining, Office Equipment, Multi-Purpose Items |
| Quantity | 10 |
| Disposed | false |
| Tags | wood, stackable, versatile |

#### Transactions

| Date | Type | Quantity | Unit Price | Currency |
|------|------|----------|------------|----------|
| 2020-06-01 | ACQUIRE | 10 | 40 | EUR |

#### Balance Snapshots

| Snapshot Date | Value | Currency | Source |
|---------------|-------|----------|--------|
| 2024-01-01 | 300 | EUR | manual |

!!! note "Asset belongs to THREE categories simultaneously"
    - Home > Furniture > Dining (primary use)
    - Office Equipment (secondary use)
    - Multi-Purpose Items (functional classification)

**Total acquisition cost**: €400 (10×40)  
**Current value**: €300 (25% depreciation)

### 6. Mortgage Loan (Liability)

#### Scenario

You have a mortgage loan on your primary residence. This is a **liability** (negative asset).

#### Asset

| Field | Value |
|------|------|
| Name | Mortgage - Paris Apartment |
| Asset Type | LOAN |
| Categories | Liabilities > Real Estate Loans, Long-Term Debt |
| Quantity | null |
| Disposed | false |
| Tags | mortgage, primary_residence, fixed_rate |

#### Transactions

| Date | Type | Quantity | Unit Price | Currency | Notes |
|------|------|----------|------------|----------|-------|
| 2015-05-10 | ACQUIRE | 1 | -250,000 | EUR | Initial loan |
| 2016-01-01 | DISPOSE | 1 | 5,000 | EUR | Principal payment |
| 2017-01-01 | DISPOSE | 1 | 5,200 | EUR | Principal payment |
| 2018-01-01 | DISPOSE | 1 | 5,400 | EUR | Principal payment |

#### Balance Snapshots

| Snapshot Date | Value | Currency | Source | Notes |
|---------------|-------|----------|--------|-------|
| 2024-01-01 | -220,000 | EUR | manual | Remaining debt |
| 2024-02-01 | -219,500 | EUR | manual | After payment |

!!! note "Key Points"
    - Initial acquisition is **negative** (-€250,000 = you owe this)
    - DISPOSE transactions are **positive** (principal payments reduce the debt)
    - Balance snapshots are **negative** (current debt owed)
    - Portfolio valuation: This **subtracts** from total net worth

## Liabilities

**Liabilities are assets with negative values:**

| Asset Type | Typical Balance | Portfolio Impact |
|-----------|----------------|------------------|
| CASH | Positive | Increases net worth |
| REAL_ESTATE | Positive | Increases net worth |
| LOAN | Negative | Decreases net worth |
| CREDIT_CARD | Negative | Decreases net worth |
| MORTGAGE | Negative | Decreases net worth |

**Portfolio Calculation:**

```
Net Worth = Sum of all asset balances (positive + negative)

Example:
  Checking Account:     +€10,000
  Paris Apartment:     +€420,000
  Mortgage Loan:       -€220,000
  ────────────────────────────────
  Net Worth:           +€210,000
```

### Transaction Logic

**For a LOAN asset:**

- `ACQUIRE` with negative unit_price = Taking out a loan (you owe money)
- `DISPOSE` with positive unit_price = Paying off principal (reducing debt)

**Example Flow:**

```
2015-05-10: ACQUIRE 1 × -€250,000 = -€250,000 (loan originated)
2016-01-01: DISPOSE 1 × +€5,000   = -€245,000 (paid €5k principal)
2017-01-01: DISPOSE 1 × +€5,200   = -€239,800 (paid €5.2k principal)
```

## Complete Picture

**Assets (Positive):**

- Checking Account: €10,000
- Paris Apartment: €420,000

**Liabilities (Negative):**

- Mortgage Loan: -€220,000
- Credit Card: -€2,000

**Net Worth:**

€10,000 + €420,000 - €220,000 - €2,000 = **€208,000**

This is tracked in Portfolio Snapshots.

## Portfolio Example

All assets combined into a portfolio view.

### Portfolio: "My Personal Wealth"

| Asset Name | Asset Type | Categories | Current Value | Currency |
|-----------|-----------|------------|---------------|----------|
| Checking Account | CASH | Bank Accounts, Liquid Assets | 9,800 | EUR |
| Summer T-Shirts | PERSONAL_PROPERTY | Clothing > T-Shirts, Athletic Wear, Casual Wear | 225 | EUR |
| Apartment Paris | REAL_ESTATE | Residential > Apartments, Primary Residence, Income Generating | 0 | EUR |
| LEGO Millennium Falcon | PERSONAL_PROPERTY | Toys > LEGO, Collectibles, Kids Room | 350 | EUR |
| Wooden Chairs | PERSONAL_PROPERTY | Furniture > Dining, Office Equipment, Multi-Purpose | 300 | EUR |

### Portfolio Snapshot

| Snapshot Date | Total Value | Currency |
|---------------|-------------|----------|
| 2024-01-01 | 10,675 | EUR |

!!! note "Apartment is disposed (sold), so its current value is €0 in the portfolio."

## Category in Action

Categories let you organize and filter assets.

!!! note "Asset belongs to THREE categories simultaneously"
    - Toys > Building Sets > LEGO (what it is)
    - Collectibles > Investment Grade (how you treat it)
    - Kids Room Items (where it's stored)

!!! example "Filtering by "Income Generating Assets""
    - Apartment Paris 11th (partial Airbnb rental)

!!! example "Filtering by "Multi-Purpose Items""
    - Wooden Dining Chairs (used for dining, office, guests)

!!! example "Filtering by "Collectibles""
    - LEGO Star Wars Millennium Falcon

One asset can appear in multiple organizational contexts without duplication.
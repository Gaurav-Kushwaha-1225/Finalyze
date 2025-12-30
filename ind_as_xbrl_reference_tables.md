# IND AS XBRL: Quick Reference & Lookup Tables

## Table of Contents
1. [Complete Element Reference](#complete-element-reference)
2. [Extended Link Roles (ELRs) Directory](#extended-link-roles-elrs-directory)
3. [Dimension & Member Reference](#dimension-member-reference)
4. [Ind AS Cross-Reference](#ind-as-cross-reference)
5. [Data Types & Units](#data-types-units)
6. [File Format & Naming](#file-format-naming)
7. [Validation Rules Quick Lookup](#validation-rules-quick-lookup)

---

## Complete Element Reference

### Balance Sheet Elements (Instant - Stock Items)

#### ASSET ELEMENTS

**Non-Current Assets:**
```
ind-as:PropertyPlantAndEquipment
  - Type: Monetary (INR)
  - Definition: Tangible assets > 1 year useful life
  - Ind AS: 16
  - ELR: [110000] Balance Sheet

ind-as:InvestmentProperty
  - Type: Monetary (INR)
  - Definition: Real estate held for income/appreciation
  - Ind AS: 40
  - ELR: [110000] Balance Sheet

ind-as:GoodwillAssets
  - Type: Monetary (INR)
  - Definition: Premium paid in business combination
  - Ind AS: 38/103
  - ELR: [110000] Balance Sheet
  - Note: Typically in DisclosureOfGoodwillTable

ind-as:IntangibleAssets
  - Type: Monetary (INR)
  - Definition: Identifiable non-monetary assets (patents, software)
  - Ind AS: 38
  - ELR: [110000] Balance Sheet
  - Dimensional: ClassesOfIntangibleAssetsAxis

ind-as:OtherIntangibleAssets
  - Type: Monetary (INR)
  - Definition: Unidentified intangibles, catch-all category
  - Ind AS: 38
  - ELR: [110000] Balance Sheet
  - Dimensional: ClassesOfOtherIntangibleAssetsAxis (Licenses, Trademarks, Patents, Software)

ind-as:FinancialAssetsNoncurrent
  - Type: Monetary (INR)
  - Definition: Long-term investments in equities, bonds
  - Ind AS: 109
  - ELR: [110000] Balance Sheet
  - Dimensional: TypesOfFinancialAssetsAxis

ind-as:InvestmentInAssociate
  - Type: Monetary (INR)
  - Definition: Equity-accounted investments (20-50% ownership)
  - Ind AS: 28
  - ELR: [110000] Balance Sheet

ind-as:BiologicalAssets
  - Type: Monetary (INR)
  - Definition: Living animals/plants
  - Ind AS: 41
  - ELR: [110000] Balance Sheet

ind-as:DeferredTaxAssets
  - Type: Monetary (INR)
  - Definition: Future tax benefits from temporary differences
  - Ind AS: 12
  - ELR: [110000] Balance Sheet

**Current Assets:**
```
ind-as:Inventories
  - Type: Monetary (INR)
  - Definition: Goods held for sale or consumption
  - Ind AS: 2
  - ELR: [110000] Balance Sheet

ind-as:TradeReceivables
  - Type: Monetary (INR)
  - Definition: Amounts due from customers
  - Ind AS: 109
  - ELR: [110000] Balance Sheet
  - Note: Net of allowances/provisions

ind-as:CashAndCashEquivalents
  - Type: Monetary (INR)
  - Definition: Cash, bank balances, liquid investments < 3 months
  - Ind AS: 7
  - ELR: [110000] Balance Sheet

ind-as:OtherFinancialAssets (Current)
  - Type: Monetary (INR)
  - Definition: Short-term financial investments
  - Ind AS: 109
  - ELR: [110000] Balance Sheet

ind-as:OtherCurrentAssets
  - Type: Monetary (INR)
  - Definition: Prepayments, advances, other non-financial assets
  - Ind AS: 1
  - ELR: [110000] Balance Sheet

ind-as:AssetsHeldForSale
  - Type: Monetary (INR)
  - Definition: Non-current assets classified as held for sale
  - Ind AS: 105
  - ELR: [110000] Balance Sheet
```

#### LIABILITY ELEMENTS

**Non-Current Liabilities:**
```
ind-as:BorrowingsNoncurrent
  - Type: Monetary (INR)
  - Definition: Long-term loans, bonds, debentures
  - Ind AS: 109/123
  - ELR: [120000] Balance Sheet
  - Dimensional: ClassificationOfBorrowingsAxis

ind-as:OtherFinancialLiabilitiesNoncurrent
  - Type: Monetary (INR)
  - Definition: Lease obligations, derivative liabilities, accruals
  - Ind AS: 109/116
  - ELR: [120000] Balance Sheet

ind-as:ProvisionsNoncurrent
  - Type: Monetary (INR)
  - Definition: Estimated long-term obligations (pensions, warranties)
  - Ind AS: 37
  - ELR: [120000] Balance Sheet
  - Dimensional: ClassesOfProvisionsAxis

ind-as:DeferredTaxLiabilities
  - Type: Monetary (INR)
  - Definition: Future tax payable from temporary differences
  - Ind AS: 12
  - ELR: [120000] Balance Sheet

ind-as:OtherNoncurrentLiabilities
  - Type: Monetary (INR)
  - Definition: Deferred income, contingencies, other long-term obligations
  - Ind AS: 1
  - ELR: [120000] Balance Sheet

**Current Liabilities:**
```
ind-as:BorrowingsCurrent
  - Type: Monetary (INR)
  - Definition: Short-term loans due within 12 months
  - Ind AS: 109/123
  - ELR: [120000] Balance Sheet
  - Dimensional: ClassificationOfBorrowingsAxis

ind-as:TradePayables
  - Type: Monetary (INR)
  - Definition: Amounts due to suppliers
  - Ind AS: 109
  - ELR: [120000] Balance Sheet

ind-as:CurrentTaxLiabilities
  - Type: Monetary (INR)
  - Definition: Income tax provision for current year
  - Ind AS: 12
  - ELR: [120000] Balance Sheet

ind-as:ProvisionsCurrent
  - Type: Monetary (INR)
  - Definition: Short-term estimated obligations (bonuses, vacation)
  - Ind AS: 37
  - ELR: [120000] Balance Sheet
  - Dimensional: ClassesOfProvisionsAxis

ind-as:OtherFinancialLiabilitiesCurrent
  - Type: Monetary (INR)
  - Definition: Accrued expenses, short-term lease liabilities
  - Ind AS: 109/116
  - ELR: [120000] Balance Sheet

ind-as:OtherCurrentLiabilities
  - Type: Monetary (INR)
  - Definition: Deferred revenue, statutory liabilities
  - Ind AS: 1
  - ELR: [120000] Balance Sheet
```

#### EQUITY ELEMENTS

```
ind-as:ShareCapital
  - Type: Monetary (INR)
  - Definition: Issued equity share capital
  - Ind AS: 32
  - ELR: [120000] Balance Sheet
  - Dimensional: DetailsOfShareCapitalAxis

ind-as:PreferenceShareCapital
  - Type: Monetary (INR)
  - Definition: Issued preference share capital
  - Ind AS: 32
  - ELR: [120000] Balance Sheet

ind-as:ReservesAndSurplus
  - Type: Monetary (INR)
  - Definition: Retained earnings, statutory reserves, revaluation reserves
  - Ind AS: 32
  - ELR: [120000] Balance Sheet
  - Dimensional: ClassesOfReservesAxis

ind-as:TreasuryStock
  - Type: Monetary (INR)
  - Definition: Repurchased own shares (negative equity)
  - Ind AS: 32
  - ELR: [120000] Balance Sheet

ind-as:NonControllingInterests
  - Type: Monetary (INR)
  - Definition: Minority interest in consolidated subsidiaries
  - Ind AS: 110
  - ELR: [120000] Balance Sheet

ind-as:OtherComprehensiveIncome
  - Type: Monetary (INR)
  - Definition: Cumulative OCI items (hedging, translation, revaluation)
  - Ind AS: 1
  - ELR: [120000] Balance Sheet
```

---

### P&L / Income Statement Elements (Duration - Flow Items)

```
ind-as:RevenueFromOperations
  - Type: Monetary (INR)
  - Definition: Main business revenue
  - Ind AS: 115/18
  - ELR: [200000] Income Statement
  - Dimensional: ClassesOfRevenueAxis (Product/Service breakdown)

ind-as:OtherIncome
  - Type: Monetary (INR)
  - Definition: Non-operating income (interest, dividends, gains)
  - Ind AS: 1
  - ELR: [200000] Income Statement

ind-as:CostOfMaterialsConsumed
  - Type: Monetary (INR)
  - Definition: Cost of raw materials used in production
  - Ind AS: 2
  - ELR: [200000] Income Statement

ind-as:EmployeeBenefitExpense
  - Type: Monetary (INR)
  - Definition: Salaries, wages, bonuses, benefits
  - Ind AS: 19
  - ELR: [200000] Income Statement

ind-as:DepreciationAndAmortization
  - Type: Monetary (INR)
  - Definition: Systematic write-down of PPE and intangibles
  - Ind AS: 16/38
  - ELR: [200000] Income Statement

ind-as:FinanceCosts
  - Type: Monetary (INR)
  - Definition: Interest expense, borrowing costs
  - Ind AS: 109/123
  - ELR: [200000] Income Statement

ind-as:OtherExpense
  - Type: Monetary (INR)
  - Definition: General operating expenses
  - Ind AS: 1
  - ELR: [200000] Income Statement

ind-as:ProfitBeforeTax
  - Type: Monetary (INR)
  - Definition: Operating profit before taxes
  - Ind AS: 1
  - ELR: [200000] Income Statement
  - Calculation: Revenue - Expenses (before tax)

ind-as:TaxExpense
  - Type: Monetary (INR)
  - Definition: Current + deferred income tax
  - Ind AS: 12
  - ELR: [200000] Income Statement
  - Dimensional: TypesOfTaxExpenseAxis

ind-as:NetProfitLoss
  - Type: Monetary (INR)
  - Definition: Profit after tax (earnings)
  - Ind AS: 1
  - ELR: [200000] Income Statement
  - Calculation: Profit Before Tax - Tax Expense

ind-as:OtherComprehensiveIncomeNotReclassifiedSubsequentlyToProfitOrLoss
  - Type: Monetary (INR)
  - Definition: Actuarial gains, revaluation gains (permanent OCI)
  - Ind AS: 1
  - ELR: [200000] Income Statement

ind-as:OtherComprehensiveIncomeWillBeReclassifiedSubsequentlyToProfitOrLoss
  - Type: Monetary (INR)
  - Definition: Hedging gains, translation differences (temporary OCI)
  - Ind AS: 1
  - ELR: [200000] Income Statement

ind-as:ComprehensiveIncome
  - Type: Monetary (INR)
  - Definition: Net Profit + OCI total
  - Ind AS: 1
  - ELR: [200000] Income Statement
```

---

### Cash Flow Statement Elements (Duration - Flow Items)

```
ind-as:CashGeneratedFromOperations
  - Type: Monetary (INR)
  - Definition: Net cash from operating activities
  - Ind AS: 7
  - ELR: [300000] Cash Flow
  - Method: Indirect (PnL adjustments) or Direct

ind-as:CashFlowsFromInvestingActivities
  - Type: Monetary (INR)
  - Definition: Net cash from investing (capital expenditure, asset sales)
  - Ind AS: 7
  - ELR: [300000] Cash Flow

ind-as:CashFlowsFromFinancingActivities
  - Type: Monetary (INR)
  - Definition: Net cash from financing (borrowings, dividends)
  - Ind AS: 7
  - ELR: [300000] Cash Flow

ind-as:IncreaseDecreaseInCashAndCashEquivalents
  - Type: Monetary (INR)
  - Definition: Net change in cash (Operating + Investing + Financing)
  - Ind AS: 7
  - ELR: [300000] Cash Flow

ind-as:CashAndCashEquivalentsAtBeginningOfPeriod
  - Type: Monetary (INR)
  - Definition: Opening cash balance
  - Ind AS: 7
  - ELR: [300000] Cash Flow

ind-as:CashAndCashEquivalentsAtEndOfPeriod
  - Type: Monetary (INR)
  - Definition: Closing cash balance
  - Ind AS: 7
  - ELR: [300000] Cash Flow
```

---

## Extended Link Roles (ELRs) Directory

### Balance Sheet ELRs

| ELR Code | Description | Contexts | Key Elements |
|----------|-------------|----------|--------------|
| [100000] | Balance Sheet - Assets | Instant | All current & non-current assets |
| [110000] | Balance Sheet - Main (Asset Side) | Instant | Cash, Receivables, PPE, Intangibles |
| [120000] | Balance Sheet - Liabilities & Equity | Instant | Borrowings, Payables, Share Capital |
| [130000] | Balance Sheet Opening (Ind AS Adoption) | Instant | All B/S items for 01-Apr-2015 |

### Income Statement ELRs

| ELR Code | Description | Contexts | Key Elements |
|----------|-------------|----------|--------------|
| [200000] | Income Statement [Main] | Duration | Revenue, Expenses, Profit, OCI |
| [210000] | P&L - Quarterly Reporting | Duration | Same as [200000] for Q1-Q4 |

### Cash Flow ELRs

| ELR Code | Description | Contexts | Key Elements |
|----------|-------------|----------|--------------|
| [300000] | Statement of Cash Flows | Duration | Operating, Investing, Financing activities |

### Disclosure/Notes ELRs

| ELR Code | Description | Type | Dimensional |
|----------|-------------|------|-------------|
| [400000] | Disclosures - General Information | Table | Entity, Period |
| [400100] | Property, Plant & Equipment Details | Table | Classes, Movement schedule |
| [400200] | Investment Property | Table | Classes, Gross/Accumulated |
| [400300] | Inventories | Table | Classes breakdown |
| [400400] | Trade Receivables | Table | Aging analysis |
| [400500] | Borrowings | Table | Type, Rate, Maturity |
| [400600] | Equity Details | Table | Capital, Reserves classes |
| [400700] | Lease Information | Table | Right-of-use details |
| [400800] | Investments | Table | Type, Fair value |
| [400900] | Intangible Assets | Table | Classes (Goodwill, Licenses, Patents) |
| [401000] | Related Parties | Table | Transactions, Balances |
| [401100] | Segment Information | Table | Revenue, Assets by segment |
| [401200] | Director Information | Table | DIN, Designation, Appointment |
| [401300] | Audit Remarks | Table | Qualifications, Reservations |

---

## Dimension & Member Reference

### Explicit Dimensions (Pre-defined Members)

#### ClassesOfOtherIntangibleAssetsAxis
```
Parent Members:
├── CompanyOtherIntangibleAssetsMember
    ├── PatentsMember
    ├── LicensesAndFranchiseMember
    │   ├── LicensesMember (e.g., Spectrum)
    │   └── FranchisesMember
    ├── BrandsAndTradeMarksMember
    ├── SoftwareAndSystemsMember
    ├── CopyrightsMember
    └── OtherIntangibleAssetsMember
```

#### ClassificationOfBorrowingsAxis
```
├── SecuredBorrowingsMember
│   ├── TermLoansFromBanksMember
│   ├── WorkingCapitalLoansFromBanksMember
│   └── VehicleLoansFromBanksMember
└── UnsecuredBorrowingsMember
    ├── TermLoansFromOthersMember
    ├── BondsMember
    └── DevelopmentLoansMember
```

#### ClassesOfReservesAxis
```
├── CapitalReserveMember
├── GeneralReserveMember
├── SecuritiesPremiumReserveMember
├── RetainedEarningsMember
├── RevaluationReserveMember
└── OtherReserveMember
```

#### TypesOfTaxExpenseAxis
```
├── CurrentTaxExpenseMember
└── DeferredTaxExpenseMember
```

#### ClassesOfProvisionsAxis
```
├── ProvisionForEmployeeBenefitsMember
├── ProvisionForWarrantiesAndGaranteesMember
├── ProvisionForRestructuringMember
├── ProvisionForDeprecationOfAssetsMember
└── OtherProvisionsMember
```

---

### Typed Dimensions (User-defined Members)

#### DetailsOfDirectorsSigningFinancialStatementsAxis
```
Members: Director1Member, Director2Member, ... DirectorNMember

Associated Elements:
├── NameOfDirector (string)
├── DINOfDirector (integer)
├── DesignationOfDirector (enumeration)
├── DateOfAppointmentOfDirector (date)
└── DateOfCessationOfDirector (date, optional)
```

#### DetailsOfAuditorsAxis
```
Members: Auditor1Member, Auditor2Member

Associated Elements:
├── NameOfAuditor (string)
├── AddressOfAuditor (string)
├── MembershipNumberOfAuditor (integer)
└── RemunerationOfAuditor (monetary)
```

---

## Ind AS Cross-Reference

### Complete Mapping of IND AS to XBRL Elements

| Ind AS Standard | Key Topic | Primary XBRL Elements | ELR |
|---|---|---|---|
| **Ind AS 1** | Presentation of Financial Statements | Balance Sheet, P&L, Cash Flow structure | [100000], [200000], [300000] |
| **Ind AS 2** | Inventories | `Inventories` | [110000] |
| **Ind AS 7** | Statement of Cash Flows | `CashGeneratedFromOperations`, `CashFlowsFromInvestingActivities` | [300000] |
| **Ind AS 8** | Accounting Policies, Changes, Errors | Disclosure tables | [400000] |
| **Ind AS 10** | Events After Reporting Period | Disclosure notes | [400000] |
| **Ind AS 12** | Income Taxes | `DeferredTaxAssets`, `DeferredTaxLiabilities`, `TaxExpense` | [110000], [120000], [200000] |
| **Ind AS 16** | PPE | `PropertyPlantAndEquipment` + `DisclosureOfPropertyPlantAndEquipmentTable` | [110000], [400100] |
| **Ind AS 18** | Revenue | `RevenueFromOperations` | [200000] |
| **Ind AS 19** | Employee Benefits | `EmployeeBenefitExpense`, Pension disclosure tables | [200000], [401400] |
| **Ind AS 20** | Govt Grants | Disclosure notes | [400000] |
| **Ind AS 21** | Foreign Exchange | Translation differences in OCI | [200000] |
| **Ind AS 23** | Borrowing Costs | Capitalized interest in PPE notes | [400100] |
| **Ind AS 27** | Separate Financial Statements | Standalone P/L structures | [200000] |
| **Ind AS 28** | Investments in Associates | `InvestmentInAssociate` | [110000] |
| **Ind AS 29** | Financial Reporting in Hyperinflationary Economies | Adjustment disclosures | [400000] |
| **Ind AS 32** | Financial Instruments - Presentation | Share capital, equity components | [120000] |
| **Ind AS 34** | Interim Financial Reporting | Quarterly reporting structures | [210000] |
| **Ind AS 36** | Impairment of Assets | Impairment losses, write-downs | [400000] |
| **Ind AS 37** | Provisions, Contingent Liabilities | `Provisions` + detailed tables | [120000], [401500] |
| **Ind AS 38** | Intangible Assets | `IntangibleAssets`, `OtherIntangibleAssets` + tables | [110000], [400900] |
| **Ind AS 40** | Investment Property | `InvestmentProperty` | [110000] |
| **Ind AS 41** | Agriculture | `BiologicalAssets` | [110000] |
| **Ind AS 103** | Business Combinations | `Goodwill`, `OtherIntangibleAssets` | [400900] |
| **Ind AS 105** | Non-Current Assets Held for Sale | `AssetsHeldForSale` | [110000] |
| **Ind AS 108** | Operating Segments | Segment disclosure tables | [401100] |
| **Ind AS 109** | Financial Instruments - Recognition | Investment tables, receivables/payables | [400000-409999] |
| **Ind AS 110** | Consolidated Financial Statements | Non-controlling interests | [120000] |
| **Ind AS 111** | Joint Arrangements | Joint venture disclosures | [400000] |
| **Ind AS 115** | Revenue from Contracts | Revenue breakdown by class | [400000] |
| **Ind AS 116** | Leases | Right-of-use assets, lease liabilities | [110000], [120000], [400700] |

---

## Data Types & Units

### Standard Data Types

| Data Type | Examples | Valid Values | XML Declaration |
|-----------|----------|--------------|-----------------|
| **Monetary** | Amounts in currency | Any decimal number | `unitRef="INR"` |
| **Numeric (Pure)** | Percentages, ratios | 0 to 1 (for percentages) | `unitRef="pure"` |
| **Numeric (Count)** | Shares, units | Whole numbers only | `unitRef="shares"` |
| **Date** | Period end dates | YYYY-MM-DD format | No unit needed |
| **String** | Text, descriptions | Any characters (HTML-safe) | No unit needed |
| **Boolean** | Yes/No flags | "true" or "false" | No unit needed |
| **Enumeration** | Categorical values | Pre-defined set | No unit needed |

### Standard Units

| Unit | Symbol | Use Case | Code |
|------|--------|----------|------|
| **INR** | ₹ | Indian Rupee amounts | `iso4217:INR` |
| **USD** | $ | US Dollar amounts (subsidiary) | `iso4217:USD` |
| **EUR** | € | Euro amounts (subsidiary) | `iso4217:EUR` |
| **Pure** | (none) | Percentages, ratios | `xbrli:pure` |
| **Shares** | (none) | Number of shares | `xbrli:shares` |

### Common Percentage Conversions

| Percentage | Decimal | XBRL Value |
|-----------|---------|-----------|
| 0% | 0.00 | 0 |
| 5% | 0.05 | 0.05 |
| 50% | 0.50 | 0.5 |
| 100% | 1.00 | 1 |
| 150% | 1.50 | 1.5 |

---

## File Format & Naming

### Instance Document File Naming Convention

```
Pattern: {CompanyNameOrCIN}_{ReportType}_{Period}.xml

Examples:
XYZ_Limited_IndAS_Standalone_2017-03-31.xml
U24251MH2010PLC203456_IndAS_Consolidated_2017-03-31.xml

ReportTypes:
- Standalone
- Consolidated

Period:
- Calendar year end: 2017-03-31 (YYYY-MM-DD)
- Fiscal year: FullDate or Year format
```

### Schema Reference (Mandatory)

```xml
<link:schemaRef 
  xlink:href="http://www.mca.gov.in/XBRL/2017/07/16/Taxonomy/Ind/in-ci-ent-2017-03-31.xsd"
  xlink:type="simple"/>
```

### Encoding Specification

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- UTF-8 is mandatory per MCA Filing Manual -->
```

---

## Validation Rules Quick Lookup

### Mandatory Financial Statement Elements by ELR

| ELR | Minimum Mandatory Elements | Count |
|-----|---------------------------|-------|
| [110000] Balance Sheet | All line items per Ind AS 1 | 20+ |
| [200000] P&L | Revenue, Expenses, Profit, Tax | 10+ |
| [300000] Cash Flow | Operating, Investing, Financing | 3 |
| [400000] Disclosures | Company info, accounting policies | Varies |

### Calculation Validation Rules

#### Balance Sheet
```
✓ Total Assets = Current Assets + Non-Current Assets
✓ Total Liabilities & Equity = Current Liabilities + Non-Current Liabilities + Equity
✓ Current Assets = Cash + Receivables + Inventory + Other Current
✓ Non-Current Assets = PPE + Intangibles + Investments + Other Non-Current
```

#### P&L
```
✓ Gross Profit = Revenue - Cost of Materials
✓ EBITDA = PBT + Finance Costs + Depreciation
✓ PBT = Revenue - Total Expenses (before tax)
✓ Net Profit = PBT - Tax Expense
✓ Total Comprehensive Income = Net Profit + OCI
```

#### Cash Flow
```
✓ Closing Cash = Opening Cash + Operating CF + Investing CF + Financing CF
✓ Net Cash from Operations ≥ 0 (ideally)
✓ Capital Expenditure ≥ 0 (outflow)
✓ Borrowing Net = Proceeds - Repayments
```

### Common Validation Errors - Quick Fix Table

| Error Message | Data Type | Fix |
|---|---|---|
| "Not a valid value for date" | Date | Use YYYY-MM-DD |
| "Decimal not valid for integer" | Integer | Remove decimals |
| "'yes' not valid for boolean" | Boolean | Use "true" or "false" |
| "Value must be between 0-1" | Percentage | Convert to decimal (60% = 0.6) |
| "Unit not defined for X" | Monetary | Add proper unit (INR, USD) |
| "Duplicate context" | Context | Merge or rename contexts |
| "Element X required" | Mandatory | Add missing element |

---

## Quick Checklists

### Before Validation
- [ ] Current year + previous year data entered
- [ ] Opening balance (if Ind AS adoption year)
- [ ] All amounts in INR (or documented exception)
- [ ] Dates in YYYY-MM-DD format
- [ ] Context CIN correct
- [ ] Company name correct

### After Validation
- [ ] No errors (only warnings acceptable)
- [ ] PDF export successful
- [ ] PDF matches published financial statements
- [ ] Pre-scrutiny completed
- [ ] No dimensional validation errors

### Before Filing
- [ ] Validated instance document ready
- [ ] Form AOC-4 XBRL prepared
- [ ] Authorized person identified
- [ ] Digital signature available
- [ ] Filing deadline noted
- [ ] Backup copy of all documents

---

**Document Version**: 1.0 Quick Reference  
**Last Updated**: December 2025  
**Status**: Complete lookup tables for IND AS XBRL 2017 Taxonomy  
**Applicability**: All IND AS reporting entities


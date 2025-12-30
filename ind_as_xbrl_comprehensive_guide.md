# IND AS XBRL Taxonomy: Comprehensive Understanding Guide

## Table of Contents
1. [Introduction to IND AS XBRL](#introduction-to-ind-as-xbrl)
2. [Taxonomy Overview](#taxonomy-overview)
3. [Core Taxonomy Components](#core-taxonomy-components)
4. [Linkbase Architecture](#linkbase-architecture)
5. [Financial Statement Mappings](#financial-statement-mappings)
6. [Dimensional Modeling](#dimensional-modeling)
7. [Tag Identification Methodology](#tag-identification-methodology)
8. [XBRL Instance Document Specifications](#xbrl-instance-document-specifications)
9. [Business Rules & Validation](#business-rules-validation)
10. [Common Element Mappings](#common-element-mappings)

---

## Introduction to IND AS XBRL

### What is IND AS XBRL?

IND AS XBRL is the standardized format for reporting financial statements prepared under Indian Accounting Standards (Ind AS) using eXtensible Business Reporting Language (XBRL). It enables:

- **Structured Financial Reporting**: Machine-readable financial data
- **Regulatory Compliance**: Mandatory filing format for Indian companies with MCA
- **Data Comparability**: Standardized taxonomy across organizations
- **Automated Processing**: Digital analysis and aggregation of financial data

### Regulatory Framework

- **Release Version**: 2017-03-31 (IND-AS 2017)
- **Authority**: Ministry of Corporate Affairs (MCA), Government of India
- **Mandatory For**: All companies filing financial statements under Companies Act, 2013
- **Implementation**: Standalone and Consolidated Financial Statements (FY 2015-16 onwards)

---

## Taxonomy Overview

### Taxonomy Statistics

| Metric | Value |
|--------|-------|
| Total Concepts/Elements | 3,187 |
| Extended Links (ELR) | 57 |
| Tuples | 24 |
| Predefined Rules | 361 |
| Linkbase Types | 6 (Label, Presentation, Calculation, Definition, Reference, Formula) |

### Taxonomy Namespace

```
http://www.xbrl.org/in/2017-03-31/ind-as
Prefix: ind-as_
Example: ind-as_PropertyPlantAndEquipment
```

### Taxonomy File Reference

**Schema Reference URL** (for instance documents):
```xml
http://www.mca.gov.in/XBRL/2017/07/16/Taxonomy/Ind/in-ci-ent-2017-03-31.xsd
```

---

## Core Taxonomy Components

### 1. Concepts (Elements)

Concepts are the fundamental building blocks representing financial data items.

**Types of Concepts:**

| Concept Type | Purpose | Examples |
|---|---|---|
| **Monetary Items** | Currency values | Revenue, Assets, Liabilities |
| **Numeric Items** | Non-monetary numbers | Quantity, Percentage (0-1), EPS |
| **Instant Items** | Point-in-time (stock) | Assets, Liabilities, Cash |
| **Duration Items** | Period-based (flow) | Revenue, Expenses, Cash Flow |
| **Non-Numeric Items** | Text/strings | Descriptions, Names, Addresses |

**Concept Naming Convention:**
```
ind-as_{ConceptName}
Examples:
- ind-as_PropertyPlantAndEquipment
- ind-as_Cash
- ind-as_RevenueFromOperations
- ind-as_NetProfitLoss
```

### 2. Dimensions (Axes)

Dimensions add context to facts by categorizing data along multiple axes.

**Types of Dimensions:**

| Type | Definition | Examples |
|---|---|---|
| **Explicit Dimensions** | Pre-defined domain members | Entity, Product Type, Customer Type |
| **Typed Dimensions** | User-defined values | Director Name, Address, Company Details |
| **Core Dimensions** | Standard XBRL dimensions | Period, Entity, Unit |

**Common Dimension Examples:**
```
- ClassesOfOtherIntangibleAssetsAxis → {Goodwill, Patents, Licenses, Trademarks, Software}
- TypesOfBorrowingsAxis → {TermLoans, WorkingCapitalLoans, Bonds}
- GeographicSegmentAxis → {DomesticSegment, InternationalSegment}
- ProductLineAxis → {Product1Member, Product2Member, Product3Member}
```

### 3. Members & Domain Values

Members are specific values that fill a dimensional axis.

**Example Hierarchy:**
```
ClassesOfOtherIntangibleAssetsAxis
├── Goodwill
├── LicensesAndFranchise
│   └── LicensesMember (Spectrum example)
├── PatentsMember
└── BrandsAndTradeMarksMember
```

---

## Linkbase Architecture

Linkbases define relationships between concepts and provide metadata.

### 1. Label Linkbase (Label Link Roles)

**Purpose**: Human-readable labels for concepts
**File**: `ind-as-label-2017-03-31.xml`

**Content**:
```xml
<link:labelLink>
  <link:loc xlink:href="schema#ind-as_PropertyPlantAndEquipment" xlink:label="label_ppe"/>
  <link:label xlink:label="label_ppe" xml:lang="en">
    Property, plant and equipment
  </link:label>
</link:labelLink>
```

**Characteristics**:
- Standard English labels matching Ind AS terminology
- Searchable for exact PDF text matches
- Critical for initial tag identification

### 2. Presentation Linkbase (Report Structure)

**Purpose**: Hierarchical organization of elements in financial reports
**File**: `ind-as-pre-2017-03-31-{XXXXXX}.xml` (varies by report type)

**Key Extended Link Roles (ELRs)**:
```
[100000] Balance Sheet - Assets Section
[110000] Balance Sheet - Main
[120000] Balance Sheet - Liabilities & Equity
[200000] Statement of Profit & Loss
[300000] Statement of Cash Flows
[400000-409999] Disclosures/Notes
[500000+] Other Reports & Statements
```

**Hierarchy Example** (Balance Sheet):
```
Assets [Abstract]
├── Non-Current Assets [Abstract]
│   ├── Property, Plant & Equipment
│   ├── Investment Property
│   ├── Intangible Assets (Goodwill)
│   ├── Other Intangible Assets
│   │   ├── Patents
│   │   ├── Licenses (e.g., Spectrum)
│   │   ├── Trademarks
│   │   └── Software
│   └── ...
└── Current Assets [Abstract]
    ├── Inventories
    ├── Trade Receivables
    ├── Cash & Cash Equivalents
    └── ...
```

### 3. Calculation Linkbase (Mathematical Relationships)

**Purpose**: Defines addition/subtraction rules for validation
**File**: `ind-as-cal-2017-03-31-{XXXXXX}.xml`

**Example Calculation Rule**:
```
Total Assets = Non-Current Assets + Current Assets
Total Assets = Fixed Assets + Investments + Current Assets

Non-Current Assets = PPE + Investment Property + Intangibles + ...
Current Assets = Inventory + Receivables + Cash + ...
```

**Key Principle**:
- All totals and subtotals must follow calculation linkbase relationships
- Ensures mathematical consistency across reports
- Non-adherence = validation errors

### 4. Definition Linkbase (Domain Relationships)

**Purpose**: Defines dimensional relationships, domain hierarchies, and concept relationships
**File**: `ind-as-def-2017-03-31-{XXXXXX}.xml` (varies by section, e.g., -400900.xml for Notes)

**Arc Roles**:
```
- all_arcrole: All relationships (parent-child)
- notAll_arcrole: Exclusive relationships
- is-a: Specialization (similar to inheritance)
- essence-alias: Equivalent concepts
- whole-part: Component relationships
```

**Example Definition (Intangible Assets Dimension)**:
```
Axis: ClassesOfOtherIntangibleAssetsAxis
├── Parent: CompanyOtherIntangibleAssetsMember
├── Children:
│   ├── Goodwill
│   ├── LicensesAndFranchise
│   │   ├── LicensesMember (e.g., Spectrum, Airwave Rights)
│   │   └── FranchisesAndLicensesMember
│   ├── PatentsMember
│   ├── BrandsAndTradeMarksMember
│   └── SoftwareAndSystemsMember
```

### 5. Reference Linkbase (Standards Mapping)

**Purpose**: Links elements to Indian Accounting Standards paragraphs
**File**: `ind-as-ref-2017-03-31.xml`

**Content**:
```xml
<link:referenceLink>
  <link:loc xlink:href="schema#ind-as_PropertyPlantAndEquipment" xlink:label="ref_ppe"/>
  <link:reference xlink:label="ref_ppe">
    Ind AS 16, Paragraph 6
  </link:reference>
</link:referenceLink>
```

**Cross-References**:
- Ind AS 1: Presentation of Financial Statements
- Ind AS 2: Inventories
- Ind AS 7: Statement of Cash Flows
- Ind AS 12: Income Taxes
- Ind AS 16: Property, Plant & Equipment
- Ind AS 18/115: Revenue Recognition
- Ind AS 37: Provisions
- Ind AS 38: Intangible Assets
- Ind AS 40: Investment Property
- Ind AS 41: Agriculture

### 6. Formula Linkbase (Business Rules)

**Purpose**: Advanced validation and calculation rules
**File**: Not always present; used for complex business logic

**Capabilities**:
- Open/closing balance reconciliation
- Multi-dimensional validation
- Complex aggregation rules
- Conditional relationships

---

## Financial Statement Mappings

### A. Balance Sheet Elements (Ind AS 1)

#### Non-Current Assets

| Line Item | XBRL Tag | Ind AS Ref | Notes |
|---|---|---|---|
| Property, Plant & Equipment | `ind-as_PropertyPlantAndEquipment` | Ind AS 16 | Tangible, long-term |
| Investment Property | `ind-as_InvestmentProperty` | Ind AS 40 | Real estate for income |
| Intangible Assets (Goodwill) | `ind-as_GoodwillAssets` | Ind AS 38 | Business combination |
| Other Intangible Assets | `ind-as_OtherIntangibleAssets` | Ind AS 38 | Patents, licenses, trademarks |
| Financial Assets (non-current) | `ind-as_FinancialAssetsNoncurrent` | Ind AS 109 | Non-current investments |
| Investments - Equity Method | `ind-as_InvestmentInAssociate` | Ind AS 28 | Associates & JVs |
| Biological Assets | `ind-as_BiologicalAssets` | Ind AS 41 | Agricultural assets |
| Deferred Tax Assets | `ind-as_DeferredTaxAssets` | Ind AS 12 | Tax differences |

#### Current Assets

| Line Item | XBRL Tag | Ind AS Ref | Notes |
|---|---|---|---|
| Inventories | `ind-as_Inventories` | Ind AS 2 | Raw materials, WIP, finished goods |
| Trade Receivables | `ind-as_TradeReceivables` | Ind AS 109 | Customer invoices |
| Cash & Cash Equivalents | `ind-as_CashAndCashEquivalents` | Ind AS 7 | Liquid funds |
| Other Financial Assets (current) | `ind-as_OtherFinancialAssets` | Ind AS 109 | Other liquid investments |
| Other Current Assets | `ind-as_OtherCurrentAssets` | Ind AS 1 | Prepayments, advances |
| Assets Held for Sale | `ind-as_AssetsHeldForSale` | Ind AS 105 | Non-current assets (classified) |

#### Non-Current Liabilities

| Line Item | XBRL Tag | Ind AS Ref | Notes |
|---|---|---|---|
| Borrowings (Long-term) | `ind-as_BorrowingsNoncurrent` | Ind AS 109 | Term loans, bonds |
| Provisions (Long-term) | `ind-as_ProvisionsNoncurrent` | Ind AS 37 | Employee benefits, warranties |
| Other Financial Liabilities | `ind-as_OtherFinancialLiabilitiesNoncurrent` | Ind AS 109 | Lease liabilities, derivatives |
| Deferred Tax Liabilities | `ind-as_DeferredTaxLiabilities` | Ind AS 12 | Tax differences |
| Other Non-Current Liabilities | `ind-as_OtherNoncurrentLiabilities` | Ind AS 1 | Deferred income, contingencies |

#### Current Liabilities

| Line Item | XBRL Tag | Ind AS Ref | Notes |
|---|---|---|---|
| Borrowings (Short-term) | `ind-as_BorrowingsCurrent` | Ind AS 109 | Working capital loans |
| Trade Payables | `ind-as_TradePayables` | Ind AS 109 | Vendor invoices |
| Current Tax Payable | `ind-as_CurrentTaxLiabilities` | Ind AS 12 | Income tax provision |
| Provisions (Current) | `ind-as_ProvisionsCurrent` | Ind AS 37 | Short-term employee benefits |
| Other Financial Liabilities (current) | `ind-as_OtherFinancialLiabilitiesCurrent` | Ind AS 109 | Accrued expenses |
| Other Current Liabilities | `ind-as_OtherCurrentLiabilities` | Ind AS 1 | Unearned revenue |

#### Equity

| Line Item | XBRL Tag | Ind AS Ref | Notes |
|---|---|---|---|
| Share Capital | `ind-as_ShareCapital` | Ind AS 32 | Equity shares issued |
| Preference Share Capital | `ind-as_PreferenceShareCapital` | Ind AS 32 | Preference shares |
| Reserves & Surplus | `ind-as_ReservesAndSurplus` | Ind AS 1 | Retained earnings, reserves |
| Treasury Stock | `ind-as_TreasuryStock` | Ind AS 32 | Repurchased shares |
| Non-Controlling Interests | `ind-as_NonControllingInterests` | Ind AS 110 | Minority interests |
| Other Comprehensive Income | `ind-as_OtherComprehensiveIncome` | Ind AS 1 | Revaluation gains, hedging |

### B. Statement of Profit & Loss (Ind AS 1)

#### Revenue Section

| Line Item | XBRL Tag | Ind AS Ref | Notes |
|---|---|---|---|
| Revenue from Operations | `ind-as_RevenueFromOperations` | Ind AS 115/18 | Main business income |
| Other Income | `ind-as_OtherIncome` | Ind AS 1 | Interest, dividends, gains |
| Finance Costs | `ind-as_FinanceCosts` | Ind AS 109/123 | Interest, borrowing fees |
| Depreciation & Amortization | `ind-as_DepreciationAndAmortization` | Ind AS 16/38 | Systematic write-down |
| Employee Benefits | `ind-as_EmployeeBenefitExpense` | Ind AS 19 | Salaries, bonuses |
| Other Expenses | `ind-as_OtherExpense` | Ind AS 1 | Operating expenses |

#### Profit Section

| Line Item | XBRL Tag | Ind AS Ref | Notes |
|---|---|---|---|
| Profit Before Tax | `ind-as_ProfitBeforeTax` | Ind AS 1 | EBIT-like measure |
| Tax Expense | `ind-as_TaxExpense` | Ind AS 12 | Current & deferred |
| Profit for the Period | `ind-as_NetProfitLoss` | Ind AS 1 | Net income |
| Profit Before Minority Interest | `ind-as_NetProfitLossbeforeMinorityInterestShareJointVenture` | Ind AS 1 | Before NCI |

#### Other Comprehensive Income (OCI)

| Line Item | XBRL Tag | Ind AS Ref | Notes |
|---|---|---|---|
| Items not Reclassified | `ind-as_OtherComprehensiveIncomeNotReclassifiedSubsequentlyToProfitOrLoss` | Ind AS 1 | Actuarial gains, revaluations |
| Items Reclassified | `ind-as_OtherComprehensiveIncomeWillBeReclassifiedSubsequentlyToProfitOrLoss` | Ind AS 1 | Hedging gains, translation |
| Total OCI | `ind-as_OtherComprehensiveIncomeNetOfTax` | Ind AS 1 | After tax OCI |
| Total Comprehensive Income | `ind-as_ComprehensiveIncome` | Ind AS 1 | PnL + OCI |

### C. Statement of Cash Flows (Ind AS 7)

#### Operating Activities

| Line Item | XBRL Tag | Ind AS Ref | Notes |
|---|---|---|---|
| Profit for the Period | `ind-as_NetProfitLoss` | Ind AS 7 | Starting point (indirect method) |
| Depreciation & Amortization | `ind-as_DepreciationAndAmortization` | Ind AS 7 | Non-cash adjustment |
| Impairment Losses | `ind-as_ImpairmentLossRecognized` | Ind AS 36 | Non-cash adjustment |
| Working Capital Changes | `ind-as_IncreaseDecreaseInWorkingCapital` | Ind AS 7 | Inventory, receivables, payables |
| Inventories Change | `ind-as_IncreaseInInventories` / `ind-as_DecreaseInInventories` | Ind AS 7 | Working capital |
| Receivables Change | `ind-as_IncreaseInTradeAndOtherReceivables` / Decrease | Ind AS 7 | Working capital |
| Payables Change | `ind-as_IncreaseInTradeAndOtherPayables` / Decrease | Ind AS 7 | Working capital |
| Income Tax Paid | `ind-as_IncomeTaxPaidRefund` | Ind AS 7 | Cash outflow |
| Cash from Operations (Net) | `ind-as_CashGeneratedFromOperations` | Ind AS 7 | Total operating cash |

#### Investing Activities

| Line Item | XBRL Tag | Ind AS Ref | Notes |
|---|---|---|---|
| Capital Expenditure | `ind-as_CapitalExpendituresIncurredButNotYetPaid` | Ind AS 7 | PPE, intangibles purchase |
| Proceeds from Asset Sales | `ind-as_ProceedsFromSaleOfPropertyPlantAndEquipment` | Ind AS 7 | Asset disposals |
| Investment Purchase | `ind-as_PaymentsForAcquisitionOfInvestments` | Ind AS 7 | Securities, equity |
| Investment Proceeds | `ind-as_ProceedsFromSaleOfInvestments` | Ind AS 7 | Securities sold |
| Interest Received | `ind-as_InterestReceived` | Ind AS 7 | Investment income |
| Dividends Received | `ind-as_DividendsReceived` | Ind AS 7 | Investment returns |
| Cash from Investments (Net) | `ind-as_CashFlowsFromInvestingActivities` | Ind AS 7 | Total investing cash |

#### Financing Activities

| Line Item | XBRL Tag | Ind AS Ref | Notes |
|---|---|---|---|
| Proceeds from Borrowing | `ind-as_ProceedsFromBorrowings` | Ind AS 7 | Loan disbursements |
| Repayment of Borrowing | `ind-as_RepaymentOfBorrowings` | Ind AS 7 | Loan repayments |
| Share Capital Received | `ind-as_ProceedsFromIssueOfShareCapital` | Ind AS 7 | Equity issuance |
| Dividends Paid | `ind-as_DividendsPaid` | Ind AS 7 | Distribution to equity |
| Interest Paid | `ind-as_InterestPaid` | Ind AS 7 | Debt servicing |
| Lease Payments | `ind-as_LeaseLiabilityPayments` | Ind AS 16 | IFRS 16/Ind AS 116 |
| Cash from Financing (Net) | `ind-as_CashFlowsFromFinancingActivities` | Ind AS 7 | Total financing cash |

#### Summary

| Item | XBRL Tag | Notes |
|---|---|---|
| Net Increase/(Decrease) in Cash | `ind-as_IncreaseDecreaseInCashAndCashEquivalents` | Operating + Investing + Financing |
| Cash at Beginning | `ind-as_CashAndCashEquivalentsAtBeginningOfPeriod` | Opening balance |
| Cash at End | `ind-as_CashAndCashEquivalentsAtEndOfPeriod` | Closing balance (per balance sheet) |

---

## Dimensional Modeling

### Common Dimensional Structures

#### 1. Intangible Assets Dimension

**Primary Table**: `DisclosureOfIntangibleAssetsTable`

**Axes**:
```
ClassesOfIntangibleAssetsAxis:
├── Goodwill
├── OtherIntangibleAssets
│   ├── LicensesAndFranchise
│   │   ├── LicensesMember (Spectrum rights)
│   │   └── FranchisesMember
│   ├── PatentsMember
│   ├── BrandsAndTradeMarksMember
│   ├── SoftwareAndSystemsMember
│   └── CopyrightsMember

CarryingAmountAccumulatedAmortizationAndImpairmentAndGrossCarryingAmountAxis:
├── GrossCarryingAmount
├── AccumulatedAmortization
├── AccumulatedImpairment
└── CarryingAmount
```

**Fact Dimension**:
```
Elements for each Member:
├── IntangibleAssets (opening)
├── Additions
├── Disposals
├── Amortization
├── Impairment
└── IntangibleAssets (closing)
```

#### 2. Borrowings Classification Dimension

**Axis**:
```
ClassificationOfBorrowingsAxis:
├── TermLoans
│   ├── TermLoansFromBanks
│   ├── TermLoansFromOthers
├── WorkingCapitalLoans
├── Bonds
├── DebenturesTowardCapitalReserve
└── OtherBorrowings
```

#### 3. Geographic/Business Segment Dimension

**Axes**:
```
GeographicSegmentAxis:
├── DomesticSegment
├── InternationalSegment

ProductOrServiceSegmentAxis:
├── Product1Member
├── Product2Member
└── ...ProductNMember
```

#### 4. Typed Dimension Example: Director Details

**Table**: `DetailsOfDirectorsSigningFinancialStatements`

**Elements** (Typed Members):
```
Director1:
├── DirectorName (typed string)
├── DirectorId (typed string)
├── DIN (typed integer)
├── DesignationOfDirector (typed enumeration)
└── ...

Director2, Director3, ... (same structure)
```

---

## Tag Identification Methodology

### Step-by-Step Process

#### Step 1: Label Search
```
Input: Text from financial statement (e.g., "Property, Plant and Equipment")
Search: Label Linkbase (ind-as-label-2017-03-31.xml)
Output: Concept ID (e.g., ind-as_PropertyPlantAndEquipment)
```

#### Step 2: Concept Verification
```
Input: Concept ID
Action: Look up in appropriate Presentation Linkbase
Output: Confirm hierarchy, context, and ELR
Example: Verify it's under NoncurrentAssetsAbstract in Balance Sheet [110000]
```

#### Step 3: Definition Linkbase Check
```
Input: Concept ID
Action: Check Definition Linkbase for dimensional relationships
Output: Identify required dimensions and members
Example: OtherIntangibleAssets requires ClassesOfOtherIntangibleAssetsAxis
```

#### Step 4: Reference Linkbase Validation
```
Input: Concept ID
Action: Check Reference Linkbase for Ind AS mapping
Output: Confirm accounting standard
Example: ind-as_PropertyPlantAndEquipment → Ind AS 16
```

### Example: Spectrum Mapping (Implicit Mapping)

**Scenario**: Company reports "Spectrum" as a separate line item under intangible assets

**Process**:

1. **Domain Knowledge**: Spectrum is a frequency band right = License
2. **Label Search**: "Spectrum" not found in Label Linkbase
3. **Classification**: Maps to `ind-as_OtherIntangibleAssets` (parent concept)
4. **Dimensional Breakdown**: 
   - Table: `DisclosureOfDetailedInformationAboutOtherIntangibleAssetsTable`
   - Axis: `ClassesOfOtherIntangibleAssetsAxis`
   - Member: `ind-as_LicensesMember` (specifically for Spectrum)
5. **Mapping**: 
   - Balance Sheet: `ind-as_OtherIntangibleAssets`
   - Notes Detail: `ind-as_OtherIntangibleAssets` + dimension `{ind-as_LicensesMember}`

**Definition File Evidence**:
- File: `ind-as-def-2017-03-31-400900.xml` (Notes - Other Intangible Assets)
- Hierarchy shows `LicensesAndFranchiseMember` → `LicensesMember`

---

## XBRL Instance Document Specifications

### Technical Requirements

#### 1. Schema Reference
```xml
<link:schemaRef 
  xlink:href="http://www.mca.gov.in/XBRL/2017/07/16/Taxonomy/Ind/in-ci-ent-2017-03-31.xsd"
  xlink:type="simple"/>
```

#### 2. Context Elements

**Context Structure**:
```xml
<xbrli:context id="D2017">
  <xbrli:entity>
    <xbrli:identifier scheme="http://www.mca.gov.in/CIN">
      [Company CIN]
    </xbrli:identifier>
  </xbrli:entity>
  <xbrli:period>
    <xbrli:startDate>2016-04-01</xbrli:startDate>
    <xbrli:endDate>2017-03-31</xbrli:endDate>
  </xbrli:period>
</xbrli:context>
```

**Instant Context** (for stock items):
```xml
<xbrli:context id="I2017">
  <xbrli:entity>
    <xbrli:identifier scheme="http://www.mca.gov.in/CIN">
      [Company CIN]
    </xbrli:identifier>
  </xbrli:entity>
  <xbrli:period>
    <xbrli:instantDate>2017-03-31</xbrli:instantDate>
  </xbrli:period>
</xbrli:context>
```

**Dimensional Context** (with members):
```xml
<xbrli:context id="D2017_Licenses">
  <xbrli:entity>
    <xbrli:identifier scheme="http://www.mca.gov.in/CIN">
      [Company CIN]
    </xbrli:identifier>
    <xbrli:segment>
      <xbrli:explicitMember dimensionName="ind-as:ClassesOfOtherIntangibleAssetsAxis">
        ind-as:LicensesMember
      </xbrli:explicitMember>
    </xbrli:segment>
  </xbrli:entity>
  <xbrli:period>
    <xbrli:startDate>2016-04-01</xbrli:startDate>
    <xbrli:endDate>2017-03-31</xbrli:endDate>
  </xbrli:period>
</xbrli:context>
```

#### 3. Unit Definitions

**Monetary Units**:
```xml
<xbrli:unit id="INR">
  <xbrli:measure>iso4217:INR</xbrli:measure>
</xbrli:unit>
```

**Numeric Units**:
```xml
<xbrli:unit id="shares">
  <xbrli:measure>xbrli:shares</xbrli:measure>
</xbrli:unit>

<xbrli:unit id="pure">
  <xbrli:measure>xbrli:pure</xbrli:measure>
</xbrli:unit>
```

#### 4. Fact Declaration

**Monetary Fact**:
```xml
<ind-as:PropertyPlantAndEquipment 
  contextRef="I2017" 
  unitRef="INR" 
  decimals="0">
  5000000000
</ind-as:PropertyPlantAndEquipment>
```

**Numeric Fact**:
```xml
<ind-as:NumberOfEmployees 
  contextRef="I2017" 
  unitRef="shares" 
  decimals="0">
  1000
</ind-as:NumberOfEmployees>
```

**Text Fact**:
```xml
<ind-as:NameOfCompany 
  contextRef="D2017">
  XYZ Limited
</ind-as:NameOfCompany>
```

**Fact with Footnote**:
```xml
<ind-as:OtherIntangibleAssets 
  contextRef="D2017" 
  unitRef="INR" 
  decimals="0"
  id="f_oia_1">
  500000000
</ind-as:OtherIntangibleAssets>

<link:footnoteLink xlink:type="extended">
  <link:loc xlink:href="#f_oia_1" xlink:label="loc_oia"/>
  <link:footnote xlink:label="fn_oia" xlink:type="simple">
    Spectrum (License) value adjusted from original basis
  </link:footnote>
  <link:footnoteArc xlink:from="loc_oia" xlink:to="fn_oia"/>
</link:footnoteLink>
```

### Instance Document Structure

**File Naming**:
```
CompanyName_IndAS_Standalone_YYYY-MM-DD.xml (Standalone)
CompanyName_IndAS_Consolidated_YYYY-MM-DD.xml (Consolidated)
```

**Mandatory Periods**:
- Current Year (e.g., 2016-04-01 to 2017-03-31)
- Comparative Year (e.g., 2015-04-01 to 2016-03-31)
- Opening Balance Sheet (if first-time Ind AS adoption: 2015-04-01)

---

## Business Rules & Validation

### MCA Filing Manual Requirements

#### 1. Mapping Rules

| Rule | Description | Example |
|---|---|---|
| **Exact Matching** | Use exact taxonomy element if available | "Property, Plant and Equipment" → `ind-as_PropertyPlantAndEquipment` |
| **Next-Best-Fit** | Use parent/general category if exact not available | "Spectrum" → `ind-as_OtherIntangibleAssets` + Member |
| **Others Element** | Use generic "Others" element only as last resort | Not applicable if specific tag exists |
| **Footnote Adjustment** | Document any adjustments or approximations | Required for non-exact mappings |
| **No Extensions** | Cannot extend core taxonomy | All elements from published taxonomy only |

#### 2. Calculation Relationships

**Must Satisfy**:
```
Total Assets = Current Assets + Non-Current Assets
Current Assets = Cash + Receivables + Inventory + ...
Non-Current Assets = PPE + Intangibles + Long-term Investments + ...

Total Liabilities & Equity = Current Liabilities + Non-Current Liabilities + Equity
Equity = Share Capital + Reserves + Retained Earnings

Profit = Revenue - Expenses
Total Income = Revenue + Other Income
```

**Validation**: Calculation linkbase enforces these relationships

#### 3. Dimensional Validation

**Rules**:
- Dimensional contexts must be valid against hypercubes
- Default members should not appear in instance
- All explicit members must have valid namespaces
- Typed member values must match expected data type

**Example Error**:
```
DisclosureOfIntangibleAssetsTable requires:
- ClassesOfIntangibleAssetsAxis: At least one child member
- SubClassesOfOtherIntangibleAssetsAxis: Valid for "OtherIntangibleAssets" only
- CarryingAmountAxis: All three members (Gross, Accumulated, Net)
```

#### 4. Mandatory Elements

**By Extended Link Role (ELR)**:

| ELR | Mandatory Elements | Condition |
|---|---|---|
| [100000] Balance Sheet - Main | All line items per Ind AS 1 | Company-specific |
| [200000] P&L - Main | Revenue, Expenses, Profit | Always required |
| [300000] Cash Flow | Operating, Investing, Financing activities | Always required |
| [400000-409999] Note Tables | Varies by element presence | If element present in P&L/BS |

**Example**:
```
If "NetProfitLoss" is reported, then EITHER:
- "NetProfitLossbeforeMinorityInterestShareJointVenture" 
  AND "MinorityInterestProportionOfProfitOrLoss"
OR (for standalone) just NetProfitLoss
```

#### 5. Data Type Rules

| Data Type | Valid Values | Example |
|---|---|---|
| Monetary | Integer with INR unit | 5000000000 |
| Percentage | 0-1 range | 0.60 (for 60%) |
| Boolean | true / false (not yes/no) | true |
| Date | YYYY-MM-DD format | 2017-03-31 |
| String | Text with allowed HTML | "XYZ Limited" |
| Integer | Whole numbers | 1000 |

#### 6. Context Validation

**Rules**:
```
1. No duplicate contexts (same scenario + period)
2. Each context used at least once
3. Non-overlapping periods for same element
4. No segment element at entity level
5. All dimensional references use valid namespaces
```

#### 7. Common Validation Errors & Resolutions

| Error | Cause | Resolution |
|---|---|---|
| `cvc-datatype-valid.1.2.1: '01-04-2011' not valid` | Wrong date format | Use YYYY-MM-DD (2011-04-01) |
| `'yes' is not valid for 'boolean'` | Boolean case issue | Use "true" or "false" |
| `value 60 not equal to 1` | Percentage format error | Use 0.60 (not 60 or 60%) |
| `No unit specified for INR currency` | Missing unit ref | Add unitRef="INR" to monetary facts |
| `Element X required for Member Y` | Dimensional requirement | Add all required axes for member |
| `Closing balance ≠ Opening + Changes` | Formula violation | Ensure reconciliation |
| `All axes mandatory for table presence` | Multi-axis requirement | Add all child members for all axes |

---

## Common Element Mappings

### Quick Reference Table

| Financial Statement Item | XBRL Tag | Period Type | Data Type | Notes |
|---|---|---|---|---|
| **Balance Sheet - Assets** | | | | |
| Cash & Equivalents | `ind-as_CashAndCashEquivalents` | Instant | Monetary | |
| Trade Receivables | `ind-as_TradeReceivables` | Instant | Monetary | Net of allowances |
| Inventories | `ind-as_Inventories` | Instant | Monetary | Finished goods value |
| Other Current Assets | `ind-as_OtherCurrentAssets` | Instant | Monetary | Prepayments, advances |
| PPE | `ind-as_PropertyPlantAndEquipment` | Instant | Monetary | Gross or net per policy |
| Intangible Assets | `ind-as_IntangibleAssets` | Instant | Monetary | Patents, software, etc. |
| Goodwill | `ind-as_GoodwillAssets` | Instant | Monetary | Business combinations |
| **Balance Sheet - Liabilities** | | | | |
| Trade Payables | `ind-as_TradePayables` | Instant | Monetary | Vendor payables |
| Short-term Borrowings | `ind-as_BorrowingsCurrent` | Instant | Monetary | Working capital loans |
| Current Tax Liability | `ind-as_CurrentTaxLiabilities` | Instant | Monetary | Provision for tax |
| Other Current Liabilities | `ind-as_OtherCurrentLiabilities` | Instant | Monetary | Accruals, deferred income |
| Long-term Borrowings | `ind-as_BorrowingsNoncurrent` | Instant | Monetary | Term loans, bonds |
| Deferred Tax Liability | `ind-as_DeferredTaxLiabilities` | Instant | Monetary | Tax temporary differences |
| **Balance Sheet - Equity** | | | | |
| Share Capital | `ind-as_ShareCapital` | Instant | Monetary | Equity share capital |
| Reserves & Surplus | `ind-as_ReservesAndSurplus` | Instant | Monetary | Retained earnings, reserves |
| **P&L - Income** | | | | |
| Revenue from Operations | `ind-as_RevenueFromOperations` | Duration | Monetary | Main business revenue |
| Other Income | `ind-as_OtherIncome` | Duration | Monetary | Interest, dividend, gains |
| **P&L - Expenses** | | | | |
| Cost of Materials | `ind-as_CostOfMaterialsConsumed` | Duration | Monetary | Raw materials used |
| Employee Costs | `ind-as_EmployeeBenefitExpense` | Duration | Monetary | Salaries, bonuses |
| Depreciation | `ind-as_DepreciationAndAmortization` | Duration | Monetary | Asset write-down |
| Finance Costs | `ind-as_FinanceCosts` | Duration | Monetary | Interest expense |
| Other Expenses | `ind-as_OtherExpense` | Duration | Monetary | Operating expenses |
| **P&L - Bottom Line** | | | | |
| Profit Before Tax | `ind-as_ProfitBeforeTax` | Duration | Monetary | EBIT-like measure |
| Tax Expense | `ind-as_TaxExpense` | Duration | Monetary | Current + deferred tax |
| Net Profit for Period | `ind-as_NetProfitLoss` | Duration | Monetary | Earnings/Net income |
| **Cash Flow - Operating** | | | | |
| Cash from Operations | `ind-as_CashGeneratedFromOperations` | Duration | Monetary | Net operating cash |
| Tax Paid | `ind-as_IncomeTaxPaidRefund` | Duration | Monetary | Cash tax payment |
| **Cash Flow - Investing** | | | | |
| Capital Expenditure | `ind-as_CapitalExpendituresIncurredButNotYetPaid` | Duration | Monetary | Asset purchases |
| Proceeds from Asset Sales | `ind-as_ProceedsFromSaleOfPropertyPlantAndEquipment` | Duration | Monetary | Asset disposal proceeds |
| **Cash Flow - Financing** | | | | |
| Borrowing Proceeds | `ind-as_ProceedsFromBorrowings` | Duration | Monetary | New debt |
| Borrowing Repayment | `ind-as_RepaymentOfBorrowings` | Duration | Monetary | Debt repaid |
| Dividends Paid | `ind-as_DividendsPaid` | Duration | Monetary | Cash distributed |
| **Disclosures - General** | | | | |
| Company Name | `ind-as_NameOfCompany` | Duration | String | Legal entity name |
| CIN | `ind-as_IdentificationNumberOfCompany` | Duration | String | Corporate ID |
| Reporting Currency | `ind-as_PresentationCurrency` | Duration | String | INR (mandatory) |
| **Disclosures - Notes** | | | | |
| Goodwill Detail | `DisclosureOfGoodwillTable` | Table | Multiple | By class, gross/accum. |
| Intangible Detail | `DisclosureOfIntangibleAssetsTable` | Table | Multiple | By type, opening/closing |
| PPE Reconciliation | `DisclosureOfPropertyPlantAndEquipmentTable` | Table | Multiple | Movement schedule |
| Borrowings Detail | `DisclosureOfBorrowingsTable` | Table | Multiple | By type, rate, maturity |

---

## Summary & Best Practices

### Key Takeaways

1. **Taxonomy is Hierarchical**: Presentation linkbase shows financial statement structure
2. **Dimensions Enable Drill-Down**: Use members for detailed disclosures (notes)
3. **Validation is Mandatory**: Calculation and definition linkbases enforce rules
4. **No Guessing**: Always search label linkbase first; use domain knowledge for implicit mappings
5. **Documentation Required**: Footnotes explain non-standard or adjusted mappings

### Best Practices for XBRL Tagging

#### DO:
- ✓ Search label linkbase for exact text matches
- ✓ Verify in presentation linkbase for hierarchy
- ✓ Check definition linkbase for dimensional requirements
- ✓ Use calculation linkbase to validate totals
- ✓ Document adjustments via footnotes
- ✓ Use proper context structures (instant vs. duration)
- ✓ Apply dimensions for detailed disclosures
- ✓ Follow MCA business rules strictly

#### DON'T:
- ✗ Create custom extensions or new elements
- ✗ Use "Others" elements when specific tags exist
- ✗ Skip validation against calculation relationships
- ✗ Mix currencies without documenting
- ✗ Ignore dimensional requirements in tables
- ✗ Report inconsistent periods (gaps or overlaps)
- ✗ Use wrong data types (e.g., "yes" for boolean)
- ✗ Forget footnotes for approximations

### Verification Checklist

Before filing instance documents:

- [ ] All mandatory financial statement elements entered
- [ ] Current year AND prior year data completed
- [ ] Opening balance sheet completed (if first-time Ind AS)
- [ ] All totals match calculation linkbase relationships
- [ ] Dimensional contexts valid and all axes populated
- [ ] Context IDs are unique and used at least once
- [ ] Monetary units consistently applied (INR)
- [ ] Data types correct (dates, percentages, booleans)
- [ ] Footnotes documented for non-standard mappings
- [ ] PDF export successful and content matches filed FS
- [ ] Pre-scrutiny validation passed in MCA tool
- [ ] No schema validation errors (cvc-*)

---

## References & Resources

### Regulatory Documents
- MCA XBRL Filing Manual (For IND AS Validation Tool)
- MCA XBRL Portal: www.mca.gov.in/XBRL
- Business Rules: Available in validation tool

### Accounting Standards
- Ind AS 1: Presentation of Financial Statements
- Ind AS 2: Inventories
- Ind AS 7: Statement of Cash Flows
- Ind AS 12: Income Taxes
- Ind AS 16: Property, Plant & Equipment
- Ind AS 18/115: Revenue Recognition
- Ind AS 28: Investments in Associates & JVs
- Ind AS 32: Financial Instruments – Presentation
- Ind AS 37: Provisions
- Ind AS 38: Intangible Assets
- Ind AS 40: Investment Property
- Ind AS 109: Financial Instruments
- Ind AS 110: Consolidated Financial Statements

### XBRL Technical Standards
- XBRL 2.1 Specification
- XBRL Dimensions 1.0
- XBRL Table Linkbase
- XBRL Formula

### Tools & Support
- MCA XBRL Validation Tool (free download from MCA website)
- Professional XBRL Software (various vendors)
- XBRL International Documentation
- Indian XBRL Community Resources

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**Status**: Comprehensive Guide for IND AS XBRL Implementation  
**Applicability**: IND AS 2017 Taxonomy (Released March 31, 2017)


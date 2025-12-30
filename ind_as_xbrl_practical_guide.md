# IND AS XBRL: Practical Implementation Guide with Examples

## Table of Contents
1. [Complete Mapping Examples](#complete-mapping-examples)
2. [Real-World Scenarios](#real-world-scenarios)
3. [Common Tagging Challenges](#common-tagging-challenges)
4. [Dimensional Modeling Examples](#dimensional-modeling-examples)
5. [Instance Document Code Examples](#instance-document-code-examples)
6. [Validation Error Troubleshooting](#validation-error-troubleshooting)
7. [Filing Checklist](#filing-checklist)

---

## Complete Mapping Examples

### Example 1: Simple Balance Sheet Item (Property, Plant & Equipment)

#### Source Data
```
XYZ Limited
Balance Sheet as at 31 March 2017 (in INR)

Non-Current Assets
  Property, Plant and Equipment       5,000,000,000
  Less: Accumulated Depreciation     (1,500,000,000)
  Net PPE                             3,500,000,000
```

#### Mapping Process

**Step 1: Label Search**
- Search label linkbase for "Property, Plant and Equipment"
- Found: Exact match = `ind-as_PropertyPlantAndEquipment`

**Step 2: Hierarchy Verification**
- Presentation linkbase search:
  - ELR [110000] Balance Sheet - Main
  - Parent: `NoncurrentAssetsAbstract`
  - Position: Line item under non-current assets ✓

**Step 3: Definition Check**
- Definition linkbase search:
  - No dimensional requirements for this element
  - Stands alone without member requirements

**Step 4: Reference Check**
- Reference linkbase:
  - Ind AS 16: Property, Plant and Equipment ✓

#### XBRL Instance Coding

**Context Definition**:
```xml
<xbrli:context id="I2017">
  <xbrli:entity>
    <xbrli:identifier scheme="http://www.mca.gov.in/CIN">
      U24251MH2010PLC203456
    </xbrli:identifier>
  </xbrli:entity>
  <xbrli:period>
    <xbrli:instantDate>2017-03-31</xbrli:instantDate>
  </xbrli:period>
</xbrli:context>

<xbrli:context id="I2016">
  <xbrli:entity>
    <xbrli:identifier scheme="http://www.mca.gov.in/CIN">
      U24251MH2010PLC203456
    </xbrli:identifier>
  </xbrli:entity>
  <xbrli:period>
    <xbrli:instantDate>2016-03-31</xbrli:instantDate>
  </xbrli:period>
</xbrli:context>
```

**Unit Definition**:
```xml
<xbrli:unit id="INR">
  <xbrli:measure>iso4217:INR</xbrli:measure>
</xbrli:unit>
```

**Facts**:
```xml
<!-- Current Year -->
<ind-as:PropertyPlantAndEquipment 
  contextRef="I2017" 
  unitRef="INR" 
  decimals="0">
  3500000000
</ind-as:PropertyPlantAndEquipment>

<!-- Previous Year -->
<ind-as:PropertyPlantAndEquipment 
  contextRef="I2016" 
  unitRef="INR" 
  decimals="0">
  3200000000
</ind-as:PropertyPlantAndEquipment>
```

---

### Example 2: Complex Item with Dimensions (Intangible Assets)

#### Source Data
```
XYZ Limited - Notes to Financial Statements
Intangible Assets Disclosure (in INR):

                        Opening    Additions  Disposals  Amortization  Closing
                        Balance                                         Balance
Goodwill               1,000 Cr    -          -          -             1,000 Cr
Patents                  500 Cr    200 Cr     -          (50 Cr)       650 Cr
Spectrum License        5,000 Cr   1,000 Cr   -          (500 Cr)     5,500 Cr
Trademarks               300 Cr    -          -          (30 Cr)       270 Cr
Software                 200 Cr    100 Cr     -          (50 Cr)       250 Cr
```

#### Mapping Strategy

**Primary Element**: `ind-as_IntangibleAssets` (line item level)

**Dimensional Breakdown**:
```
Table: DisclosureOfIntangibleAssetsTable
Axis 1: ClassesOfIntangibleAssetsAxis
  ├── GoodwillMember
  └── OtherIntangibleAssetsMember
        ├── PatentsMember
        ├── LicensesMember (Spectrum)
        ├── BrandsAndTradeMarksMember
        └── SoftwareAndSystemsMember

Axis 2: CarryingAmountAccumulatedAmortizationAndImpairmentAndGrossCarryingAmountAxis
  ├── GrossCarryingAmountMember
  ├── AccumulatedAmortizationAndImpairmentMember
  └── CarryingAmountMember
```

#### XBRL Instance Coding

**Context Definitions**:
```xml
<!-- For Goodwill -->
<xbrli:context id="D2017_Goodwill">
  <xbrli:entity>
    <xbrli:identifier scheme="http://www.mca.gov.in/CIN">
      U24251MH2010PLC203456
    </xbrli:identifier>
    <xbrli:segment>
      <xbrli:explicitMember 
        dimensionName="ind-as:ClassesOfIntangibleAssetsAxis">
        ind-as:GoodwillMember
      </xbrli:explicitMember>
      <xbrli:explicitMember 
        dimensionName="ind-as:CarryingAmountAccumulatedAmortizationAndImpairmentAndGrossCarryingAmountAxis">
        ind-as:CarryingAmountMember
      </xbrli:explicitMember>
    </xbrli:segment>
  </xbrli:entity>
  <xbrli:period>
    <xbrli:instantDate>2017-03-31</xbrli:instantDate>
  </xbrli:period>
</xbrli:context>

<!-- For Spectrum (LicensesMember) -->
<xbrli:context id="D2017_Spectrum_Carrying">
  <xbrli:entity>
    <xbrli:identifier scheme="http://www.mca.gov.in/CIN">
      U24251MH2010PLC203456
    </xbrli:identifier>
    <xbrli:segment>
      <xbrli:explicitMember 
        dimensionName="ind-as:ClassesOfOtherIntangibleAssetsAxis">
        ind-as:LicensesMember
      </xbrli:explicitMember>
      <xbrli:explicitMember 
        dimensionName="ind-as:SubClassesOfOtherIntangibleAssetsAxis">
        ind-as:LicensesAndFranchiseMember
      </xbrli:explicitMember>
      <xbrli:explicitMember 
        dimensionName="ind-as:CarryingAmountAccumulatedAmortizationAndImpairmentAndGrossCarryingAmountAxis">
        ind-as:CarryingAmountMember
      </xbrli:explicitMember>
    </xbrli:segment>
  </xbrli:entity>
  <xbrli:period>
    <xbrli:instantDate>2017-03-31</xbrli:instantDate>
  </xbrli:period>
</xbrli:context>
```

**Facts**:
```xml
<!-- Goodwill - Carrying Amount -->
<ind-as:IntangibleAssets 
  contextRef="D2017_Goodwill" 
  unitRef="INR" 
  decimals="0">
  100000000
</ind-as:IntangibleAssets>

<!-- Spectrum License - Carrying Amount -->
<ind-as:ChangesInIntangibleAssets 
  contextRef="D2017_Spectrum_Carrying" 
  unitRef="INR" 
  decimals="0">
  550000000
</ind-as:ChangesInIntangibleAssets>

<!-- Spectrum License - Gross Amount -->
<ind-as:ChangesInIntangibleAssets 
  contextRef="D2017_Spectrum_Gross" 
  unitRef="INR" 
  decimals="0">
  600000000
</ind-as:ChangesInIntangibleAssets>

<!-- Spectrum License - Opening Balance -->
<ind-as:IntangibleAssets 
  contextRef="D2017_Spectrum_Opening" 
  unitRef="INR" 
  decimals="0">
  500000000
</ind-as:IntangibleAssets>
```

---

### Example 3: Profit & Loss Statement

#### Source Data
```
XYZ Limited
Statement of Profit and Loss for year ended 31 March 2017 (in INR)

Revenue from operations                   50,000,000,000
Other income                               2,000,000,000
Total Income                              52,000,000,000

Cost of materials consumed                20,000,000,000
Employee benefit expenses                  8,000,000,000
Depreciation & amortization                1,500,000,000
Finance costs                              3,000,000,000
Other expenses                             5,000,000,000
Total Expenses                            37,500,000,000

Profit Before Tax                         14,500,000,000
Tax expense (current)                      3,000,000,000
Tax expense (deferred)                       500,000,000
Total Tax                                  3,500,000,000

Profit for the period                     11,000,000,000
```

#### Mapping Process

| Line Item | XBRL Tag | ELR | Duration Context |
|---|---|---|---|
| Revenue | `ind-as_RevenueFromOperations` | [200000] | D2017 |
| Other Income | `ind-as_OtherIncome` | [200000] | D2017 |
| Cost of Materials | `ind-as_CostOfMaterialsConsumed` | [200000] | D2017 |
| Employee Expenses | `ind-as_EmployeeBenefitExpense` | [200000] | D2017 |
| Depreciation | `ind-as_DepreciationAndAmortization` | [200000] | D2017 |
| Finance Costs | `ind-as_FinanceCosts` | [200000] | D2017 |
| Other Expenses | `ind-as_OtherExpense` | [200000] | D2017 |
| Profit Before Tax | `ind-as_ProfitBeforeTax` | [200000] | D2017 |
| Tax Expense | `ind-as_TaxExpense` | [200000] | D2017 |
| Net Profit | `ind-as_NetProfitLoss` | [200000] | D2017 |

#### Duration Context Definition
```xml
<xbrli:context id="D2017">
  <xbrli:entity>
    <xbrli:identifier scheme="http://www.mca.gov.in/CIN">
      U24251MH2010PLC203456
    </xbrli:identifier>
  </xbrli:entity>
  <xbrli:period>
    <xbrli:startDate>2016-04-01</xbrli:startDate>
    <xbrli:endDate>2017-03-31</xbrli:endDate>
  </xbrli:period>
</xbrli:context>
```

#### XBRL Facts
```xml
<ind-as:RevenueFromOperations 
  contextRef="D2017" 
  unitRef="INR" 
  decimals="0">
  50000000000
</ind-as:RevenueFromOperations>

<ind-as:OtherIncome 
  contextRef="D2017" 
  unitRef="INR" 
  decimals="0">
  2000000000
</ind-as:OtherIncome>

<ind-as:CostOfMaterialsConsumed 
  contextRef="D2017" 
  unitRef="INR" 
  decimals="0">
  20000000000
</ind-as:CostOfMaterialsConsumed>

<ind-as:EmployeeBenefitExpense 
  contextRef="D2017" 
  unitRef="INR" 
  decimals="0">
  8000000000
</ind-as:EmployeeBenefitExpense>

<ind-as:DepreciationAndAmortization 
  contextRef="D2017" 
  unitRef="INR" 
  decimals="0">
  1500000000
</ind-as:DepreciationAndAmortization>

<ind-as:FinanceCosts 
  contextRef="D2017" 
  unitRef="INR" 
  decimals="0">
  3000000000
</ind-as:FinanceCosts>

<ind-as:OtherExpense 
  contextRef="D2017" 
  unitRef="INR" 
  decimals="0">
  5000000000
</ind-as:OtherExpense>

<ind-as:ProfitBeforeTax 
  contextRef="D2017" 
  unitRef="INR" 
  decimals="0">
  14500000000
</ind-as:ProfitBeforeTax>

<ind-as:TaxExpense 
  contextRef="D2017" 
  unitRef="INR" 
  decimals="0">
  3500000000
</ind-as:TaxExpense>

<ind-as:NetProfitLoss 
  contextRef="D2017" 
  unitRef="INR" 
  decimals="0">
  11000000000
</ind-as:NetProfitLoss>
```

#### Calculation Validation
```
Total Income = Revenue + Other Income
             = 50,000 Cr + 2,000 Cr = 52,000 Cr ✓

Total Expenses = Cost + Employee + Depreciation + Finance + Other
               = 20,000 + 8,000 + 1,500 + 3,000 + 5,000 = 37,500 Cr ✓

Profit Before Tax = Total Income - Total Expenses
                  = 52,000 - 37,500 = 14,500 Cr ✓

Net Profit = Profit Before Tax - Tax
           = 14,500 - 3,500 = 11,000 Cr ✓
```

---

## Real-World Scenarios

### Scenario 1: Spectrum License Mapping (Implicit Dimension)

**Business Context**:
- Telecommunications company holds spectrum licenses (airwave rights)
- Acquired for INR 5 billion, amortized over 20 years
- Not separately line-itemized in balance sheet; shown under "Other Intangible Assets"

**Mapping Challenge**:
- Exact tag "Spectrum" doesn't exist in taxonomy
- Must use domain knowledge + dimensional breakdown

**Solution**:

1. **Balance Sheet Entry**:
   ```
   XBRL Tag: ind-as_OtherIntangibleAssets
   Value: INR 5,000,000,000 (carrying amount)
   Context: Instant (as at 31 March 2017)
   ```

2. **Notes Disclosure**:
   ```
   Table: DisclosureOfDetailedInformationAboutOtherIntangibleAssetsTable
   Axis: ClassesOfOtherIntangibleAssetsAxis + SubClassesOfOtherIntangibleAssetsAxis
   Member: ind-as:LicensesMember
   
   Facts for each member:
   - Opening Gross Spectrum Value: 5,000 Cr
   - Additions: 1,000 Cr
   - Amortization: (500 Cr)
   - Closing Gross Spectrum Value: 5,500 Cr
   - Accumulated Amortization: (500 Cr)
   - Carrying Amount: 5,000 Cr
   ```

3. **Footnote** (important!):
   ```
   "Spectrum represents wireless spectrum licenses acquired from 
   Department of Telecom. Value includes acquisition cost of 
   INR 5 billion and subsequent renewal for INR 1 billion. 
   Amortized over license validity period."
   ```

---

### Scenario 2: First-Time Ind AS Adoption (Opening Balance Sheet)

**Business Context**:
- Company transitioning from Indian GAAP to Ind AS
- Compliance requirement from FY 2016-17
- Previous GAAP values differ from Ind AS opening balance

**Example: Deferred Tax Asset**
```
Indian GAAP (2016):    INR 500 million
Ind AS Adjustments:    INR (200) million (tax rate change)
Ind AS Opening (2015): INR 300 million
```

**XBRL Mapping**:

Periods Required:
```
1. Opening Balance Sheet:   2015-04-01 (Instant)
2. Previous Balance Sheet:  2016-03-31 (Instant) 
3. Current Balance Sheet:   2017-03-31 (Instant)
```

Contexts:
```xml
<!-- Opening Balance Sheet (Ind AS transitional) -->
<xbrli:context id="I2015">
  <xbrli:entity>
    <xbrli:identifier scheme="http://www.mca.gov.in/CIN">
      U24251MH2010PLC203456
    </xbrli:identifier>
  </xbrli:entity>
  <xbrli:period>
    <xbrli:instantDate>2015-04-01</xbrli:instantDate>
  </xbrli:period>
</xbrli:context>

<!-- Previous Year (comparative) -->
<xbrli:context id="I2016">...</xbrli:context>

<!-- Current Year -->
<xbrli:context id="I2017">...</xbrli:context>
```

Facts:
```xml
<!-- Opening Deferred Tax Asset -->
<ind-as:DeferredTaxAssets 
  contextRef="I2015" 
  unitRef="INR" 
  decimals="0">
  30000000
</ind-as:DeferredTaxAssets>

<!-- Previous Year Comparative -->
<ind-as:DeferredTaxAssets 
  contextRef="I2016" 
  unitRef="INR" 
  decimals="0">
  35000000
</ind-as:DeferredTaxAssets>

<!-- Current Year -->
<ind-as:DeferredTaxAssets 
  contextRef="I2017" 
  unitRef="INR" 
  decimals="0">
  40000000
</ind-as:DeferredTaxAssets>
```

---

### Scenario 3: Multi-Currency Subsidiary Consolidation

**Business Context**:
- Parent company (India, INR) + subsidiary (USA, USD)
- Consolidated financial statements in INR
- Subsidiary operates independently with USD borrowings

**XBRL Challenge**:
- MCA specification allows subsidiary monetary amounts in original currency
- Presentation and functional currency differences

**Solution**:

Definition:
```xml
<!-- USD Unit for Subsidiary -->
<xbrli:unit id="USD">
  <xbrli:measure>iso4217:USD</xbrli:measure>
</xbrli:unit>

<!-- INR Unit for Consolidated -->
<xbrli:unit id="INR">
  <xbrli:measure>iso4217:INR</xbrli:measure>
</xbrli:unit>
```

Context with Typed Dimension:
```xml
<xbrli:context id="D2017_SubsidiaryUSD">
  <xbrli:entity>
    <xbrli:identifier scheme="http://www.mca.gov.in/CIN">
      U24251MH2010PLC203456 <!-- Parent CIN -->
    </xbrli:identifier>
    <xbrli:segment>
      <xbrli:typedMember 
        dimensionName="ind-as:IdentityOfSubsidiaryOrAssociateOrJointVentureAxis">
        CompanyUSA Subsidiary Inc
      </xbrli:typedMember>
      <xbrli:typedMember 
        dimensionName="ind-as:CurrencyOfSubsidiaryAxis">
        USD
      </xbrli:typedMember>
    </xbrli:segment>
  </xbrli:entity>
  <xbrli:period>
    <xbrli:instantDate>2017-03-31</xbrli:instantDate>
  </xbrli:period>
</xbrli:context>
```

Facts:
```xml
<!-- Consolidated Parent (INR) -->
<ind-as:BorrowingsCurrent 
  contextRef="I2017" 
  unitRef="INR" 
  decimals="0">
  10000000000
</ind-as:BorrowingsCurrent>

<!-- Subsidiary Detail (USD) -->
<ind-as:SubsidiaryBorrowingsCurrent 
  contextRef="D2017_SubsidiaryUSD" 
  unitRef="USD" 
  decimals="0">
  150000000
</ind-as:SubsidiaryBorrowingsCurrent>
```

---

## Common Tagging Challenges

### Challenge 1: "Other Assets" Categorization

**Problem**: Company reports "Other Assets" not matching any specific tag

**Resolution Process**:

1. **Analyze Nature**: What type of asset is it?
   - Long-term? → Non-current
   - Short-term? → Current
   - Financial? → Financial Assets
   - Operational? → Operational Assets

2. **Find Parent Concept**:
   - If long-term financial: `ind-as_OtherFinancialAssetsNoncurrent`
   - If short-term other: `ind-as_OtherCurrentAssets`
   - If special type: Use specific tag (goodwill, intangibles, etc.)

3. **Add Footnote**:
   ```
   "Other Assets includes [itemized breakdown]:
   - Advance to vendors: INR 500 Mn
   - Prepaid insurance: INR 300 Mn
   - Security deposits: INR 200 Mn"
   ```

### Challenge 2: Lease Obligations (Ind AS 116)

**Problem**: Company has right-of-use (ROU) assets under Ind AS 116

**Mapping**:

Note: Ind AS 116 (effective FY 2019-20) may not be fully covered in 2017 taxonomy initially

**Workaround**:
```
Balance Sheet Asset:
  Tag: ind-as_OtherNoncurrentAssets (temporary, pending taxonomy update)
  Note: Detailed lease schedule in disclosure note

Balance Sheet Liability:
  Tag: ind-as_OtherFinancialLiabilitiesNoncurrent
  Note: Lease obligation detail per Ind AS 116

Cash Flow:
  Tag: ind-as_LeaseLiabilityPayments
  Note: Operating vs financing classification per Ind AS 7
```

### Challenge 3: Business Combination & Goodwill Accounting

**Problem**: Acquisitions during year; goodwill revaluation

**Solution**:

Table: `DisclosureOfGoodwillTable`

Members:
```
ClassesOfGoodwillAxis:
├── GoodwillFromAcquisitionOfSubsidiary1Member
├── GoodwillFromAcquisitionOfSubsidiary2Member
└── Other...

CarryingAmountAccumulatedImpairmentAndGrossCarryingAmountAxis:
├── GrossCarryingAmountMember
├── AccumulatedImpairmentMember
└── CarryingAmountMember
```

Facts:
```xml
<!-- Goodwill Opening -->
<ind-as:Goodwill contextRef="..." unitRef="INR">
  1000000000
</ind-as:Goodwill>

<!-- Business Combination Addition -->
<ind-as:PurchaseOfBusinessCombination contextRef="..." unitRef="INR">
  500000000
</ind-as:PurchaseOfBusinessCombination>

<!-- Impairment -->
<ind-as:GoodwillAndIntangibleAssetsImpairment contextRef="..." unitRef="INR">
  (100000000)
</ind-as:GoodwillAndIntangibleAssetsImpairment>

<!-- Closing -->
<ind-as:Goodwill contextRef="..." unitRef="INR">
  1400000000
</ind-as:Goodwill>
```

---

## Dimensional Modeling Examples

### Example 1: Borrowings by Type

**Table**: `DisclosureOfBorrowingsTable`

**Primary Axis**:
```
ClassificationOfBorrowingsAxis:
├── SecuredBorrowingsMember
│   ├── TermLoansFromBanksMember
│   ├── VehicleLoansFromBanksMember
│   └── WorkingCapitalLoansFromBanksMember
└── UnsecuredBorrowingsMember
    ├── TermLoansFromOthersMember
    ├── DevelopmentLoansMember
    └── BondsMember
```

**Secondary Axis** (Current vs Non-Current):
```
TermOrMaturityOfBorrowingsAxis:
├── CurrentMember
└── NoncurrentMember
```

**Example Facts**:
```xml
<!-- Secured Term Loans - Current -->
<ind-as:InterestRateOfBorrowings 
  contextRef="D2017_SecuredTermLoans_Current" 
  unitRef="pure" 
  decimals="3">
  0.085
</ind-as:InterestRateOfBorrowings>

<ind-as:BorrowingAmount 
  contextRef="D2017_SecuredTermLoans_Current" 
  unitRef="INR" 
  decimals="0">
  2000000000
</ind-as:BorrowingAmount>

<!-- Unsecured Bonds - Non-Current -->
<ind-as:MaturityDateOfBorrowings 
  contextRef="D2017_UnsecuredBonds_Noncurrent">
  2025-03-31
</ind-as:MaturityDateOfBorrowings>

<ind-as:BorrowingAmount 
  contextRef="D2017_UnsecuredBonds_Noncurrent" 
  unitRef="INR" 
  decimals="0">
  5000000000
</ind-as:BorrowingAmount>
```

---

### Example 2: Director Information (Typed Members)

**Table**: `DetailsOfDirectorsSigningFinancialStatements`

**Structure**:
```
Member Set 1: Director1Member
  ├── NameOfDirector (typed string)
  ├── DINOfDirector (typed integer)
  ├── DesignationOfDirector (typed enumeration)
  └── DateOfAppointment (typed date)

Member Set 2: Director2Member
  └── (same structure)
```

**Context Definition**:
```xml
<xbrli:context id="D2017_Director1">
  <xbrli:entity>
    <xbrli:identifier scheme="http://www.mca.gov.in/CIN">
      U24251MH2010PLC203456
    </xbrli:identifier>
    <xbrli:segment>
      <xbrli:typedMember 
        dimensionName="ind-as:DetailOfDirectorsAxis">
        Director1Member
      </xbrli:typedMember>
    </xbrli:segment>
  </xbrli:entity>
  <xbrli:period>
    <xbrli:startDate>2016-04-01</xbrli:startDate>
    <xbrli:endDate>2017-03-31</xbrli:endDate>
  </xbrli:period>
</xbrli:context>
```

**Facts**:
```xml
<ind-as:NameOfDirector 
  contextRef="D2017_Director1">
  Rajesh Kumar Singh
</ind-as:NameOfDirector>

<ind-as:DINOfDirector 
  contextRef="D2017_Director1" 
  unitRef="pure" 
  decimals="0">
  01234567
</ind-as:DINOfDirector>

<ind-as:DesignationOfDirector 
  contextRef="D2017_Director1">
  Managing Director
</ind-as:DesignationOfDirector>

<ind-as:DateOfAppointmentOfDirector 
  contextRef="D2017_Director1">
  2015-06-15
</ind-as:DateOfAppointmentOfDirector>
```

---

## Instance Document Code Examples

### Minimal Complete Instance (Skeleton)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xbrli:xbrl 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:xbrli="http://www.xbrl.org/2003/instance"
  xmlns:link="http://www.xbrl.org/2003/linkbase"
  xmlns:iso4217="http://www.xbrl.org/2003/iso4217"
  xmlns:ind-as="http://www.xbrl.org/in/2017-03-31/ind-as">

  <!-- Schema Reference -->
  <link:schemaRef 
    xlink:type="simple" 
    xlink:href="http://www.mca.gov.in/XBRL/2017/07/16/Taxonomy/Ind/in-ci-ent-2017-03-31.xsd"/>

  <!-- Units -->
  <xbrli:unit id="INR">
    <xbrli:measure>iso4217:INR</xbrli:measure>
  </xbrli:unit>

  <!-- Contexts -->
  <xbrli:context id="I2017">
    <xbrli:entity>
      <xbrli:identifier scheme="http://www.mca.gov.in/CIN">
        U24251MH2010PLC203456
      </xbrli:identifier>
    </xbrli:entity>
    <xbrli:period>
      <xbrli:instantDate>2017-03-31</xbrli:instantDate>
    </xbrli:period>
  </xbrli:context>

  <xbrli:context id="D2017">
    <xbrli:entity>
      <xbrli:identifier scheme="http://www.mca.gov.in/CIN">
        U24251MH2010PLC203456
      </xbrli:identifier>
    </xbrli:entity>
    <xbrli:period>
      <xbrli:startDate>2016-04-01</xbrli:startDate>
      <xbrli:endDate>2017-03-31</xbrli:endDate>
    </xbrli:period>
  </xbrli:context>

  <!-- Company General Information -->
  <ind-as:NameOfCompany contextRef="D2017">
    XYZ Limited
  </ind-as:NameOfCompany>

  <ind-as:IdentificationNumberOfCompany contextRef="D2017">
    U24251MH2010PLC203456
  </ind-as:IdentificationNumberOfCompany>

  <!-- Balance Sheet Items -->
  <ind-as:Cash contextRef="I2017" unitRef="INR" decimals="0">
    10000000
  </ind-as:Cash>

  <ind-as:PropertyPlantAndEquipment contextRef="I2017" unitRef="INR" decimals="0">
    500000000
  </ind-as:PropertyPlantAndEquipment>

  <!-- P&L Items -->
  <ind-as:RevenueFromOperations contextRef="D2017" unitRef="INR" decimals="0">
    50000000000
  </ind-as:RevenueFromOperations>

  <!-- Footnotes -->
  <link:footnoteLink xlink:type="extended">
    <link:loc 
      xlink:label="loc_ppe" 
      xlink:href="#PropertyPlantAndEquipmentNote"/>
    <link:footnote 
      xlink:label="fn_ppe" 
      xlink:type="simple">
      PPE includes land valued at INR 200 Mn acquired during the year
    </link:footnote>
    <link:footnoteArc 
      xlink:from="loc_ppe" 
      xlink:to="fn_ppe" 
      xlink:arcrole="http://www.xbrl.org/2003/arcrole/fact-footnote"/>
  </link:footnoteLink>

</xbrli:xbrl>
```

---

## Validation Error Troubleshooting

### Error Category 1: Schema/Format Errors (cvc-*)

| Error Code | Symptom | Cause | Fix |
|---|---|---|---|
| `cvc-datatype-valid.1.2.1` | "2017-03-31 not valid for date" | Wrong date format | Use YYYY-MM-DD |
| `cvc-id.1` | "No ID/IDREF binding for Rs" | Wrong currency code | Use ISO 4217 (INR, USD) |
| `cvc-complex-type.2.4` | "Invalid element order" | Tuple order wrong | Check presentation linkbase |

### Error Category 2: Business Rule Errors

| Error Type | Message | Cause | Resolution |
|---|---|---|---|
| **Mandatory Element Missing** | "Element X is required" | Forgot to enter required field | Check business rules for ELR |
| **Calculation Mismatch** | "Total Assets ≠ Liabilities + Equity" | Math doesn't work | Recalculate using linkbase rules |
| **Dimensional Validation** | "Element invalid for member Y" | Dimension requirements not met | Add all required axis members |
| **Period Overlap** | "Overlapping periods not allowed" | Duplicate or overlapping dates | Fix context period definitions |
| **Duplicate Context** | "Duplicate context elements" | Two identical scenario+period | Merge or rename contexts |

### Error Category 3: Data Type Errors

| Data Type | Wrong | Right | Error Message |
|---|---|---|---|
| Percentage | 60 | 0.60 | "Value must be between 0-1" |
| Boolean | yes | true | "'yes' not valid for boolean" |
| Date | 31/03/2017 | 2017-03-31 | "Not a valid date value" |
| Integer | 1000.5 | 1000 | "Decimal not allowed" |
| Currency | Rs | INR | "Unit Rs not defined" |

### Troubleshooting Workflow

```
1. Validate in MCA Tool
   ↓
2. Note Error Code
   ↓
3. Is it "cvc-*"?
   YES → Schema/XML issue → Contact software vendor
   NO → Continue
   ↓
4. Check Error Message
   ↓
5. Business Rule Error?
   YES → Verify against business rules → Add missing elements
   NO → Continue
   ↓
6. Dimensional Error?
   YES → Ensure all axes populated → Check member validity
   NO → Continue
   ↓
7. Data Type Error?
   YES → Fix data format → Re-validate
   NO → Review MCA manual Annexure II
   ↓
8. Pre-scrutiny Successful → Export PDF → Verify content
```

---

## Filing Checklist

### Pre-Filing Verification (Before Validation)

- [ ] Financial data reconciled with audited statements
- [ ] All amounts in INR (or documented subsidiary currency)
- [ ] Dates in YYYY-MM-DD format
- [ ] Current year (2016-04-01 to 2017-03-31)
- [ ] Previous year comparatives included
- [ ] Opening balance sheet included (if Ind AS adoption year)
- [ ] Context CIN matches company registration

### Mapping Verification

- [ ] All balance sheet line items mapped
- [ ] All P&L line items mapped
- [ ] All cash flow sections covered
- [ ] Mandatory tables completed (per business rules)
- [ ] Dimensional hierarchies followed
- [ ] Calculation relationships verified
- [ ] Footnotes for adjustments documented
- [ ] No custom extensions used

### Validation & Compliance

- [ ] Downloaded latest IND-AS 2017 taxonomy from MCA
- [ ] Instance document validates without errors
- [ ] All "warnings" reviewed and explained
- [ ] PDF export successful (non-zero size)
- [ ] PDF content matches filed financial statements
- [ ] Pre-scrutiny completed successfully on MCA tool
- [ ] No dimensional validation errors
- [ ] All mandatory elements present

### Quality Assurance

- [ ] PDF matches balance sheet exactly
- [ ] PDF matches P&L exactly
- [ ] PDF matches cash flow exactly
- [ ] Numbers reconcile to financial statements
- [ ] Decimal places consistent (0 for whole rupees)
- [ ] Opening/closing balances reconcile
- [ ] No mathematical errors in calculations
- [ ] Textual information clearly readable

### Filing Readiness

- [ ] Instance document backup created
- [ ] Form AOC-4 XBRL prepared (on MCA portal)
- [ ] Correct taxonomy selected ([IND-AS 2017])
- [ ] Instance file attached to form
- [ ] Form pre-scrutinized
- [ ] Authorized person identified
- [ ] Digital signature ready
- [ ] Filing deadline confirmed
- [ ] Fee payment arranged

---

**Document Version**: 1.0 Practical Implementation Guide  
**Last Updated**: December 2025  
**Target Audience**: XBRL Implementers, Finance Professionals, Software Vendors  
**Applicability**: IND AS 2017 Taxonomy Implementations


# XBRL Financial Reporting Format: Complete Developer Guide

## Part 1: What, How, Why - Conceptual Framework

### What is XBRL?

XBRL (eXtensible Business Reporting Language) is a standardized XML-based language for financial reporting. It enables structured, machine-readable financial data that can be automatically extracted, analyzed, and compared across companies and periods. For India, XBRL filing is mandatory under the Companies Act, 2013 for financial statements submitted to the Ministry of Corporate Affairs (MCA).

**Key Characteristics:**
- Tag-based semantic markup for financial concepts
- Standardized taxonomy (vocabulary) that maps accounting elements
- Dimensional reporting to handle complex table structures
- Instance documents containing actual financial data
- Schema-based validation ensuring compliance

### Why XBRL?

1. **Regulatory Compliance**: MCA mandates XBRL for companies filing Form AOC-4
2. **Data Standardization**: Eliminates inconsistent presentation across companies
3. **Automated Processing**: Regulators and analysts can extract data programmatically
4. **Comparability**: Standardized tags enable cross-company analysis
5. **Accessibility**: Financial information is machine-readable for data analytics
6. **Validation**: Built-in business rules catch errors before submission

### How XBRL Works - The Mapping Process

```
PDF Financial Statement
        ↓
    [Extract]
        ↓
Accounting Concepts (e.g., "Cash and Cash Equivalents")
        ↓
    [Map]
        ↓
XBRL Taxonomy Elements (e.g., "CashAndCashEquivalents")
        ↓
    [Create Instance Document]
        ↓
XML Structure with Contexts, Units, and Facts
        ↓
    [Validate & File]
        ↓
MCA Portal (Machine-Readable Format)
```

---

## Part 2: XBRL Document Structure and Tags

### A. High-Level Document Structure

An XBRL instance document is an XML file with three main components:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xbrli:xbrl 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xbrli="http://www.xbrl.org/2003/instance"
    xmlns:link="http://www.xbrl.org/2003/linkbase"
    xmlns:ind-as="http://www.xbrl.org/in/2017-03-31/ind-as"
    xmlns:in-ca="http://www.xbrl.org/in/2017-03-31/in-ca">

    <!-- 1. SCHEMA REFERENCE (Points to taxonomy) -->
    <link:schemaRef xlink:type="simple" 
        xlink:href="http://www.mca.gov.in/XBRL/2017/07/16/Taxonomy/Ind/in-ci-ent-2017-03-31.xsd"/>

    <!-- 2. CONTEXTS (Define time periods and entities) -->
    <xbrli:context id="...">
        <!-- Period and entity information -->
    </xbrli:context>

    <!-- 3. UNITS (Define measurement units for values) -->
    <xbrli:unit id="INR">
        <!-- Currency unit definition -->
    </xbrli:unit>

    <!-- 4. FACTS (Actual financial data) -->
    <ind-as:ElementName contextRef="..." unitRef="..." decimals="0">
        Value
    </ind-as:ElementName>

    <!-- 5. FOOTNOTES (Additional explanations) -->
    <link:footnoteLink>
        <!-- Footnote relationships -->
    </link:footnoteLink>

</xbrli:xbrl>
```

### B. Core Tags Explained

#### 2.1 Schema Reference Tag
```xml
<link:schemaRef xlink:type="simple" 
    xlink:href="http://www.mca.gov.in/XBRL/2017/07/16/Taxonomy/Ind/in-ci-ent-2017-03-31.xsd"/>
```

**Purpose**: Points to the taxonomy file that validates all elements
**Critical**: Must match the exact version for the financial year
**Location**: Always the first tag in any instance document

---

#### 2.2 Context (xbrli:context)

Contexts define the "who, what, when" for each fact:

```xml
<!-- DURATION CONTEXT (for Profit & Loss / Cash Flow) -->
<xbrli:context id="D2024_MainAxis">
    <xbrli:entity>
        <xbrli:identifier scheme="http://www.mca.gov.in/CIN">
            L17110MH1973PLC019786
        </xbrli:identifier>
    </xbrli:entity>
    <xbrli:period>
        <xbrli:startDate>2024-04-01</xbrli:startDate>
        <xbrli:endDate>2025-03-31</xbrli:endDate>
    </xbrli:period>
</xbrli:context>

<!-- INSTANT CONTEXT (for Balance Sheet) -->
<xbrli:context id="I2025_MainAxis">
    <xbrli:entity>
        <xbrli:identifier scheme="http://www.mca.gov.in/CIN">
            L17110MH1973PLC019786
        </xbrli:identifier>
    </xbrli:entity>
    <xbrli:period>
        <xbrli:instantDate>2025-03-31</xbrli:instantDate>
    </xbrli:period>
</xbrli:context>

<!-- DIMENSIONAL CONTEXT (with table breakdowns) -->
<xbrli:context id="D2024_ReservesBreakdown">
    <xbrli:entity>
        <xbrli:identifier scheme="http://www.mca.gov.in/CIN">
            L17110MH1973PLC019786
        </xbrli:identifier>
    </xbrli:entity>
    <xbrli:period>
        <xbrli:startDate>2024-04-01</xbrli:startDate>
        <xbrli:endDate>2025-03-31</xbrli:endDate>
    </xbrli:period>
    <xbrli:scenario>
        <xbrli:explicitMember 
            dimension="ind-as:EquityComponentAxis">
            ind-as:ReservesMember
        </xbrli:explicitMember>
    </xbrli:scenario>
</xbrli:context>
```

**Context Structure Elements:**
- `xbrli:entity`: Contains CIN (Unique identifier for company)
- `xbrli:period`: Contains date range (duration) or specific date (instant)
- `xbrli:scenario`: Contains dimension members for breakdowns (optional)

**Key Rules:**
- CIN scheme must always be: `http://www.mca.gov.in/CIN`
- Duration contexts: For P&L, Cash Flow, changes in accounts
- Instant contexts: For Balance Sheet snapshot
- Dimensional contexts: For detailed table disclosures

---

#### 2.3 Units (xbrli:unit)

```xml
<!-- CURRENCY UNIT -->
<xbrli:unit id="INR">
    <xbrli:measure>iso4217:INR</xbrli:measure>
</xbrli:unit>

<!-- SHARE COUNT UNIT -->
<xbrli:unit id="Shares">
    <xbrli:measure>xbrli:shares</xbrli:measure>
</xbrli:unit>

<!-- PURE UNIT (for ratios, percentages) -->
<xbrli:unit id="Pure">
    <xbrli:measure>xbrli:pure</xbrli:measure>
</xbrli:unit>
```

**Usage:**
- All monetary amounts reference `unitRef="INR"`
- Share counts reference `unitRef="Shares"`
- Percentages and ratios reference `unitRef="Pure"` (values 0-1)

---

#### 2.4 Fact Tags (Financial Data Elements)

```xml
<!-- SIMPLE NUMERIC FACT -->
<ind-as:CashAndCashEquivalents 
    contextRef="I2025_MainAxis" 
    unitRef="INR" 
    decimals="0">
    50000000000
</ind-as:CashAndCashEquivalents>

<!-- FACT WITH DIMENSION -->
<ind-as:CapitalReserves 
    contextRef="I2025_ReservesBreakdown" 
    unitRef="INR" 
    decimals="0">
    10000000000
</ind-as:CapitalReserves>

<!-- TEXTUAL FACT (String data, no unit) -->
<ind-as:NameOfCompany>
    RELIANCE INDUSTRIES LIMITED
</ind-as:NameOfCompany>

<!-- BOOLEAN FACT -->
<ind-as:WhetherCompanyListedOnStockExchange>
    true
</ind-as:WhetherCompanyListedOnStockExchange>

<!-- FACT WITH FOOTNOTE -->
<ind-as:PropertyPlantAndEquipment 
    contextRef="I2025_MainAxis" 
    unitRef="INR" 
    decimals="0"
    id="fact_ppe_1">
    350000000000
</ind-as:PropertyPlantAndEquipment>
```

**Attributes Explained:**
- `contextRef`: Links to context defining period/entity/dimensions
- `unitRef`: Unit of measurement (INR, Shares, Pure)
- `decimals`: Decimal precision (0 for whole numbers, 2 for two decimals)
- `id`: Optional, used when attaching footnotes

**Data Type Rules:**
- Numeric: No commas, signs handled separately
- Strings: Use HTML entity encoding (&amp;, &lt;, &gt;)
- Dates: yyyy-mm-dd format only
- Boolean: 'true' or 'false' (lowercase)
- Percentages: 0.60 for 60% (not 60)

---

#### 2.5 Footnotes (link:footnoteLink)

```xml
<!-- FOOTNOTE STRUCTURE -->
<link:footnoteLink xlink:type="extended">
    <!-- Link to the fact being explained -->
    <link:loc xlink:type="locator" 
        xlink:href="#fact_ppe_1" 
        xlink:label="fact_1"/>
    
    <!-- The footnote content -->
    <link:footnote xlink:type="resource" 
        xlink:label="note_1"
        xml:lang="en">
        <div class="noteText1">
            Property includes land at carrying value of ₹25,000 crores
        </div>
    </link:footnote>
    
    <!-- Arc connecting fact to footnote -->
    <link:footnoteArc xlink:type="arc" 
        xlink:from="fact_1" 
        xlink:to="note_1" 
        xlink:arcrole="http://www.xbrl.org/2003/arcrole/fact-footnote"/>
</link:footnoteLink>
```

**Key Points:**
- Footnote `xlink:href` must start with `#` (fragment reference)
- HTML must follow guidelines (only allowed tags: div, span, p, br, table, tr, td, th)
- Use predefined CSS classes: `noteText1`, `noteText2`, `highlightedText1`, etc.
- Every footnote must be linked to at least one fact

---

## Part 3: Code Implementation - From PDF to XBRL

### Step 1: Extract Data from PDF

```python
import pandas as pd
from pdfplumber import PDF

# Example: Extract Balance Sheet data from PDF
def extract_balance_sheet(pdf_path):
    with PDF.open(pdf_path) as pdf:
        # Navigate to Balance Sheet page
        bs_page = pdf.pages[10]  # Assuming page 10
        
        # Extract table
        table = bs_page.extract_table()
        
        bs_data = {
            'Assets': {},
            'Liabilities': {},
            'Equity': {}
        }
        
        # Parse rows
        for row in table:
            item_name = row[0]
            current_year = float(row[1].replace(',', ''))
            previous_year = float(row[2].replace(',', ''))
            
            bs_data['Assets'][item_name] = {
                'current': current_year,
                'previous': previous_year
            }
        
        return bs_data
```

### Step 2: Create Context Objects

```python
from datetime import datetime
import uuid

class XBRLContext:
    def __init__(self, company_cin, context_type='instant', 
                 start_date=None, end_date=None, members=None):
        self.cin = company_cin
        self.context_type = context_type  # 'instant' or 'duration'
        self.start_date = start_date
        self.end_date = end_date
        self.members = members or {}  # for dimensional reporting
        self.id = self._generate_id()
    
    def _generate_id(self):
        if self.context_type == 'instant':
            date_str = self.end_date.strftime('%Y%m%d')
            return f"I{date_str}"
        else:
            start_str = self.start_date.strftime('%Y%m%d')
            end_str = self.end_date.strftime('%Y%m%d')
            return f"D{start_str}_D{end_str}"
    
    def to_xml(self):
        xml = f'<xbrli:context id="{self.id}">\n'
        xml += f'    <xbrli:entity>\n'
        xml += f'        <xbrli:identifier scheme="http://www.mca.gov.in/CIN">'
        xml += f'{self.cin}</xbrli:identifier>\n'
        xml += f'    </xbrli:entity>\n'
        xml += f'    <xbrli:period>\n'
        
        if self.context_type == 'instant':
            instant_date = self.end_date.strftime('%Y-%m-%d')
            xml += f'        <xbrli:instantDate>{instant_date}</xbrli:instantDate>\n'
        else:
            start = self.start_date.strftime('%Y-%m-%d')
            end = self.end_date.strftime('%Y-%m-%d')
            xml += f'        <xbrli:startDate>{start}</xbrli:startDate>\n'
            xml += f'        <xbrli:endDate>{end}</xbrli:endDate>\n'
        
        xml += f'    </xbrli:period>\n'
        
        # Add scenario for dimensional members if present
        if self.members:
            xml += f'    <xbrli:scenario>\n'
            for dimension, member in self.members.items():
                xml += f'        <xbrli:explicitMember dimension="{dimension}">'
                xml += f'{member}</xbrli:explicitMember>\n'
            xml += f'    </xbrli:scenario>\n'
        
        xml += f'</xbrli:context>\n'
        return xml

# Usage
context_bs = XBRLContext(
    company_cin='L17110MH1973PLC019786',
    context_type='instant',
    end_date=datetime(2025, 3, 31)
)

context_pl = XBRLContext(
    company_cin='L17110MH1973PLC019786',
    context_type='duration',
    start_date=datetime(2024, 4, 1),
    end_date=datetime(2025, 3, 31)
)

# With dimensions (for reserves breakdown)
context_reserves = XBRLContext(
    company_cin='L17110MH1973PLC019786',
    context_type='instant',
    end_date=datetime(2025, 3, 31),
    members={
        'ind-as:EquityComponentAxis': 'ind-as:ReservesMember'
    }
)

print(context_bs.to_xml())
```

### Step 3: Define Taxonomy Mappings

```python
# Mapping of accounting items to XBRL taxonomy elements
BALANCE_SHEET_MAPPING = {
    'Cash and Cash Equivalents': {
        'element': 'ind-as:CashAndCashEquivalents',
        'type': 'monetary',
        'period_type': 'instant'
    },
    'Trade Receivables': {
        'element': 'ind-as:TradeReceivables',
        'type': 'monetary',
        'period_type': 'instant'
    },
    'Property, Plant and Equipment': {
        'element': 'ind-as:PropertyPlantAndEquipment',
        'type': 'monetary',
        'period_type': 'instant'
    },
    'Total Assets': {
        'element': 'ind-as:Assets',
        'type': 'monetary',
        'period_type': 'instant'
    },
    'Equity Share Capital': {
        'element': 'ind-as:EquityShareCapital',
        'type': 'monetary',
        'period_type': 'instant'
    },
    'Reserves and Surplus': {
        'element': 'ind-as:ReservesAndSurplus',
        'type': 'monetary',
        'period_type': 'instant'
    }
}

P_L_MAPPING = {
    'Revenue from Operations': {
        'element': 'ind-as:RevenueFromOperations',
        'type': 'monetary',
        'period_type': 'duration'
    },
    'Cost of Materials Consumed': {
        'element': 'ind-as:CostOfMaterialsConsumed',
        'type': 'monetary',
        'period_type': 'duration'
    },
    'Profit Before Tax': {
        'element': 'ind-as:ProfitBeforeTax',
        'type': 'monetary',
        'period_type': 'duration'
    },
    'Net Profit After Tax': {
        'element': 'ind-as:NetProfitLoss',
        'type': 'monetary',
        'period_type': 'duration'
    }
}
```

### Step 4: Create XBRL Facts

```python
class XBRLFact:
    def __init__(self, element, context_ref, unit_ref, decimals, value, 
                 fact_id=None, namespace='ind-as'):
        self.element = element
        self.context_ref = context_ref
        self.unit_ref = unit_ref
        self.decimals = decimals
        self.value = value
        self.fact_id = fact_id
        self.namespace = namespace
    
    def to_xml(self):
        full_element = f"{self.namespace}:{self.element}"
        
        # Validate and format value
        if self.unit_ref == 'INR':
            # Monetary value - ensure integer
            value_str = str(int(self.value))
        elif self.unit_ref == 'Pure':
            # Percentage/ratio - ensure between 0 and 1
            value_str = str(float(self.value))
        else:
            value_str = str(self.value)
        
        xml = f'<{full_element} '
        xml += f'contextRef="{self.context_ref}" '
        xml += f'unitRef="{self.unit_ref}" '
        xml += f'decimals="{self.decimals}"'
        
        if self.fact_id:
            xml += f' id="{self.fact_id}"'
        
        xml += f'>{value_str}</{full_element}>'
        
        return xml

# Usage
fact1 = XBRLFact(
    element='CashAndCashEquivalents',
    context_ref='I20250331',
    unit_ref='INR',
    decimals='0',
    value=50000000000
)

fact2 = XBRLFact(
    element='RevenueFromOperations',
    context_ref='D20250331',
    unit_ref='INR',
    decimals='0',
    value=250000000000
)

print(fact1.to_xml())
print(fact2.to_xml())
```

### Step 5: Build Complete XBRL Document

```python
import xml.etree.ElementTree as ET

class XBRLBuilder:
    def __init__(self, company_cin, taxonomy_ref):
        self.company_cin = company_cin
        self.taxonomy_ref = taxonomy_ref
        self.contexts = []
        self.units = {}
        self.facts = []
        self.footnotes = []
    
    def add_context(self, context):
        self.contexts.append(context)
    
    def add_unit(self, unit_id, measure):
        self.units[unit_id] = measure
    
    def add_fact(self, fact):
        self.facts.append(fact)
    
    def generate_xbrl(self):
        """Generate complete XBRL XML"""
        
        xml_header = '''<?xml version="1.0" encoding="UTF-8"?>
<xbrli:xbrl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xbrli="http://www.xbrl.org/2003/instance"
    xmlns:link="http://www.xbrl.org/2003/linkbase"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:ind-as="http://www.xbrl.org/in/2017-03-31/ind-as"
    xmlns:in-ca="http://www.xbrl.org/in/2017-03-31/in-ca"
    xmlns:iso4217="http://www.xbrl.org/2003/iso4217">

'''
        
        # Schema reference
        xml_content = xml_header
        xml_content += f'<link:schemaRef xlink:type="simple" xlink:href="{self.taxonomy_ref}"/>\n'
        
        # Contexts
        for context in self.contexts:
            xml_content += context.to_xml()
        
        # Units
        xml_content += '\n<!-- UNITS -->\n'
        for unit_id, measure in self.units.items():
            xml_content += f'<xbrli:unit id="{unit_id}">\n'
            xml_content += f'    <xbrli:measure>{measure}</xbrli:measure>\n'
            xml_content += f'</xbrli:unit>\n'
        
        # Facts
        xml_content += '\n<!-- FACTS -->\n'
        for fact in self.facts:
            xml_content += fact.to_xml() + '\n'
        
        # Footnotes
        if self.footnotes:
            xml_content += '\n<!-- FOOTNOTES -->\n'
            xml_content += self._generate_footnotes()
        
        xml_content += '\n</xbrli:xbrl>'
        
        return xml_content
    
    def _generate_footnotes(self):
        """Generate footnote linkbase"""
        xml = '<link:footnoteLink xlink:type="extended">\n'
        
        for idx, (fact_id, note_text) in enumerate(self.footnotes):
            xml += f'    <link:loc xlink:type="locator" xlink:href="#{fact_id}" xlink:label="fact_{idx}"/>\n'
            xml += f'    <link:footnote xlink:type="resource" xlink:label="note_{idx}" xml:lang="en">\n'
            xml += f'        <div class="noteText1">{note_text}</div>\n'
            xml += f'    </link:footnote>\n'
            xml += f'    <link:footnoteArc xlink:type="arc" xlink:from="fact_{idx}" xlink:to="note_{idx}" '
            xml += f'xlink:arcrole="http://www.xbrl.org/2003/arcrole/fact-footnote"/>\n'
        
        xml += '</link:footnoteLink>\n'
        return xml
    
    def save_xbrl(self, filename):
        """Save XBRL document to file"""
        content = self.generate_xbrl()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"XBRL document saved to {filename}")

# Complete Usage Example
builder = XBRLBuilder(
    company_cin='L17110MH1973PLC019786',
    taxonomy_ref='http://www.mca.gov.in/XBRL/2017/07/16/Taxonomy/Ind/in-ci-ent-2017-03-31.xsd'
)

# Add contexts
from datetime import datetime

context_bs = XBRLContext(
    company_cin='L17110MH1973PLC019786',
    context_type='instant',
    end_date=datetime(2025, 3, 31)
)
builder.add_context(context_bs)

context_pl = XBRLContext(
    company_cin='L17110MH1973PLC019786',
    context_type='duration',
    start_date=datetime(2024, 4, 1),
    end_date=datetime(2025, 3, 31)
)
builder.add_context(context_pl)

# Add units
builder.add_unit('INR', 'iso4217:INR')
builder.add_unit('Shares', 'xbrli:shares')
builder.add_unit('Pure', 'xbrli:pure')

# Add facts
builder.add_fact(XBRLFact(
    element='CashAndCashEquivalents',
    context_ref='I20250331',
    unit_ref='INR',
    decimals='0',
    value=50000000000
))

builder.add_fact(XBRLFact(
    element='RevenueFromOperations',
    context_ref='D20250331',
    unit_ref='INR',
    decimals='0',
    value=250000000000
))

builder.add_fact(XBRLFact(
    element='EquityShareCapital',
    context_ref='I20250331',
    unit_ref='INR',
    decimals='0',
    value=10000000000,
    fact_id='fact_capital_1'
))

# Add footnote
builder.footnotes.append(('fact_capital_1', 'Par value per share is ₹10'))

# Generate and save
builder.save_xbrl('reliance_standalone.xml')
```

---

## Part 4: Common XBRL Elements from Reliance Example

### Balance Sheet Elements

```python
RELIANCE_BS_ELEMENTS = {
    # Assets
    'CashAndCashEquivalents': 'ind-as:CashAndCashEquivalents',
    'TradeReceivables': 'ind-as:TradeReceivables',
    'Inventories': 'ind-as:Inventories',
    'CurrentInvestments': 'ind-as:CurrentInvestments',
    'OtherCurrentAssets': 'ind-as:OtherCurrentAssets',
    'PropertyPlantEquipment': 'ind-as:PropertyPlantAndEquipment',
    'RightOfUseAssets': 'ind-as:RightOfUseAssets',
    'Goodwill': 'ind-as:Goodwill',
    'IntangibleAssets': 'ind-as:IntangibleAssets',
    'FinancialAssets': 'ind-as:FinancialAssets',
    'Investments': 'ind-as:Investments',
    'DeferredTaxAssets': 'ind-as:DeferredTaxAssets',
    'OtherNoncurrentAssets': 'ind-as:OtherNoncurrentAssets',
    'TotalAssets': 'ind-as:Assets',
    
    # Liabilities
    'BorrowingsCurrent': 'ind-as:CurrentBorrowings',
    'BorrowingsNoncurrent': 'ind-as:NoncurrentBorrowings',
    'TradePayables': 'ind-as:TradePayables',
    'CurrentTaxLiabilities': 'ind-as:CurrentTaxLiability',
    'LeaseLiabilities': 'ind-as:LeaseLiabilities',
    'OtherCurrentLiabilities': 'ind-as:OtherCurrentLiabilities',
    'DeferredTaxLiabilities': 'ind-as:DeferredTaxLiabilities',
    'OtherNoncurrentLiabilities': 'ind-as:OtherNoncurrentLiabilities',
    'TotalLiabilities': 'ind-as:Liabilities',
    
    # Equity
    'EquityShareCapital': 'ind-as:EquityShareCapital',
    'ReservesAndSurplus': 'ind-as:ReservesAndSurplus',
    'CapitalReserves': 'ind-as:CapitalReserves',
    'SecuritiesPremiumReserve': 'ind-as:SecuritiesPremiumReserve',
    'GeneralReserve': 'ind-as:GeneralReserve',
    'RetainedEarnings': 'ind-as:RetainedEarnings',
    'OtherComprehensiveIncome': 'ind-as:OtherComprehensiveIncome',
    'TotalEquity': 'ind-as:Equity',
    'MinorityInterest': 'ind-as:MinorityInterest'
}
```

### Income Statement Elements

```python
RELIANCE_IS_ELEMENTS = {
    'RevenueFromOperations': 'ind-as:RevenueFromOperations',
    'OtherOperatingRevenue': 'ind-as:OtherOperatingRevenue',
    'TotalOperatingRevenue': 'ind-as:TotalOperatingRevenue',
    
    'CostOfMaterialsConsumed': 'ind-as:CostOfMaterialsConsumed',
    'ChangesInInventoriesOfFinishedGoods': 'ind-as:ChangesInInventoriesOfFinishedGoods',
    'EmployeeBenefitsExpense': 'ind-as:EmployeeBenefitsExpense',
    'DepreciationAndAmortisation': 'ind-as:DepreciationAndAmortisation',
    'OtherOperatingExpenses': 'ind-as:OtherOperatingExpenses',
    'TotalOperatingCosts': 'ind-as:TotalOperatingCosts',
    
    'EBITDAFromOperations': 'ind-as:EBITDAFromOperations',
    'ProfitFromOperations': 'ind-as:ProfitFromOperations',
    
    'FinanceCosts': 'ind-as:FinanceCosts',
    'OtherIncome': 'ind-as:OtherIncome',
    'ProfitBeforeTax': 'ind-as:ProfitBeforeTax',
    
    'TaxExpense': 'ind-as:TaxExpense',
    'CurrentTaxExpense': 'ind-as:CurrentTaxExpense',
    'DeferredTaxExpense': 'ind-as:DeferredTaxExpense',
    'PreviousYearTaxAdjustment': 'ind-as:PreviousYearAdjustment',
    
    'NetProfitLoss': 'ind-as:NetProfitLoss',
    'OtherComprehensiveIncomeNet': 'ind-as:OtherComprehensiveIncomeNet',
    'TotalComprehensiveIncome': 'ind-as:TotalComprehensiveIncome',
    
    'EarningsPerShare': 'ind-as:EarningsPerShare',
    'BasicEPS': 'ind-as:EarningsPerShareBasic',
    'DilutedEPS': 'ind-as:EarningsPerShareDiluted'
}
```

### Dimensional Members (for detailed disclosures)

```python
# Borrowing Classification
BORROWING_DIMENSIONS = {
    'Bonds': 'ind-as:BondsMember',
    'Debentures': 'ind-as:DebenturesMember',
    'TermLoans': 'ind-as:TermLoansMember',
    'TermLoansFromBanks': 'ind-as:TermLoansFromBanksMember',
    'CommercialPaper': 'ind-as:CommercialPaperMember',
    'SecuredBorrowings': 'ind-as:SecuredBorrowingsMember',
    'UnsecuredBorrowings': 'ind-as:UnsecuredBorrowingsMember',
    'Current': 'ind-as:CurrentMember',
    'Noncurrent': 'ind-as:NoncurrentMember'
}

# Equity Components
EQUITY_DIMENSIONS = {
    'CapitalReserves': 'ind-as:CapitalReservesMember',
    'SecuritiesPremium': 'ind-as:SecuritiesPremiumReserveMember',
    'GeneralReserve': 'ind-as:GeneralReserveMember',
    'SpecialReserve': 'ind-as:SpecialReserveMember',
    'RetainedEarnings': 'ind-as:RetainedEarningsMember',
    'OtherComprehensiveIncome': 'ind-as:OtherRetainedEarningMember'
}
```

---

## Part 5: Validation and Filing Process

### Validation Checklist

```python
class XBRLValidator:
    """Validate XBRL instance documents against rules"""
    
    @staticmethod
    def validate_file(xbrl_file):
        """Run all validations"""
        errors = []
        warnings = []
        
        # 1. Schema validity
        if not XBRLValidator.is_schema_valid(xbrl_file):
            errors.append("CVC-ERROR: XML not schema-valid")
        
        # 2. Context validation
        contexts = XBRLValidator.extract_contexts(xbrl_file)
        if not XBRLValidator.validate_contexts(contexts):
            errors.append("Context errors found")
        
        # 3. Unit validation
        units = XBRLValidator.extract_units(xbrl_file)
        if not XBRLValidator.validate_units(units):
            errors.append("Unit definition errors")
        
        # 4. Fact validation
        facts = XBRLValidator.extract_facts(xbrl_file)
        for fact in facts:
            fact_errors = XBRLValidator.validate_fact(fact)
            errors.extend(fact_errors)
        
        # 5. Business rule validation
        br_errors = XBRLValidator.validate_business_rules(facts)
        errors.extend(br_errors)
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    @staticmethod
    def validate_fact(fact):
        """Validate individual fact"""
        errors = []
        
        # Check contextRef exists
        if not fact.get('contextRef'):
            errors.append(f"Fact missing contextRef")
        
        # Check unitRef for monetary
        if 'CashAndCashEquivalents' in fact.get('element', ''):
            if fact.get('unitRef') != 'INR':
                errors.append(f"Monetary element must have INR unit")
        
        # Check decimal places
        decimals = int(fact.get('decimals', 0))
        if decimals < 0:
            errors.append(f"Decimals cannot be negative")
        
        return errors
```

### Pre-Filing Checklist

```
✓ XBRL Document Created
  - Schema reference points to correct taxonomy
  - Encoding is UTF-8
  - All mandatory elements present

✓ Contexts Defined
  - CIN in correct scheme (http://www.mca.gov.in/CIN)
  - Instant contexts for balance sheet dates
  - Duration contexts for P&L and CF periods
  - No duplicate contexts
  - All defined contexts referenced

✓ Data Accuracy
  - Current year and previous year both entered
  - Calculation relationships follow taxonomy
  - Dimensions used correctly
  - No conflicting values

✓ Unit Definitions
  - INR used for all monetary items
  - Shares unit for share count
  - Pure unit for percentages (0-1 range)
  - No unused units defined

✓ Footnotes
  - Properly formatted HTML
  - Only allowed tags used
  - All footnotes linked to facts

✓ Validation
  - Passed MCA XBRL validation tool
  - Business rules validated
  - Pre-scrutiny completed
  - PDF conversion successful

✓ Filing
  - Attached to Form AOC-4 XBRL
  - Uploaded on MCA portal
  - Confirmation received
```

---

## Part 6: Key Takeaways for Development

| Aspect | Key Point |
|--------|-----------|
| **Document Type** | XML-based with strict structure |
| **Core Components** | Contexts, Units, Facts, Footnotes |
| **Data Mapping** | Requires understanding of both accounting and XBRL taxonomy |
| **Validation** | Multiple layers: schema, business rules, dimension consistency |
| **Complexity** | Scales with dimensional reporting (reserves, investments, related party) |
| **Common Errors** | Wrong currency codes, percentage format, context references, dimension members |
| **Development Timeline** | Extraction (2-3 days) → Mapping (3-5 days) → Coding (5-7 days) → Testing (2-3 days) |

---

**References:**
- MCA 21 XBRL Filing Manual for Ind-AS
- XBRL International Specification (http://www.xbrl.org)
- Indian Accounting Standards Taxonomy 2017-03-31
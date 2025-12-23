# XBRL Financial Reporting Format

## XBRL Document Structure and Tags

An XBRL instance document is an XML file with 5 main components:

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
- Just a one-line with links to the MCA that validates the report
- Points to the taxonomy file that validates all elements
- Always the first tag in any instance document

---

#### 2.2 Context (xbrli:context)

Contexts define the exact details, including IDs, for each entry/facts/values given in the report.

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
- id general formula: `“{type of context letter}{year of entry}_{type of name of entry}”`

**Child Tags:**
- `xbrli:entity`: Contains CIN (Unique identifier for company)
- `xbrli:period`: Contains date range (duration) or specific date (instant)
- <mark>`xbrli:scenario`: Contains dimension members for breakdowns (optional)</mark>

**Rules:**
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

- All monetary amounts reference `unitRef="INR"`
- Share counts reference `unitRef="Shares"`
- Percentages and ratios reference `unitRef="Pure"` (values 0-1)

---

#### 2.4 Fact Tags (Financial Data Entries)

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

- `contextRef`: Links to context defining period/entity/dimensions
- `unitRef`: Unit of measurement (INR, Shares, Pure)
- `decimals`: Decimal precision (0 for whole numbers, 2 for two decimals)
- <mark>`id`: Optional, used when attaching footnotes</mark>

**Data Type Rules:**
- Numeric: No commas, signs handled separately
- Strings: Use HTML entity encoding (&amp;, &lt;, &gt;)
- Dates: yyyy-mm-dd format only
- Boolean: 'true' or 'false' (lowercase)
- Percentages: 0.60 for 60% (not 60)

---

#### 2.5 Footnotes (link:footnoteLink)

A brief explanatory note corresponding to facts entries.

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

- Footnote `xlink:href` must start with `#` (fragment reference)
- HTML must follow guidelines (only allowed tags: div, span, p, br, table, tr, td, th)
- Use predefined CSS classes: `noteText1`, `noteText2`, `highlightedText1`, etc.
- Every footnote must be linked to at least one fact

### Refined Prompt (with page provenance)

We are now entering the refinement stage of the application development. The file **`xxx_meta.json`** contains multiple ESIA-related tables extracted from the original ESIA PDF (**Final ESIA Report – Pharsalus Gold Mine**, 465 pages). Each table entry includes at least:

* A unique identifier (e.g. `table_id`, `position`)
* The **page number** in the original ESIA PDF (field `page`)
* The table content (markdown / pipe-delimited format in `content`)
* Optional metadata such as bounding boxes. 

Your task is to design and implement a complete solution for **extracting, structuring, formatting and visualising** these tables as a professional, reviewer-friendly HTML interface called **`xxx_fact_browser.html`**, together with a companion **`xxx_fact_browser.xlsx`** workbook.

Act as a senior **ESIA technical reviewer and report designer** familiar with IFC Performance Standards, World Bank ESF, and ADB safeguards. The outputs must support both **internal reviewers** and **external reviewers (IFC, World Bank, ADB, lenders, regulators)** in quickly locating and validating facts in the original ESIA.

---

#### 1. Core Objectives

1. Transform `xxx_meta.json` into an HTML “fact browser” with:

   * Clear thematic organisation of ESIA tables.
   * Collapsible sections to manage volume.
   * Powerful search and navigation.
2. Preserve and expose **page-level provenance** so reviewers can always trace each fact back to the exact **page(s) of the original ESIA PDF**.
3. Generate a parallel **Excel workbook** mirroring the same structure and provenance to facilitate offline review and analysis.

---

#### 2. Data Interpretation

* Assume each table object in `xxx_meta.json` has, at minimum:

  * `table_id`
  * `page` (integer, 1-based page number in the original ESIA PDF)
  * `position` (e.g. `"table_0_page_8"`)
  * `content` (pipe-delimited text representing a table, as already extracted) 
* Where practical, infer a **logical category** (e.g. “Contents”, “Legislation”, “Physical Environment”, “Ecology”, “Social Environment”, “Impact Assessment”, “Management Plans”, “Monitoring”, “Closure”) from the heading rows.

Design your processing logic so that new ESIA meta files with similar structure can be handled without manual adjustment.

---

#### 3. HTML Design Requirements (`xxx_fact_browser.html`)

1. **Overall Layout**

   * Clean, responsive HTML, no external frameworks required.
   * A left (or top) navigation area listing high-level categories (e.g. Chapters, Themes).
   * A main content area displaying collapsible sections.

2. **Collapsible Sections**

   * Group tables into logical sections (by chapter / theme / category).
   * Each section should show:

     * Section title (e.g. “3.4 General National Environmental Legislation”).
     * Optional short description if it can be inferred from the data.
     * One or more tables rendered as HTML `<table>` elements.
   * Each **table block** must clearly show at least:

     * Table label or inferred title.
     * **Source page information**: e.g. “Source: ESIA PDF, page 38” (or “pages 38–40” if you infer a span).
     * Optionally, a technical “ID” such as `table_1_page_9` for debugging. 

3. **Page Number Provenance**

   * For **every fact row**, ensure provenance is obvious:

     * At minimum, display the **page number** for the table at the top of the table block.
     * Optionally, add a dedicated **“Page” column** in the table where appropriate, especially when content likely spans multiple pages.
   * Embed the page number as a data attribute (e.g. `data-page="38"`) on the container element for each table to support filtering and future enhancements.
   * If a base URL or known file name for the PDF is available, design the HTML so that page numbers can later be turned into deep links (for example, a placeholder link such as `href="#pdf-page-38"` or a configurable template string).

4. **Search Functionality**

   * Implement a **global search box** (pure JavaScript, no external libraries).
   * Behaviour:

     * Search across all tables and all visible text cells.
     * Highlight matching cells and automatically expand any collapsed section containing a match.
     * Provide a simple indication of how many matches are found and where (e.g. section/table names).
     * Allow case-insensitive search.
   * Search results should **not** remove data; they should filter or grey-out non-matching rows/sections or simply highlight matches, as you deem most usable.

5. **Reviewer-Centric UX**

   * Design for ESIA reviewer workflows:

     * Ability to quickly jump to key sections (e.g. impacts, mitigation, monitoring, management plans).
     * Immediate visibility of **page numbers** next to facts.
     * Clear separation of baseline, impact assessment, mitigation and monitoring content where identifiable.
   * Avoid cluttered styling; prioritise legibility for long reading sessions.

---

#### 4. Excel Design Requirements (`xxx_fact_browser.xlsx`)

1. Create one **worksheet per ESIA table** or per logical group of tables (choose the structure that is most usable, but keep it consistent).
2. Each worksheet must include:

   * A clear sheet name (sanitised, short, and valid for Excel, derived from table title or section heading).
   * All rows and columns from the table content.
   * A dedicated column (e.g. `Source_Page`) containing the **page number from the original ESIA PDF** for that table (or row, if you choose a more granular scheme).
   * Where multiple pages are implied, store them as a range string (e.g. `38–40`).
3. Ensure the workbook is easily navigable for ESIA reviewers (freeze header row, reasonable column widths, etc., if straightforward to implement).

---

#### 5. Python Script Requirements

Write a complete, standalone Python script that can be run from the command line as:

```bash
python build_fact_browser.py --input xxx_meta.json --output ./single_source_output
```

Requirements:

1. **Inputs and Outputs**

   * Input: `--input` path to `xxx_meta.json`.
   * Output: `--output` directory (created if it does not exist).
   * The script must generate within this directory:

     * `xxx_fact_browser.html`
     * `xxx_fact_browser.xlsx`

2. **Implementation Details**

   * Use standard and widely available libraries only:

     * `json`, `argparse`, `pathlib` (standard library)
     * `pandas` + `openpyxl` for Excel generation.
   * Parse `xxx_meta.json`, reconstruct each table from its `content`, and attach provenance from the `page` and other relevant fields.
   * Encapsulate logic in clear, testable functions (e.g. `load_meta`, `build_tables`, `build_html`, `build_excel`).
   * Include docstrings and inline comments that explain key design choices, especially how **provenance is preserved**.

3. **HTML & JS**

   * Do not rely on external CDNs or frameworks; use inline CSS and plain JavaScript.
   * Ensure the A4-friendly layout prints reasonably well for reviewers who prefer hard copy.

---

#### 6. ESIA / Lender Perspective

Throughout your design, think like an ESIA reviewer for IFC, WB, and ADB:

* The **ability to jump from a fact to the originating ESIA page** is essential.
* Tables should be structured to support cross-checking against IFC PS, WB ESF, and ADB requirements (policy, baseline, impact, mitigation, monitoring, management systems, closure).
* Maintain a professional, audit-ready feel to both HTML and Excel outputs.

---

If you wish, I can now also draft the actual `build_fact_browser.py` implementation that follows this specification.

# WEEKLY SHOWING REPORTS AUTOMATION PROTOCOL (REAL ESTATE INSIGHTS)

## PROJECT OBJECTIVE
To automatically process weekly progress logs, marketing metrics, client/agent feedback, and market comparative data for all active listings across all agents. Modify corresponding HTML files within the local GitHub Pages repository, apply cache busting, localized Spanish adaptations, milestone triggers, and deploy changes to production. This ensures both root-level and agent-specific client portals remain 100% updated in real-time.

## STATIC SYSTEM CONFIGURATIONS (DO NOT RE-INVESTIGATE)
1. **OPERATIONAL BASE DIRECTORY:** All codebase files, scripts, and repository templates live within `B:\Downloads Compass\Real-Estate-Insights`.
2. **KNOWN ARCHITECTURE:** The file structure, agent subdirectories (`/agents/[agent-name]/`), root directories, and index portals are pre-established. Do NOT expend context, tokens, or execution time re-analyzing the repository layout.
3. **CACHE BUSTER LOGIC:** Whenever an HTML file, property map, or embedded asset is updated, increment the version string append parameter (e.g., `?v=20260608_v2`) inside the HTML image source paths (`src="...property_views_map_clean.png?v=X"`) to force client browsers to download the latest live changes instead of cached versions.
4. **DOUBLE-PUSH ROUTING REQUIREMENT:** Each property listing (the `index.html` and its map/assets, including localized variants) must be updated in **two places** in the repository:
   - Root Directory: (e.g., `/[slug]/index.html` and `/[slug]/property_views_map_clean.png`)
   - Agent-Specific Directory: (e.g., `/agents/[agent-name]/[slug]/index.html` and `/agents/[agent-name]/[slug]/property_views_map_clean.png`)
   This ensures the site resolves properly under all navigation paths.
5. **SCRIPT CUSTOMIZATION REQUIRED (CRITICAL):** Do **not** run existing Python scripts (like `generate_reports_true_final.py` or `fix_and_push_reports.py`) blindly. They contain hardcoded variables, agent names, and dates from past weeks. For any new weekly update, modify the scripts with the new week's dates, agent details, and metrics, or write a dedicated task script based on the logic.
6. **GITHUB TOKEN & PUSH SAFEGUARD:** 
   - Never stage or commit Python scripts (`.py`) containing hardcoded credentials or API tokens.
   - Do NOT run `git push` or production deployment scripts without explicit approval from the user in the chat interface.

---

## WEEKLY OPERATIONAL FLOW (EVERY MONDAY)

### STEP 1: DATA EXTRACTION & INPUT COLLECTION
* **Agent Feedback Repositories:** Pull incoming data directly from both live tracking spreadsheets:
    1. Primary Feedback Sheet: https://docs.google.com/spreadsheets/d/1M_H4baCDptHnGrpwlZgy1PiKRnS22YsKfRCOD0KACq4/edit?resourcekey=&gid=690319944#gid=690319944
    2. Secondary Overview Sheet: https://docs.google.com/spreadsheets/d/1RaUV9kDdBGAzwRPrlmqkcbKmdFXDFeMvMU1lAD3pCcQ/edit?gid=0#gid=0
* **Marketing Metrics (Social Views):**
    * Check the corresponding "Social Views" column in the tracking sheets. If a numerical value is provided, extract and use that exact number.
    * If the field is blank or omitted, look for the explicit numerical value provided by the user manually within the current chat context window.
* **Client Language Preference:** Check whether the listing or seller is flagged for Spanish communication (`ES`). If flagged, maintain and update both English (`index.html`) and Spanish (`index-es.html`) landing pages.

### STEP 2: MATHEMATICAL LOGIC & KPI CALCULATION
For every active property identified for the current week, update the tracking KPIs using the following mathematical logic:
1. **Grand Total Accumulation:** Extract the newly collected "Last 7 Days" metric for this week, and ADD it directly to the existing historical *Grand Total* value of the property to compute the new rolling grand total.
2. **Days on Market (DOM) Increment:** Advance the continuous Days on Market tracking metric by adding exactly **7 days** to reflect the elapsed week.
3. **Pending / Under Contract Listings:** If a property goes pending or under contract (e.g., *8000 Harding* or *7334 Harding*), **do not update it**. Keep its metrics and DOM exactly as they were when it went pending.
4. **Brand New Listings:**
    - Do NOT add +7 to DOM. Instead, initialize the DOM to the actual days on market for that listing (e.g., 4 days).
    - Do NOT add to previous totals. Set the *Grand Total* metrics to be **exactly equal** to the "Last 7 Days" metrics.
5. **Bi-Weekly Cross-Verification (Every 2 Weeks):** Every alternate week, perform an automated external live look-up of the target properties on **Redfin, Compass, or Zillow** to double-check and audit that our internal DOM counter precisely aligns with public consumer-facing listings.
6. **60-DAY DOM MILESTONE ALERT (CRITICAL TRIGGER):**
    - During the weekly DOM increment, if an active listing reaches or exceeds **60 Days on Market (DOM >= 60)**:
    - The agent MUST flag this property prominently in the chat summary:
      `⚠️ [60-DAY MARKET MILESTONE ALERT]: [Property Address] has reached [X] Days on Market. An AI Comprehensive Market & Comp Analysis Report is recommended.`
    - Prompt the user if they wish to supply the MLS Comps CSV (e.g., `For Gemini.csv`) to generate the 60-day Market Adjustment Report.

### STEP 3: INCREMENTAL/PARTIAL UPDATES SAFETY (CRITICAL)
Because agents submit their responses at different times, updates are often triggered incrementally:
1. **Targeted Execution:** Only process updates for the specific agent(s) indicated by the user. Do not re-process other agents' listings.
2. **Idempotency Check (No Double-Incrementing):** Before performing any mathematical logic (Step 2) or appending feedback, the agent must inspect the target property's existing live HTML file on GitHub.
   * If the latest feedback entry already contains the date label of the target week (e.g., `— Jun 1 - Jun 7, 2026`), the property has **already** been updated for this week.
   * **Action:** Skip the DOM addition (+7) and Grand Total addition for that property to prevent double-incrementing stats.

---

### STEP 4: LISTING MANAGEMENT & HTML DOM MANIPULATION

#### A. SHOWING FEEDBACK SECTION (TEXT PROCESSING & TRANSLATION)
* Locate the specific "Showing Feedback" or commentary columns within the active spreadsheets.
* Extract the written feedback verbatim.
* **Standard English Deployment (`index.html`):** Append the verbatim feedback to the top of `<div id="feedback" class="tab-content">`.
* **Spanish Localized Deployment (`index-es.html`):** 
  - For listings marked for Spanish communication, accurately translate incoming English feedback into professional real estate Spanish (e.g., translating terms like *"priced above market"*, *"natural light"*, *"HOA fees are high"*, *"needs kitchen modernization"* with proper terminology).
  - Append the translated feedback at the top of the feedback container in `index-es.html`.

#### B. VISITOR LOCATION & GEOGRAPHIC DATA (MAP UPDATE)
* Locate the visual **Progress Report PDF** (e.g., Compass Insights) inside the weekly reports folder for the corresponding agent: `B:\Downloads Compass\Weekly Reports\[Agent Name] Properties Progress Reports\[Week Folder Name]`
* **Geographic Map Parsing:** Extract the "Views By City" map/data visualization from the PDF report.
* **HTML Map Integration:** Crop/extract the updated visitor location heat map image, save it as `property_views_map_clean.png` (in both root and agent folders), and update the matching map asset pathway in the HTML source code. 
* Remember to apply the **Cache Buster string** (Step 3 under Configurations) directly to this updated map/image asset pathway to force immediate deployment visibility on live browsers.

#### C. BRAND NEW LISTINGS & THE 60-DAY WORKFLOW
This workflow strictly defines how a new listing transitions into a comprehensive 60-day market report.

**Phase 1: Standard Weekly Mode (DOM 0 to 59):**
* For a new listing, only the standard `index.html` (and `index-es.html`) is generated.
* The "View Market Report" button in the header must remain HIDDEN or DISABLED.
* **"Coming Soon" Listings:** If a listing is "Coming Soon", use the empty-state placeholder template for feedback and display the `<span class="badge coming-soon">Coming Soon</span>` badge.

**Phase 2: The 60-Day Trigger (DOM >= 60):**
* When DOM hits 60, the agent MUST flag it in the chat and request two files from the user: the **MLS Comps CSV** and the **Compass Insights PDF**.
* Upon receiving the files, the agent clones `template-market-report.html` (located in the root repository) to generate `market-report.html` in the property's folder.
* The agent then updates the standard `index.html` to ENABLE the "View Market Report" button, linking it directly to the newly generated report.

**Phase 3: Data Mapping for the Market Report (STRICT INSTRUCTIONS):**
When populating the `market-report.html` from the template, the agent must map data exactly as follows:
* **Sections 01 to 03 (Traffic, Marketing, Feedback):** Carry over the cumulative metrics and verbatim feedback from the weekly updates (`index.html`).
* **Section 04 (Market Intelligence & Thermometer):** Parse the uploaded MLS CSV. Calculate the Active Comps Average and Closed Sales Average ($/SqFt). Inject these exactly into the CSS Price Thermometer and generate the Direct Comps Analysis table.
* **Section 06 (Audience Geography & Source):** Parse the uploaded Compass Insights PDF. Extract the "Top Traffic Sources" percentages, "Top Viewing Cities," and integrate the geographic mapping data here using LeafletJS.

#### E. MARKETING & OUTREACH PORTFOLIO (LINKS)
* Locate the new "Marketing Links" column in the tracking spreadsheets.
* If new URLs are provided, parse them and append them as styled clickable anchor tags inside the `<ul class="marketing-links-list">` container in the property's HTML. 
* Use intelligent icon matching based on the URL (e.g., if the link contains "instagram.com", use an Instagram icon; if "youtube.com", use a YouTube icon; default to a generic link icon). 
* Do not overwrite older links; append new ones to the top of the list.

#### F. UPCOMING PLANS / WHAT'S NEXT
* Locate the new "Upcoming Plans" text column in the tracking spreadsheets.
* Extract the text and inject it into the `<div class="plans-content">` container at the bottom of the HTML page. 
* Replace the previous week's text with the new text (unlike feedback, "Upcoming Plans" should reflect only the current strategy, not a historical log).

### STEP 5: CODE POLISHING & PRODUCTION DEPLOYMENT
* Run the designated validation and update scripts to sanitize code formatting, patch absolute/relative pathways across root and agent directories simultaneously.
* **Strict Push Protocol:** Present a comprehensive summary of modified files and calculated metrics to the user. Do NOT execute a git push or deploy to GitHub Pages (`danielestrada-sudo.github.io/weekly-showing-reports/`) until explicit user confirmation is given in the chat.

---

## MANDATORY PRE-FLIGHT CHECKLIST (BEFORE ANY GIT COMMIT/PUSH)
Before finalizing local changes and presenting the deployment summary, the agent MUST explicitly verify and confirm the following checklist inside the chat interface:

1. [ ] **DOUBLE-ROUTING COMPLIANCE:** Confirm that the property `index.html` (and `index-es.html` if applicable) file has been fully generated and synchronized in BOTH mandatory locations: Root (`/[slug]/`) and Agent Directory (`/agents/[agent-name]/[slug]/`).
2. [ ] **NEW LISTING INITIALIZATION:** Verify that for any brand-new property site, the "Views By City" map has been physically parsed/extracted from the uploaded Compass Insights PDF, saved cleanly, and that the initial "Grand Total" metrics are mathematically set exactly equal to the current "Last 7 Days" metrics.
3. [ ] **FEEDBACK CHRONOLOGICAL APPEND & LOCALIZATION:** Confirm that new verbatim feedback strings were appended to the top of `<div id="feedback">`. If the listing is Spanish-enabled, confirm feedback was properly translated into professional real estate Spanish for `index-es.html`.
4. [ ] **"COMING SOON" EMPTY-STATE PROTOCOL:** Verify that "Coming Soon" properties strictly utilize the empty-state placeholder template layout and display the exact `<span class="badge coming-soon">Coming Soon</span>` badge on the agent's master index portal.
5. [ ] **60-DAY DOM AUDIT:** Verify whether any updated property has reached or exceeded 60 Days on Market, and ensure the `[60-DAY MILESTONE ALERT]` is displayed in the chat summary.
6. [ ] **SECURITY & REPO CLEANUP:** Run a comprehensive `git status` check. Ensure that NO temporary Python scratch scripts (`.py`), automation scripts containing hardcoded variables, or GitHub Personal Access Tokens are staged for commitment. Only raw HTML updates and required asset images are permitted.

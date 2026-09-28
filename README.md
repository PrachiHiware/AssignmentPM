# TalentFlow Q3 Roadmap & Forensic Data Audit (Acme Corp)

This repository contains the complete analytical deliverables, statistical models, engineering roadmap, metric specification, and forensic data audit for the TalentFlow ATS platform evaluation at Acme Corp.

---

## Repository Structure

```text
├── README.md                              # This setup and execution guide
├── requirements.txt                       # Pinned Python dependencies for exact reproducibility
├── findings.csv                           # Structured findings register (claim, metric, value, method, confidence)
├── PROCESS.md                             # Prompt log, timeline, and AI collaboration analysis
├── CANDIDATE_PACK_PM.md.docx              # Original assignment brief
├── submission.md.docx                     # Submission template and rubric
│
├── code/                                  # All executable code and Jupyter notebooks
│   ├── TalentFlow_Roadmap_Analysis_D1.ipynb    # Pre-rendered notebook for Claim 1 & Claim 2 analysis
│   ├── TalentFlow_Data_Integrity_Audit_D4.ipynb # Pre-rendered notebook for D4 5-dimension data audit
│   └── fetch_data.py                           # Dynamic data ingestion script from Airtable API
│
├── data/                                  # Pre-cached JSON snapshots (Zero API key needed to run)
│   ├── Applications.json                  # 350 application records
│   ├── Candidates.json                    # 300 candidate profiles
│   ├── Interviews.json                    # 160 interview records
│   ├── Offers.json                        # 36 offer records
│   ├── Job_Openings.json                  # 24 job requisitions
│   ├── Departments.json                   # 6 department records
│   ├── People.json                        # 12 internal team member records
│   ├── Findings.json                      # Reference findings
│   └── summary.json                       # Ingestion metadata summary
│
├── D2_TalentFlow_Q3_Roadmap.docx          # Deliverable D2: 6-Week Engineering Roadmap (3 to build, 3 not to build)
├── METRIC_SPEC_OAR.docx                   # Deliverable D3: Offer Acceptance Rate Metric Spec (Word)
├── METRIC_SPEC_OAR.md                     # Deliverable D3: Offer Acceptance Rate Metric Spec (Markdown)
├── D4_DATA_INTEGRITY_AUDIT.docx           # Deliverable D4: Forensic Data Integrity Audit Report (Word)
├── D4_DATA_INTEGRITY_AUDIT.md             # Deliverable D4: Forensic Data Integrity Audit Report (Markdown)
├── D5_EXECUTIVE_MEMO.docx                 # Deliverable D5: One-Page Executive Briefing (Word)
├── D5_EXECUTIVE_MEMO.md                   # Deliverable D5: One-Page Executive Briefing (Markdown)
├── CHAT_TRANSCRIPT.md                     # Complete formatted chat session transcript
└── session_transcript.jsonl               # Complete machine-readable session event log
```

---

## Quickstart & Environment Setup

### 1. Clone / Download
Extract or clone this repository to your local machine and navigate into the root directory:
```bash
cd asg1
```

### 2. Create Virtual Environment
```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (Command Prompt)
python -m venv .venv
.venv\Scripts\activate.bat

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Running the Code & Notebooks

> [!NOTE]
> **No API Key Required to Run:** All Airtable tables are pre-cached in `data/`. The notebooks and analyses run 100% offline out-of-the-box.

### Option A: Launch Jupyter Notebooks Interactively
Both notebooks are built with **adaptive path resolution**—they run smoothly whether launched from the repository root or from within the `code/` folder:

```bash
# Launch Jupyter Lab or Notebook
jupyter lab
# or
jupyter notebook
```
In Jupyter or VS Code, open either:
- `code/TalentFlow_Roadmap_Analysis_D1.ipynb`: Computes channel conversion rates, hire shares, statistical hypothesis tests (two-sided binomial $p=1.000$), offer acceptance resolution (83.9% true OAR vs 72.2% claimed), and visual charts.
- `code/TalentFlow_Data_Integrity_Audit_D4.ipynb`: Runs automated duplication scans, attribution conflict checks, temporal inversion tests, salary band validations, and prints the 88 corrupted database records.

Both notebooks are also **pre-rendered** with all charts and tables pre-computed, so they can be viewed immediately on GitHub or in any viewer without re-execution.

### Option B: Automated Headless Re-Execution
To re-run and verify all notebook cells from the command line:

```bash
# Run D1 analysis notebook
jupyter nbconvert --to notebook --execute code/TalentFlow_Roadmap_Analysis_D1.ipynb --output TalentFlow_Roadmap_Analysis_D1.ipynb

# Run D4 audit notebook
jupyter nbconvert --to notebook --execute code/TalentFlow_Data_Integrity_Audit_D4.ipynb --output TalentFlow_Data_Integrity_Audit_D4.ipynb
```

### Option C: Re-Fetching Data from Airtable (Optional)
If you wish to re-download the live dataset from Airtable:
1. Create a `.env` file in the root directory:
   ```env
   AIRTABLE_TOKEN=pat_your_airtable_token_here
   AIRTABLE_BASE_ID=appYePRAI75PMbQNQ
   ```
2. Run the fetcher:
   ```bash
   python code/fetch_data.py
   ```
The script will query all 8 Airtable tables, adhere to Airtable's 5 req/sec rate limit with backoff retries, and refresh `data/*.json`.

---

## Core Deliverables Summary

| Deliverable | File(s) | Description |
| :--- | :--- | :--- |
| **D1: Verdict on Claims** | `code/TalentFlow_Roadmap_Analysis_D1.ipynb` | Refutes Claim 1 (Job Boards tied with Referrals at 7 hires, $p=1.000$) & Claim 2 (True OAR is 83.9%, not 72.2%). |
| **D2: 6-Week Roadmap** | `D2_TalentFlow_Q3_Roadmap.docx` | 3 things to build (Inbound Triage 2.5w, Referral Portal 2.0w, Pipeline Hygiene 1.5w = 6.0w) and 3 things not to build. |
| **D3: Metric Specification** | `METRIC_SPEC_OAR.docx` / `.md` | Full spec for Offer Acceptance Rate (OAR), covering formulas, 5 edge cases, cohorting, ambiguity intervals, and SQL code. |
| **D4: Data Integrity Audit** | `D4_DATA_INTEGRITY_AUDIT.docx` / `.md` <br> `code/TalentFlow_Data_Integrity_Audit_D4.ipynb` | Comprehensive audit identifying 88 corrupted records (10.1% of base), entity resolution, and attribution leaks. |
| **D5: Executive Memo** | `D5_EXECUTIVE_MEMO.docx` / `.md` | One-page briefing for CEO & VP of People: What we found, what we are doing, what we look at next. |
| **Findings Register** | `findings.csv` | Standardized CSV table of all verified claims and audit metrics. |
| **Process Log** | `PROCESS.md` | Chronological prompt audit trail (+0.00m to +89.38m) and AI collaboration retrospective. |

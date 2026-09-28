# Engineering Metric Specification: Offer Acceptance Rate (OAR)

**Document Version:** 1.0  
**Status:** Approved for Implementation  
**Target Systems:** TalentFlow Core Platform, Analytics Engine, Recruiter Dashboard  
**Author:** Product Management Team  
**Audience:** Full-Stack Engineers, Data Engineers, QA, Product Managers  

---

## 1. Executive Summary & Objective

### 1.1 Metric Name
**Offer Acceptance Rate (OAR)**

### 1.2 Business Objective
Measure the efficiency of the bottom-of-funnel candidate experience and the market competitiveness of company compensation packages. The goal is to provide leadership and recruiters with an unpolluted, actionable signal on closing efficiency, allowing teams to diagnose commercial compensation gaps versus process friction without metric distortion.

### 1.3 Problem Statement (Context from Acme Production Audit)
In Q2, Acme's leadership reported an offer acceptance rate of **~72%**, causing executive alarm. Our audit revealed that this was an **artifact of denominator contamination**:
* Total Offers: 36
* Accepted: 26 (72.2%)
* Declined: 5 (13.9%)
* Pending (in-flight / undecided): 5 (13.9%)

The legacy reporting engine divided `Accepted / Total Offers` ($26 / 36 = 72.22\%$), mathematically treating all 5 undecided candidates as rejections. The true resolved acceptance rate was **83.87%** ($26 / 31$), meeting healthy industry benchmarks. Furthermore, 3 of the 5 pending offers were "zombie" records lingering months past their start dates without automated closure. 

This specification establishes an unambiguous, engineering-grade implementation to eliminate ambiguity across all TalentFlow tenant instances.

---

## 2. Mathematical Definition

TalentFlow defines two standard views of OAR: **Resolved OAR (Primary KPI)** and **Cohort OAR (Funnel Cohort)**.

### 2.1 Primary Metric: Resolved Offer Acceptance Rate ($\text{OAR}_{\text{resolved}}$)
Used for operational leadership reporting, quarterly board reviews, and department scorecards. It evaluates only finalized, decided candidate offers.

$$\text{OAR}_{\text{resolved}} = \frac{N_{\text{Accepted}}}{N_{\text{Accepted}} + N_{\text{Declined}} + N_{\text{Lapsed}}} \times 100$$

Where:
* $N_{\text{Accepted}}$: Total number of offers accepted within the evaluation window.
* $N_{\text{Declined}}$: Total number of offers explicitly declined by the candidate within the evaluation window.
* $N_{\text{Lapsed}}$: Total number of offers where the validity window expired without candidate response (auto-classified as declined).

### 2.2 Secondary Diagnostic Metric: Funnel Cohort Acceptance Rate ($\text{OAR}_{\text{cohort}}$)
Used for recruiting ops pipeline tracking, evaluating all offers extended in a specific timeframe.

$$\text{OAR}_{\text{cohort}} = \frac{N_{\text{Accepted}}}{N_{\text{Total Extended}}} \times 100$$
$$\text{Pending Rate} = \frac{N_{\text{Pending}}}{N_{\text{Total Extended}}} \times 100$$

$$\text{OAR}_{\text{cohort}} + \text{Declined Rate} + \text{Pending Rate} = 100\%$$

---

## 3. Data Dictionary & Field Mapping

| Parameter | Database Field / Source | Allowed Values | Nullable | Description |
| :--- | :--- | :--- | :---: | :--- |
| **Offer ID** | `Offers.Offer_ID` | String (`OFF-XXXXX`) | No | Unique primary key for the offer record. |
| **Application ID**| `Offers.Application` | Foreign Key (`Applications.id`) | No | Link to the candidate's specific job application. |
| **Offer Status** | `Offers.Status` | `Accepted`, `Declined`, `Pending`, `Rescinded`, `Lapsed` | No | Current lifecycle status of the offer. |
| **Offered On** | `Offers.Offered_On` | ISO 8601 Date (`YYYY-MM-DD`) | No | Date the official written offer was transmitted to the candidate. |
| **Decision On** | `Offers.Decision_On` | ISO 8601 Date (`YYYY-MM-DD`) | Yes | Date candidate communicated their acceptance or decline. |
| **Start Date** | `Offers.Proposed_Start_Date` | ISO 8601 Date (`YYYY-MM-DD`) | Yes | Anticipated employment start date. |
| **Decline Reason** | `Offers.Decline_Reason` | Enum | Yes | Required if `Status IN ('Declined', 'Lapsed')`. |
| **Base CTC** | `Offers.Base_CTC` | Numeric (Currency) | No | Annual base compensation offered. |
| **Current CTC** | `Candidates.Current_CTC` | Numeric (Currency) | Yes | Candidate's verified current compensation. |

---

## 4. Numerator & Denominator Specifications

### 4.1 Numerator ($N_{\text{Accepted}}$)
A candidate offer record is included in the numerator IF AND ONLY IF:
1. `Offers.Status == 'Accepted'`
2. The qualifying date falls within the selected evaluation time window:
   * **In Event-Date Mode (Default):** `Offers.Decision_On` $\in [\text{Window Start}, \text{Window End}]$.
   * **In Cohort Mode:** `Offers.Offered_On` $\in [\text{Window Start}, \text{Window End}]$.
3. The offer is the **terminal offer** for that `Application ID` (see Section 5.3 for renegotiations).

### 4.2 Denominator ($D_{\text{Resolved}}$)
A candidate offer record is included in the resolved denominator IF AND ONLY IF:
1. `Offers.Status IN ('Accepted', 'Declined', 'Lapsed')`
2. Qualifying date falls within the selected evaluation window.
3. The offer is the **terminal offer** for that `Application ID`.

### 4.3 Explicit Exclusions from the Denominator
The following records **MUST NEVER** be included in the primary resolved denominator:
* `Offers.Status == 'Pending'` (Active, in-flight offers whose validity window has not elapsed).
* `Offers.Status == 'Rescinded'` where `Rescinded_By == 'Company'` (e.g. hiring freeze, role cancellation, or failed background check / reference check).
* Intermediate superseded offers from renegotiations (e.g. revision 1 of an offer).

---

## 5. Edge Cases & Precise Engineering Rules

### Rule 1: Handling In-Flight (Pending) Offers
* **Rule:** If an offer has `Status == 'Pending'` and `Today <= Offered_On + 14 days` and `Today <= Proposed_Start_Date`:
  * It is **omitted** from $D_{\text{Resolved}}$.
  * It is **included** in $N_{\text{Pending}}$ for the diagnostic cohort view.
  * It contributes to the dashboard **Ambiguity Band**.

### Rule 2: Automated Expiry of "Zombie" / Stale Offers
* **Problem in Acme Data:** OFF-00002 was offered in Jan 2026 for an April 2026 start date, but was still marked `Pending` in August 2026.
* **Rule:** If `Status == 'Pending'` AND (`Today > Offered_On + 14 calendar days` OR `Today > Proposed_Start_Date`):
  * The system background daemon must auto-transition `Status` to `'Lapsed'`.
  * `Decision_On` is set to `Offered_On + 14 days`.
  * `Decline_Reason` is set to `'Offer Expired / No Response'`.
  * **Metric Impact:** Lapsed offers enter the denominator as a non-acceptance. Recruiters cannot game OAR by leaving unaccepted offers open forever.

### Rule 3: Multiple Revised Offers (Renegotiations / Counter-Offers)
* **Problem:** Candidate is offered \$100k, counter-offers, and receives a revised offer of \$110k which they accept.
* **Rule:** Deduplication by `Application ID`.
  * When an offer is revised, the prior offer record is marked `Status = 'Superseded'`.
  * `Superseded` offers are excluded from both numerator and denominator.
  * Only the final terminal offer outcome (`Accepted` or `Declined`) enters the calculation. One application equals at most one denominator count.

### Rule 4: Company-Rescinded Offers vs. Candidate Back-Outs
* **Company Rescission:** If Acme cancels the position or rescinds due to failed background verification:
  * `Status = 'Rescinded'`
  * `Exclusion_Flag = TRUE` (Excluded from both Numerator and Denominator).
* **Candidate Reneging (Post-Acceptance):** If candidate signs the offer but reneges before Day 1:
  * `Status` remains `'Accepted'` in the OAR calculation (because the offer was successfully accepted).
  * A separate flag `Reneged = TRUE` is populated with `Reneged_On` date.
  * OAR is NOT penalized post-hoc; candidate reneging is tracked via a dedicated operational metric: **Post-Acceptance Fall-Through Rate**.

### Rule 5: State Synchronization with Applications Table
* **Problem in Acme Data:** 5 declined offers had application status `Closed`, but application stage remained stuck in `Offer`.
* **Rule:** Bidirectional state machine:
  * When `Offers.Status -> 'Accepted'`: Automatically transition `Applications.Stage -> 'Hired'`, `Applications.Status -> 'Closed'`, and set `Applications.Closed_On = Offers.Decision_On`.
  * When `Offers.Status -> 'Declined'`: Automatically transition `Applications.Stage -> 'Rejected'`, `Applications.Status -> 'Closed'`, `Applications.Rejection_Reason = Offers.Decline_Reason`, and `Applications.Closed_On = Offers.Decision_On`.
  * When `Offers.Status -> 'Lapsed'`: Automatically transition `Applications.Stage -> 'Rejected'`, `Applications.Status -> 'Closed'`, and `Applications.Rejection_Reason = 'Offer Expired'`.

---

## 6. Time Window & Cohorting Modes

### 6.1 Mode A: Decision-Date Window (Default — Operational Mode)
* **Anchor Field:** `Offers.Decision_On`
* **Definition:** Filters offers where `Decision_On >= Start_Date AND Decision_On <= End_Date`.
* **Properties:** Closed cohort with **0% ambiguity**. Recommended for weekly/monthly business reviews.

### 6.2 Mode B: Offer-Date Window (Pipeline Cohort Mode)
* **Anchor Field:** `Offers.Offered_On`
* **Definition:** Filters offers where `Offered_On >= Start_Date AND Offered_On <= End_Date`.
* **Properties:** Open cohort. May contain active `Pending` offers if the window includes recent dates.

---

## 7. Dashboard Ambiguity UI Specification

```
+-------------------------------------------------------------------------+
| OFFER ACCEPTANCE RATE (OAR) - Q2 2026                      [Trailing 90D] |
|                                                                         |
|   PRIMARY RESOLVED OAR:   83.9%  (+11.7% vs unadjusted)                 |
|   RESOLVED BASE:          26 Accepted / 31 Decided                      |
|                                                                         |
|   [====================== 83.9% =====================]                  |
|                                                                         |
|   PROJECTED SENSITIVITY RANGE:  72.2%  <--->  86.1%                     |
|   (Worst Case: All 5 Decline)                 (Best Case: All 5 Accept) |
+-------------------------------------------------------------------------+
| [!] PIPELINE AMBIGUITY NOTICE: 5 Offers Currently Pending (13.9% Volume)|
|     * 2 Active In-Flight (<14 Days): Decisive window open               |
|     * 3 STALE / ZOMBIE OFFERS: Action Required (Overdue >30 Days)       |
|       - OFF-00002 (Aarav Menon): Offered Jan 17, 2026 [AUTO-EXPIRE]     |
|       - OFF-00021 (Manish Singh): Offered May 02, 2026 [AUTO-EXPIRE]    |
|       - OFF-00013 (Jatin Sharma): Offered Jun 19, 2026 [RESOLVE STATUS] |
+-------------------------------------------------------------------------+
```

### 7.1 Primary Value
* Display `Resolved OAR` as the large hero metric: e.g. **`83.9%`**.
* Display the denominator breakdown directly underneath: `26 Accepted / 31 Decided`.

### 7.2 The Sensitivity Range (Ambiguity Bounds)
$$\text{Worst-Case OAR} = \frac{N_{\text{Accepted}}}{N_{\text{Accepted}} + N_{\text{Declined}} + N_{\text{Pending}}} \times 100$$
$$\text{Best-Case OAR} = \frac{N_{\text{Accepted}} + N_{\text{Pending}}}{N_{\text{Accepted}} + N_{\text{Declined}} + N_{\text{Pending}}} \times 100$$

* For Acme: **Worst Case = 72.22%**, **Best Case = 86.11%**.

### 7.3 Overdue & Stale Warning Card
If any offer in the view has `Today > Offered_On + 14 days` while remaining `Pending`:
* Render an amber warning banner: **`N Stale Offers Awaiting Resolution`**.

---

## 8. Reference Implementation (SQL & Python)

### 8.1 Production SQL Implementation
```sql
WITH terminal_offers AS (
    SELECT 
        o.offer_id,
        o.application_id,
        o.status,
        o.offered_on,
        o.decision_on,
        o.proposed_start_date,
        o.decline_reason,
        o.base_ctc,
        CASE 
            WHEN o.status = 'Pending' AND (CURRENT_DATE > o.offered_on + INTERVAL '14 day' OR CURRENT_DATE > o.proposed_start_date)
            THEN 'Lapsed'
            ELSE o.status 
        END AS effective_status,
        ROW_NUMBER() OVER (PARTITION BY o.application_id ORDER BY o.offered_on DESC) AS rn
    FROM offers o
    WHERE o.status != 'Superseded'
)
SELECT 
    COUNT(CASE WHEN effective_status = 'Accepted' THEN 1 END) AS count_accepted,
    COUNT(CASE WHEN effective_status = 'Declined' THEN 1 END) AS count_declined,
    COUNT(CASE WHEN effective_status = 'Lapsed' THEN 1 END) AS count_lapsed,
    COUNT(CASE WHEN effective_status = 'Pending' THEN 1 END) AS count_pending,
    COUNT(CASE WHEN effective_status IN ('Accepted', 'Declined', 'Lapsed') THEN 1 END) AS resolved_denominator,
    ROUND(
        COUNT(CASE WHEN effective_status = 'Accepted' THEN 1 END) * 100.0 / 
        NULLIF(COUNT(CASE WHEN effective_status IN ('Accepted', 'Declined', 'Lapsed') THEN 1 END), 0),
        2
    ) AS resolved_oar_pct,
    ROUND(
        COUNT(CASE WHEN effective_status = 'Accepted' THEN 1 END) * 100.0 / 
        NULLIF(COUNT(*), 0),
        2
    ) AS worst_case_lower_bound_pct,
    ROUND(
        (COUNT(CASE WHEN effective_status = 'Accepted' THEN 1 END) + COUNT(CASE WHEN effective_status = 'Pending' THEN 1 END)) * 100.0 / 
        NULLIF(COUNT(*), 0),
        2
    ) AS best_case_upper_bound_pct
FROM terminal_offers
WHERE rn = 1;
```


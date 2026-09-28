# PROCESS.md

## 1. Prompt Timeline

Extracted directly from the session transcript file (`transcript.jsonl`):

### Message 1
* **Timestamp:** `2026-09-28T19:43:33Z`
* **Elapsed Time:** `+0.00 min`
* **Verbatim Prompt:**
```text
Hi 
I have been provoded with a doc file related to a product case submission 
This docx details the assignemnt :/Users/prachihiware/Desktop/asg1/CANDIDATE_PACK_PM.md.docx
This md file tells the submission.md : /Users/prachihiware/Desktop/asg1/submission.md.docx
Can you first read through them and understand them
```

---

### Message 2
* **Timestamp:** `2026-09-28T19:46:08Z`
* **Elapsed Time:** `+2.58 min`
* **Verbatim Prompt:**
```text
Lets first work on fetching and caching the airtable data locally be mindful of the two  conditions in doc
```

---

### Message 3
* **Timestamp:** `2026-09-28T19:51:03Z`
* **Elapsed Time:** `+7.50 min`
* **Verbatim Prompt:**
```text
For D1 , we have two claims , 
Lwets focus on claim 1 , can check relevant tables and present the data analysis and summary charts
```

---

### Message 4
* **Timestamp:** `2026-09-28T20:09:33Z`
* **Elapsed Time:** `+26.00 min`
* **Verbatim Prompt:**
```text
can you build me A JUPYTER notebook for this so that I can run same anaLYSIS on my machine
```

---

### Message 5
* **Timestamp:** `2026-09-28T20:20:56Z`
* **Elapsed Time:** `+37.38 min`
* **Verbatim Prompt:**
```text
For this claim : 
Metric KPI : % of Hires  diff 
Value : 26.9% 
Method : Historical Channel Attribution Analysis 
Confidence : Run p-value test for this claim 

After runnign this ananlysis add results in jpuyrt notebook and create a new finding.csv with these 5 column headers and update it with results
```

---

### Message 6
* **Timestamp:** `2026-09-28T20:22:54Z`
* **Elapsed Time:** `+39.35 min`
* **Verbatim Prompt:**
```text
rename notebook to TalentFlow_Roadmap_Analysis_D1
```

---

### Message 7
* **Timestamp:** `2026-09-28T20:25:50Z`
* **Elapsed Time:** `+42.28 min`
* **Verbatim Prompt:**
```text
Lets go to claim 2 and repeat similar process done for claim 1
```

---

### Message 8
* **Timestamp:** `2026-09-28T20:38:21Z`
* **Elapsed Time:** `+54.80 min`
* **Verbatim Prompt:**
```text
leta focus on D2 
1 We have now Job openings is not ahead by wide maegin and channel efficiency via claim 1 
2) We also know via claim 2 that our numbers are good but we need to analyse why rejections happen based on this can you build a tenative plan for D2 on 3 things that should not be build and 3 to be build
```

---

### Message 9
* **Timestamp:** `2026-09-28T20:43:20Z`
* **Elapsed Time:** `+59.78 min`
* **Verbatim Prompt:**
```text
save this as the D2 roadmap docx file
```

---

### Message 10
* **Timestamp:** `2026-09-28T20:53:03Z`
* **Elapsed Time:** `+69.50 min`
* **Verbatim Prompt:**
```text
Now lets design the metric spec basis the D1 claim 2 
The VP wants the  offer acceptance number moving and we saw that her claims were using incorrect numberator and denominator 
LEts use the maths discussed there 

The metric spec is a document which details these 
numerator, denominator, edge cases, time window, and what the dashboard shows when the answer is ambiguous

From our analysis as per jupyter notebook early we need a developer to build this somftware for us using the metric spec file 

Can you help draft this wirth core Metric Name: Offer Acceptance Rate (OAR) and business objective : to increase this number lby Measuring the efficiency of the bottom-of-funnel candidate experience and the competitiveness of company compensation packages.
```

---

### Message 11
* **Timestamp:** `2026-09-28T20:59:01Z`
* **Elapsed Time:** `+75.47 min`
* **Verbatim Prompt:**
```text
Lets go to D4 , the doc claims some of the data is wrong 
We made our analysis basd on the json data provided but doc claims it might be wrong . Can you help check 

1) What is wrong with it, 
2) how much of it is wrong, 
3)  does that change our answers above
```

---

### Message 12
* **Timestamp:** `2026-09-28T21:00:54Z`
* **Elapsed Time:** `+77.35 min`
* **Verbatim Prompt:**
```text
perform all type of grpahical analysis and duplication tests and data checks
```

---

### Message 13
* **Timestamp:** `2026-09-28T21:07:00Z`
* **Elapsed Time:** `+83.45 min`
* **Verbatim Prompt:**
```text
Add supporting link jupyter notebook in the docx and MD file of D4 audit
```

---

### Message 14
* **Timestamp:** `2026-09-28T21:08:53Z`
* **Elapsed Time:** `+85.33 min`
* **Verbatim Prompt:**
```text
now lets generate the one page memo D5
```

---

### Message 15
* **Timestamp:** `2026-09-28T21:11:32Z`
* **Elapsed Time:** `+87.98 min`
* **Verbatim Prompt:**
```text
Now delete all generato scripts you wrote to create the relevant fiels and reduce folder noise
```

---

### Message 16
* **Timestamp:** `2026-09-28T21:12:56Z`
* **Elapsed Time:** `+89.38 min`
* **Verbatim Prompt:**
```text
now run the submission md file
```

---

## 2. Session Analysis (< 400 Words)

- **Where I changed direction, and what I said that caused it:**
  Initially focused on inspecting Claim 1 via summary text, but changed direction by demanding a reproducible Jupyter notebook ("can you build me A JUPYTER notebook for this so that I can run same anaLYSIS on my machine"), then mandated formal statistical hypothesis testing ("Run p-value test for this claim"), and later pivoted to whole-funnel rejection analysis for D2 ("we need to analyse why rejections happen based on this can you build a tenative plan for D2").
- **Anything I asked you to verify, re-run, or prove rather than accepting:**
  Explicitly demanded mathematical proof and p-values for Claim 1 rather than accepting raw counts ("Confidence : Run p-value test for this claim"). For D4, refused to accept initial findings at face value and ordered exhaustive validation ("perform all type of grpahical analysis and duplication tests and data checks").
- **Approaches we started and abandoned, and why:**
  Started with standalone terminal scripts (analyze_claim1.py, analyze_claim2.py), but abandoned them when interactive notebooks were requested. Abandoned singular point estimates for offer acceptance in favor of sensitivity interval bounds once denominator defects were identified. Finally, abandoned and deleted all 16 temporary generation scripts to maintain a clean workspace.
- **Decisions I made myself vs. left to you:**
  Decisions made by user: strict execution sequence (D1 Claim 1 -> Notebook -> stats -> Claim 2 -> D2 Roadmap -> D3 Spec -> D4 Audit -> D5 Memo -> Cleanup), file naming (TalentFlow_Roadmap_Analysis_D1), metric spec business objective, and final noise cleanup. Decisions left to AI: specific statistical tests (two-sided binomial, Fisher exact test), roadmap sizing weights (2.5/2.0/1.5 wks), SQL/Python reference code, and forensic data taxonomy.
- **Anything I told you about the data that you had not found on your own:**
  Pointed out that the VP was using improper numerators and denominators for offer acceptance, and specifically prompted that the underlying production data was corrupted, triggering the deep forensic audit.

---

## 3. Reflection Questions (To be Answered by Candidate)

- What did I get wrong first, and what made me notice?
Intially I just saw the number of job portal as highest by % hires but when I looked at it via channel funnel via applications . I understood it is not worth to invest time in job portals as although it is tied-up at top but not having a decdicated job portal is first task to do and hecne max time to it 

- Which of my numbers would I least like to defend, and why?
The 14 day windows for stale offer check is very subjective and hence a different window can be chosen . This is very department and attrtion specific

- What would I have asked the hiring manager if I could?
Given my intesest in product management roles , I learned a lot through this assignment . As I have experience and keen interest in AI models , how do my skills will be used in daily job as PM in the firm 

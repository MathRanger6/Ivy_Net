# Vector HS Data: Scraping and Matching Specification

## Objective

Provide a step-by-step execution plan for acquiring and linking recruiting data.

---

# Scraping Plan

## Target
- 247Sports recruiting rankings pages

## Fields
- name  
- rank  
- stars  
- high school  
- college  
- class year  

---

# Scraping Logic

1. Loop over years  
2. Extract player rows  
3. Store structured dataset  

---

# Matching Plan

## Keys
- name  
- high school  
- graduation year  
- college  

---

# Matching Steps

1. Exact match on name + college  
2. Fuzzy match for unmatched  
3. Manual review layer  

---

# Validation

- Match rate  
- Duplicate checks  
- Spot checks  

---

# Output

Clean merged dataset:
- player_id  
- recruiting rank  
- star rating  
- matched college stats  

---

# Risks

- Name inconsistencies  
- Missing players  
- Partial coverage  

---

# Bottom Line

Matching is the hardest step. Build auditability into the pipeline.

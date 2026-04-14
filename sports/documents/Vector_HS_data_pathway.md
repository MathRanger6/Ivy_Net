# Vector HS Data Pathway

## Overview

This document outlines the practical pathway for integrating high school recruiting data into the existing college basketball replication pipeline.

The goal is to move from:
- baseline replication  
to:
- stronger identification and cross-domain comparability  

---

# Core Data Stack

## 1. Recruiting Data (High School Talent)

Primary Source:
- https://247sports.com/

Example:
- https://247sports.com/Season/2023-Basketball/CompositeRecruitRankings/

Data:
- Player name  
- Star rating  
- National rank  
- Position rank  
- High school  
- College commitment  

---

## 2. College Performance Data

Source:
- https://www.sports-reference.com/cbb/

Data:
- Player-season stats  
- Advanced metrics (BPM, WS, PER)  
- Team rosters  

---

## 3. Professional Outcomes

Source:
- https://www.basketball-reference.com/

Data:
- Draft status  
- NBA participation  
- Career outcomes  

---

# Supporting Data Sources

- Kaggle (https://www.kaggle.com/)
- GitHub (various repositories)
- KenPom (https://kenpom.com/)
- ESPN player pages
- MaxPreps (optional)

---

# Data Integration Pipeline

## Step 1: Build Recruiting Dataset
- Scrape 247Sports by year
- Extract rankings and player info

## Step 2: Normalize Data
- Standardize names
- Clean school names

## Step 3: Match Players
- Match to Sports-Reference players
- Use:
  - name  
  - school  
  - year  

## Step 4: Validate Matches
- Manual review
- Resolve duplicates

---

# Model Integration

\[
Y_i =
\beta_1 \text{Perf}_i +
\beta_2 \text{PoolQ}_{jt}^{(-i)} +
\beta_3 (\text{PoolQ}_{jt}^{(-i)})^2 +
\gamma \text{HSRank}_i +
X_i'\delta +
\varepsilon_i
\]

---

# Analytical Value

- Controls for sorting  
- Enables heterogeneity  
- Strengthens mechanism  

---

# Bottom Line

The HS data layer transforms the project from descriptive replication to credible empirical analysis.

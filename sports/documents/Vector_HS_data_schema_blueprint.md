# Vector HS Data: Data Schema Blueprint

## Objective

Define the data structure for integrating recruiting, college, and outcome data.

---

# Core Tables

## 1. Players Table

Fields:
- player_id  
- name  
- high_school  
- graduation_year  

---

## 2. Recruiting Table

Fields:
- player_id  
- recruiting_rank  
- star_rating  
- position_rank  
- source  

---

## 3. College Performance Table

Fields:
- player_id  
- season  
- team  
- BPM  
- minutes  
- stats  

---

## 4. Team Pool Table

Fields:
- team  
- season  
- pool_quality  

---

## 5. Outcomes Table

Fields:
- player_id  
- drafted  
- nba_games  
- career_length  

---

# Relationships

- player_id links all tables  
- team-season links pool  

---

# Derived Variables

- PoolQ (leave-one-out mean)  
- HSRank  
- performance metrics  

---

# Final Analysis Dataset

Unit:
- player-season  

Includes:
- outcome  
- performance  
- pool quality  
- HS ranking  
- controls  

---

# Bottom Line

A clean relational structure ensures scalability and reproducibility.

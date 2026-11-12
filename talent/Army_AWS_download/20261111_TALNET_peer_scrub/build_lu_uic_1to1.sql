DROP TABLE IF EXISTS lkup_uic_1to1;

CREATE TABLE lkup_uic_1to1 AS

SELECT
	m.asg_uic,
	p.asg_uic_pde
FROM study_talent_net.mv_fouo_uz_master_ad_army_v3a m 
JOIN study_talent_net.mv_master_ad_army_qtr_v3a p 
ON m_pid_pde = p.pid_pde
AND m.snpsht_dt = p.snpsht_dt
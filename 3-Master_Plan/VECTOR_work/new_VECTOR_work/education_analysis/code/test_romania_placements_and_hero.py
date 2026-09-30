"""Offline scientific guardrails. No archive requests or real HERO calculation.

Run with sports_net: python -B -m unittest discover -s <this directory>
-p test_romania_placements_and_hero.py -v
"""
import base64
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

import numpy as np
import pandas as pd
import EDUCATION_20260930_romania_placements_and_hero as hero


def program(code, school, subject="Filologie", cutoff=9, places=10, admitted=10):
    return {"program_code": code, "school_name": school, "profile": "Uman",
            "specialization": subject, "level": "Profesional" if subject == "Profesional" else "Liceal",
            "places": places, "admitted": admitted, "vacancies": places-admitted,
            "filled": places == admitted, "lowest_admitted_score": cutoff}


def placement(name, school, score="8,00", subject="Filologie"):
    return {"Nume":name, "Liceu":school, "Profil":"Uman",
            "Specializare":subject, "Medie Admitere":score}


class HeroTests(unittest.TestCase):
    def setUp(self):
        self.programs = [program("1","Winner"), program("2","Other",cutoff=8),
                         program("3","Trade","Profesional",7,100,2)]

    def test_ties_and_unfilled_programs(self):
        programs = self.programs + [program("4","Tied",cutoff=9),
                                   program("5","Unfilled",cutoff=9.9,admitted=1)]
        self.assertEqual({p["program_code"] for p in hero.winning_programs(programs)}, {"1","4"})

    def test_two_distinct_tiers_include_ties_and_keep_first_tier(self):
        programs=self.programs+[program("4","Tied first",cutoff=9),
            program("5","Tied second",cutoff=8),program("6","Third",cutoff=7),
            program("7","Unfilled high",cutoff=9.9,admitted=1)]
        one={p["program_code"] for p in hero.winning_programs(programs,1)}
        two={p["program_code"] for p in hero.winning_programs(programs,2)}
        self.assertEqual(one,{"1","4"})
        self.assertEqual(two,{"1","2","4","5"})
        self.assertTrue(one.issubset(two))
        for invalid in (0,-1,1.5,True,"2"):
            with self.assertRaises(ValueError):hero.winning_programs(programs,invalid)

    def test_tier_setting_reaches_actual_placement_labels(self):
        frame=pd.DataFrame({"source_code":["1","1"],"analytic_row":[1,2]})
        candidates={"1":[{"Nume":"A","Medie Admitere":"8,00"},{"Nume":"B","Medie Admitere":"8,00"}]}
        placements={"1":[placement("A","Winner"),placement("B","Other")]}
        one=hero.attach_placements(frame,candidates,placements,self.programs,1)
        two=hero.attach_placements(frame,candidates,placements,self.programs,2)
        self.assertEqual(one.success.tolist(),[1,0])
        self.assertEqual(two.success.tolist(),[1,1])
        pd.testing.assert_frame_equal(one.drop(columns='success'),two.drop(columns='success'))

    def test_partially_filled_switch_keeps_empty_and_missing_cutoffs_out(self):
        empty=program('empty','Empty',cutoff=10,admitted=0)
        missing=program('missing','No cutoff',cutoff=None)
        programs=self.programs+[empty,missing]
        full=hero.winning_programs(programs,require_full_programs=True)
        open_rule=hero.winning_programs(programs,require_full_programs=False)
        self.assertEqual({p['program_code'] for p in full},{'1'})
        self.assertEqual({p['program_code'] for p in open_rule},{'1','3'})
        frame=pd.DataFrame({'source_code':['1'],'analytic_row':[1]})
        c={'1':[{'Nume':'A','Medie Admitere':'8,00'}]}
        p={'1':[placement('A','Trade',subject='Profesional')]}
        self.assertEqual(hero.attach_placements(frame,c,p,programs).success.iloc[0],0)
        self.assertEqual(hero.attach_placements(frame,c,p,programs,require_full_programs=False).success.iloc[0],1)

    def test_combined_groups_rerank_instead_of_merely_relabelling(self):
        programs=self.programs+[
            program('soc','Social','Stiinte Sociale',9.5),
            program('math','Math','Matematica-Informatica',9.1),
            program('sci','Science','Stiinte ale Naturii',8.9),
            program('tech','Tech','Spec.Tehnologica',8.1)]
        separate=hero.winning_programs(programs)
        combined=hero.winning_programs(programs,combine_program_categories=True)
        self.assertEqual({p['program_code'] for p in separate},{'1','soc','math','sci','tech'})
        self.assertEqual({p['program_code'] for p in combined},{'soc','math','tech'})
        self.assertEqual(len({p['ranking_group'] for p in combined}),3)
        two=hero.winning_programs(programs,2,require_full_programs=False,combine_program_categories=True)
        self.assertEqual({p['program_code'] for p in two},{'soc','1','math','sci','tech','3'})

    def test_vocational_exclusion_accounts_for_newly_eligible_successes(self):
        frame=hero.add_peer_axis(pd.DataFrame({
            'source_code':['1','1','2','2'],'analytic_row':[1,2,1,2],
            'A_z':[-1.,0.,1.,2.], 'success':[1.,0.,1.,0.],
            'vocational':[True,False,True,False],
            'placement_status':['confirmed_Alba_program']*4,
            'program_code':['3','2','3','2']}))
        audit={'placement_status_counts':{'confirmed_Alba_program':4},
               'baseline_reconciled_flow':{'included':4}}
        with tempfile.TemporaryDirectory() as tmp, patch.object(hero,'OUTPUTS',Path(tmp)), \
             patch.object(hero,'prepare_analysis',return_value=(frame,self.programs,audit,{})):
            result=hero.run_hero(run=True,include_vocational=False,require_full_programs=False)
            comparison=result['variants']['comparison_exclude_vocational']
            self.assertEqual(comparison['N'],2)
            self.assertEqual(comparison['successes'],0)
            self.assertEqual(comparison['vocational_applicants_removed'],2)
            self.assertEqual(comparison['vocational_successes_removed'],2)
            folder=Path(result['run_directory'])
            self.assertFalse(json.loads((folder/'summary.json').read_text())['require_full_programs'])
            self.assertFalse(json.loads((folder/'run_record.json').read_text())['require_full_programs'])
            self.assertIn('requirement is OFF',(folder/'report.md').read_text())

    def test_reference_freezes_population_and_edges_but_allows_new_successes(self):
        frame=hero.outcome_population(hero.add_peer_axis(pd.DataFrame({
            'source_code':['1','1'],'analytic_row':[1,2], 'exam_score':[6.,8.],
            'grades_5_8_average':[7.,9.], 'admission_composite':[6.25,8.25],
            'A_z':[-1.,1.], 'placement_status':['confirmed_Alba_program']*2,
            'program_code':['1','2'], 'vocational':[False,False], 'success':[1.,0.]})))
        edges={k:hero.frozen_edges(frame.peer_mean_A_z,k) for k in ('equal_width','quantile')}
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);(folder/'baseline_include_vocational').mkdir()
            name='baseline_include_vocational/name_free_applicant_outcome_audit.csv.gz'
            frame.to_csv(folder/name,index=False,compression='gzip')
            hero.write_json(folder/'fixed_bin_edges.json',{k:v.tolist() for k,v in edges.items()})
            hero.write_json(folder/'run_record.json',{'output_hashes':{n:hero.source.sha256(folder/n) for n in (name,'fixed_bin_edges.json')}})
            changed=frame.copy();changed['success']=1.
            result=hero.reference_bin_edges(folder,changed,edges)
            for kind in edges:np.testing.assert_equal(result[kind],edges[kind])
            changed.loc[0,'peer_mean_A_z']+=.1
            with self.assertRaises(AssertionError):hero.reference_bin_edges(folder,changed,edges)

    def test_destination_is_observed_not_threshold(self):
        label = hero.classify_destination(placement("P","Other","10,00"), self.programs, {"1"})
        self.assertEqual(label["success"], 0)
        label = hero.classify_destination(placement("P","----- NEREPARTIZAT -----"), self.programs, {"1"})
        self.assertEqual(label["placement_status"], "confirmed_unassigned")
        self.assertEqual(label["success"], 0)
        label = hero.classify_destination(placement("P","Winner / CJ"), self.programs, {"1"})
        self.assertEqual(label["placement_status"], "confirmed_outside_Alba")
        self.assertTrue(np.isnan(label["success"]))

    def test_ambiguous_program_and_unknown_never_become_failure(self):
        programs = self.programs + [program("99","Winner")]
        for label in ("Winner", "Unrecognised"):
            result = hero.classify_destination(placement("P",label), programs, {"1"})
            self.assertTrue(np.isnan(result["success"]))

    def test_matching_respects_origin_score_and_unique_name(self):
        candidates = {
            "101":[{"Nume":"Same name","Medie Admitere":"8,00","Judeţ":"CJ"},
                   {"Nume":"Mismatch","Medie Admitere":"7,00"}],
            "102":[{"Nume":"Same name","Medie Admitere":"8,00"}],
            "103":[{"Nume":"Duplicate","Medie Admitere":"8,00"},
                   {"Nume":"Duplicate","Medie Admitere":"8,00"}],
        }
        placements = {"101":[placement("Same name","----- NEREPARTIZAT -----"),
                            placement("Mismatch","Winner","8,00")],
                      "102":[placement("Same name","Winner")],
                      "103":[placement("Duplicate","Winner"), placement("Duplicate","Other")]}
        frame = pd.DataFrame({"source_code":["101","101","102","103","103"],
                              "analytic_row":[1,2,1,1,2]})
        result = hero.attach_placements(frame,candidates,placements,self.programs)
        self.assertEqual(result["placement_status"].tolist(),[
            "confirmed_unassigned","composite_disagreement","confirmed_Alba_program",
            "ambiguous_person","ambiguous_person"])
        self.assertEqual(result["success"].iloc[2],1)
        self.assertFalse({"Nume","CNP"} & set(result.columns))

    def test_denominator_preserves_peers_bins_and_successes(self):
        frame = pd.DataFrame({
            "source_code":["1","1","1","2","2","2","3"],
            "A_z":[-2.,-1.,0.,0.,1.,2.,3.],
            "placement_status":["confirmed_Alba_program"]*6 + ["confirmed_outside_Alba"],
            "program_code":["1","3","2","1","3","2",""],
            "success":[1.,0.,0.,1.,0.,0.,np.nan],
            "vocational":[False,True,False,False,True,False,False],
        })
        frame=hero.add_peer_axis(frame)
        self.assertAlmostEqual(frame["peer_mean_A_z"].iloc[0],-.5)
        baseline=hero.outcome_population(frame,True)
        alternate=hero.outcome_population(frame,False)
        np.testing.assert_equal(baseline["peer_mean_A_z"].to_numpy(),alternate["peer_mean_A_z"].to_numpy())
        self.assertEqual(alternate["outcome_exclusion"].iloc[-1],"no_observed_peer")
        self.assertEqual(sum(alternate["outcome_exclusion"].value_counts()),len(frame))
        for kind in ("equal_width","quantile"):
            edges=hero.frozen_edges(baseline.loc[baseline.included_in_outcome,"peer_mean_A_z"],kind)
            a,b=hero.bin_table(baseline,edges),hero.bin_table(alternate,edges)
            self.assertEqual(a.N.sum(),6)
            self.assertEqual(b.N.sum(),4)
            self.assertEqual(a.successes.sum(),2)
            self.assertTrue(a.successes.equals(b.successes))
            self.assertTrue(b.loc[b.N.eq(0),"success_rate"].isna().all())

    def test_tied_quantiles_are_not_split_arbitrarily(self):
        edges=hero.frozen_edges([0]*40+[1]*40,"quantile")
        self.assertLess(len(edges)-1,16)
        self.assertEqual(edges[0],0)
        self.assertEqual(edges[-1],1)

    def test_corrupt_checkpoint_is_not_silently_reused(self):
        school={"code":"101","candidate_report":"raport_candidati_per_scoala.asp-cs=101.htm"}
        rows=[placement("A","Winner")]
        raw=b"synthetic, no source records"
        with tempfile.TemporaryDirectory() as temp, patch.object(hero,"CACHE",Path(temp)):
            payload={"schema":hero.SCHEMA,"source_code":"101",
                     "relative_url":hero.placement_relative(school),
                     "kind":"retrieved_placement_report",
                     "rows":rows,"rows_sha256":hero.digest(rows),
                     "headers":list(rows[0]),"raw_html_base64":base64.b64encode(raw).decode(),
                     "raw_html_sha256":hashlib.sha256(raw).hexdigest()}
            hero.write_json(hero.checkpoint_path("101"),payload)
            self.assertIsNotNone(hero.verify_checkpoint(school,1))
            payload["rows"][0]["Liceu"]="Changed"
            hero.write_json(hero.checkpoint_path("101"),payload)
            with self.assertRaises(ValueError):
                hero.verify_checkpoint(school,1)

    def test_preview_never_downloads(self):
        with patch.object(hero,"placement_status",return_value={"remaining_codes":["101"]}), \
             patch.object(hero.source,"load_structural_module",side_effect=AssertionError("Network client requested")):
            self.assertEqual(hero.acquire_placements(live=False)["remaining_codes"],["101"])

    def test_verified_superset_does_not_expand_frozen_population(self):
        school={"code":"101","candidate_report":"raport_candidati_per_scoala.asp-cs=101.htm"}
        candidates=[{"Nume":"A","Medie Admitere":"8,00"}]
        placements=[placement("A","Winner"),placement("Extra","Winner")]
        with patch.object(hero.source,"verified_cache_record",return_value={"rows":candidates}):
            audit=hero.validate_placement_count(school,1,placements)
        self.assertEqual(audit["unique_name_and_composite_matches"],1)
        self.assertEqual(audit["extra_report_rows_outside_frozen_population"],1)
        frame=pd.DataFrame({"source_code":["101"],"analytic_row":[1]})
        result=hero.attach_placements(frame,{"101":candidates},{"101":placements},self.programs)
        self.assertEqual(len(result),1)
        self.assertEqual(result["success"].sum(),1)

    def test_longer_report_rejects_missing_ambiguous_or_disagreeing_candidate(self):
        school={"code":"101","candidate_report":"raport_candidati_per_scoala.asp-cs=101.htm"}
        candidates=[{"Nume":"A","Medie Admitere":"8,00"}]
        bad_reports=[
            [placement("B","Winner"),placement("Extra","Other")],
            [placement("A","Winner"),placement("A","Winner")],
            [placement("A","Winner","9,00"),placement("Extra","Other")],
        ]
        with patch.object(hero.source,"verified_cache_record",return_value={"rows":candidates}):
            for rows in bad_reports:
                with self.subTest(rows=rows), self.assertRaises(ValueError):
                    hero.validate_placement_count(school,1,rows)
        with self.assertRaises(ValueError):
            hero.validate_placement_count(school,1,[])

    def test_longer_checkpoint_requires_reproducible_coverage_audit(self):
        school={"code":"101","candidate_report":"raport_candidati_per_scoala.asp-cs=101.htm"}
        candidates=[{"Nume":"A","Medie Admitere":"8,00"}]
        rows=[placement("A","Winner"),placement("Extra","Other")]
        raw=b"synthetic superset source"
        with tempfile.TemporaryDirectory() as temp, patch.object(hero,"CACHE",Path(temp)), \
             patch.object(hero.source,"verified_cache_record",return_value={"rows":candidates}):
            payload={"schema":hero.SCHEMA,"source_code":"101",
                "relative_url":hero.placement_relative(school),"kind":"retrieved_placement_report",
                "headers":list(rows[0]),"rows":rows,"rows_sha256":hero.digest(rows),
                "raw_html_base64":base64.b64encode(raw).decode(),
                "raw_html_sha256":hashlib.sha256(raw).hexdigest()}
            hero.write_json(hero.checkpoint_path("101"),payload)
            with self.assertRaises(ValueError):
                hero.verify_checkpoint(school,1)
            payload["candidate_coverage_audit"]=hero.validate_placement_count(school,1,rows)
            hero.write_json(hero.checkpoint_path("101"),payload)
            self.assertEqual(len(hero.verify_checkpoint(school,1)["rows"]),2)

    def test_fully_cached_resume_makes_no_requests(self):
        school={"code":"101","candidate_report":"raport_candidati_per_scoala.asp-cs=101.htm"}
        rows=[placement("A","Winner")]
        raw=b"synthetic"
        with tempfile.TemporaryDirectory() as temp, patch.object(hero,"CACHE",Path(temp)), \
             patch.object(hero.source,"_read_all_cached_reports",return_value=({},{})), \
             patch.object(hero.source,"read_completed_checkpoint",return_value=([school],{"101":{"candidate_rows":1}})), \
             patch.object(hero.source,"load_structural_module",side_effect=AssertionError("Network requested")):
            hero.write_json(hero.checkpoint_path("101"),{
                "schema":hero.SCHEMA,"source_code":"101","relative_url":hero.placement_relative(school),
                "kind":"retrieved_placement_report","rows":rows,"rows_sha256":hero.digest(rows),
                "headers":list(rows[0]),"raw_html_base64":base64.b64encode(raw).decode(),
                "raw_html_sha256":hashlib.sha256(raw).hexdigest()})
            self.assertEqual(hero.acquire_placements(live=True)["complete_codes"],1)
            self.assertEqual(json.loads((Path(temp)/"unresolved_addresses.json").read_text()),[])

    def test_failed_request_is_saved_in_queue_then_retried(self):
        school={"code":"101","candidate_report":"raport_candidati_per_scoala.asp-cs=101.htm"}
        rows=[placement("A","Winner")]
        calls=[]
        cooldowns=[]
        def fetch(*args, **kwargs):
            calls.append(args[0])
            if len(calls)==1:
                return None
            queue=json.loads((hero.CACHE/"unresolved_addresses.json").read_text())
            self.assertEqual(queue[0]["source_code"],"101")
            self.assertIn("unresolved",queue[0]["last_error"])
            return list(rows[0]),rows,[],{"test_only":True},b"synthetic"
        fake=SimpleNamespace(fetch=fetch, configure_retrieval=lambda *a,**k:None,
            CLIENT=SimpleNamespace(interval=2.,wait_between_passes=lambda *a:cooldowns.append(a)))
        with tempfile.TemporaryDirectory() as temp, patch.object(hero,"CACHE",Path(temp)), \
             patch.object(hero.source,"_read_all_cached_reports",return_value=({},{})), \
             patch.object(hero.source,"read_completed_checkpoint",return_value=([school],{"101":{"candidate_rows":1}})), \
             patch.object(hero.source,"load_structural_module",return_value=fake):
            result=hero.acquire_placements(live=True,retry_passes=2,retry_cooldown_seconds=0)
            self.assertEqual(result["remaining_codes"],[])
            self.assertEqual(len(calls),2)
            self.assertEqual(len(cooldowns),1)

    def test_full_synthetic_run_preserves_baseline_and_records_outputs(self):
        frame=hero.add_peer_axis(pd.DataFrame({
            "source_code":["1","1","2","2"],"analytic_row":[1,2,1,2],
            "A_z":[-1.,0.,1.,2.], "success":[0.,1.,0.,1.],
            "vocational":[True,False,True,False],
            "placement_status":["confirmed_Alba_program"]*4,
            "program_code":["3","1","3","1"],
        }))
        audit={"placement_status_counts":{"confirmed_Alba_program":4},
               "baseline_reconciled_flow":{"included":4}}
        with tempfile.TemporaryDirectory() as temp, patch.object(hero,"OUTPUTS",Path(temp)), \
             patch.object(hero,"prepare_analysis",return_value=(frame,self.programs,audit,{})):
            result=hero.run_hero(run=True,include_vocational=False)
            run_dir=Path(result["run_directory"])
            self.assertFalse((run_dir/"RUNNING.json").exists())
            self.assertEqual(result["variants"]["baseline_include_vocational"]["N"],4)
            self.assertEqual(result["variants"]["comparison_exclude_vocational"]["N"],2)
            record=json.loads((run_dir/"run_record.json").read_text())
            self.assertEqual(record['top_program_tiers'],1)
            for file,checksum in record["output_hashes"].items():
                self.assertEqual(hero.source.sha256(run_dir/file),checksum)

            # Exercise two-tier metadata, title and selected destinations without
            # reading research records or contacting the archive.
            result_two=hero.run_hero(run=True,top_program_tiers=2)
            two_dir=Path(result_two['run_directory'])
            self.assertNotEqual(two_dir,run_dir)
            self.assertEqual(json.loads((two_dir/'summary.json').read_text())['top_program_tiers'],2)
            self.assertEqual(json.loads((two_dir/'run_record.json').read_text())['top_program_tiers'],2)
            self.assertEqual({p['program_code'] for p in json.loads((two_dir/'selected_programs.json').read_text())},{'1','2'})
            self.assertIn('top 2 cutoff tier',(two_dir/'report.md').read_text())
            hero.prepare_analysis.assert_called_with(top_program_tiers=2, require_full_programs=True,
                                                     combine_program_categories=False)


if __name__ == "__main__":
    unittest.main()

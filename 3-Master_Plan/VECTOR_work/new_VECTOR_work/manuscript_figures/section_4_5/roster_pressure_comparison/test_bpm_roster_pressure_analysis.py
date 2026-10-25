"""Check source identities, peer calculations, and counts without plotting."""
import unittest
import numpy as np
import bpm_roster_pressure_analysis as b

class BPMChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources, _ = b.load_frozen_sources()
        cls.cfg = b.DEFAULTS.copy()
        cls.cohorts, cls.meta, _ = b.build_cohorts(cls.sources, cls.cfg)

    def test_full_roster_peer_means(self):
        roster, _ = b.prepare_roster(self.sources['all'], self.cfg)
        for frame in self.cohorts.values():
            for _, row in frame.iloc[::max(1,len(frame)//20)].iterrows():
                group = roster.loc[(roster.team_id==row.team_id)&(roster.season==row.season)]
                others = group.loc[group.athlete_id!=row.athlete_id]
                self.assertAlmostEqual(row.rp_shared, group.competitive_relevance.mean())
                self.assertAlmostEqual(row.rp_loo, others.competitive_relevance.mean())
                self.assertAlmostEqual(row.loo_performance, others.perf.mean())
                self.assertEqual(row.roster_n, len(group))

    def test_theta_gamma_do_not_change_bands_or_outcomes(self):
        alternative, _, _ = b.build_cohorts(self.sources, {**self.cfg,'gamma':.5,'theta_quantile':.9})
        for name, frame in self.cohorts.items():
            np.testing.assert_array_equal(frame.athlete_id, alternative[name].athlete_id)
            np.testing.assert_array_equal(frame.Y_draft, alternative[name].Y_draft)
            self.assertFalse(np.allclose(frame.rp_shared, alternative[name].rp_shared))
        self.assertTrue(set(self.cohorts['top'].athlete_id).isdisjoint(self.cohorts['next'].athlete_id))

    def test_all_bin_counts_and_modes(self):
        for mode in ['top_next','historical']:
            cohorts, _, _ = b.build_cohorts(self.sources,{**self.cfg,'band_mode':mode})
            tables, _, _, edges = b.build_tables(cohorts,self.cfg)
            for (_,name,_), table in tables.items():
                self.assertEqual(table.n.sum(),len(cohorts[name]))
                self.assertEqual(table.positive_rows.sum(),cohorts[name].Y_draft.sum())
            np.testing.assert_array_equal(edges['rp_shared'],edges['rp_loo'])

if __name__=='__main__':
    unittest.main()

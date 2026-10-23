"""Small mathematical checks independent of the NCAA source data."""
import unittest
import numpy as np
import pandas as pd
from scipy.special import expit
from roster_pressure_analysis import add_roster_pressure, bin_table, rank_bins, empirical_counts


class RosterPressureChecks(unittest.TestCase):
    def test_empirical_counts_do_not_count_repeated_seasons_as_draft_slots(self):
        f = pd.DataFrame({'athlete_id': [1, 1, 2, 3], 'Y_draft': [1, 1, 0, 0]})
        c = empirical_counts(f)
        self.assertEqual((c['K_emp'], c['N_emp']), (1, 3))
        self.assertAlmostEqual(c['K_over_N'], 1/3)
        self.assertEqual((c['D_rows'], c['N_rows']), (2, 4))

    def setUp(self):
        self.roster = pd.DataFrame(dict(athlete_id=range(1, 7), team_id=[1,1,1,2,2,3],
                                        season=[2021]*6, perf=[-1., 0., 2., 1., 3., .5],
                                        Y_draft=[0,0,1,0,1,0]))

    def test_loo_matches_direct_exclusion_and_singleton_is_undefined(self):
        out = add_roster_pressure(self.roster, theta=.7, gamma=2.)
        for _, row in out.iterrows():
            group = self.roster.loc[self.roster.team_id.eq(row.team_id)]
            peers = group.loc[group.athlete_id.ne(row.athlete_id)]
            self.assertAlmostEqual(row.rp_shared, expit(2*(group.perf-.7)).mean())
            if len(peers):
                self.assertAlmostEqual(row.rp_loo, expit(2*(peers.perf-.7)).mean())
                self.assertAlmostEqual(row.loo_performance, peers.perf.mean())
            else:
                self.assertTrue(np.isnan(row.rp_loo))
        self.assertEqual(out.Y_draft.tolist(), self.roster.Y_draft.tolist())

    def test_filter_after_aggregation_keeps_actual_teammates(self):
        out = add_roster_pressure(self.roster, theta=.7, gamma=2.)
        focal = out.loc[out.athlete_id.eq(3)].iloc[0]
        self.assertAlmostEqual(focal.rp_loo, expit(2*(np.array([-1.,0.])-.7)).mean())
        self.assertEqual(focal.roster_n, 3)
        self.assertLess(focal.rp_loo, focal.rp_shared)

    def test_averaging_relevance_is_not_sigmoid_of_average(self):
        r = pd.DataFrame(dict(athlete_id=range(4), team_id=[1,1,2,2], season=[2021]*4,
                             perf=[0.,2.,1.,1.], Y_draft=[0,1,0,1]))
        out = add_roster_pressure(r, theta=1.5, gamma=3.)
        self.assertEqual(out.groupby('team_id').T_j.first().nunique(), 1)
        self.assertEqual(out.groupby('team_id').rp_shared.first().nunique(), 2)

    def test_bins_preserve_endpoints_outcomes_and_rank_first_ties(self):
        f = pd.DataFrame(dict(athlete_id=range(16), team_id=[1]*16, season=[2021]*16,
                             perf=np.arange(16), Y_draft=[0,1]*8,
                             loo_performance=np.linspace(0,1,16), rp_shared=np.linspace(0,1,16),
                             rp_loo=np.linspace(0,1,16), team_season_key=['1:2021']*16))
        table, _, _ = bin_table(f, 'rp_loo', 'EW', 4, np.linspace(0,1,5))
        self.assertEqual(table.n.tolist(), [4,4,4,4])
        self.assertEqual(int(table.positive_rows.sum()), 8)
        labels = rank_bins(pd.Series([.2]*16), 4)
        self.assertEqual(labels.tolist(), [1]*4+[2]*4+[3]*4+[4]*4)


if __name__ == '__main__':
    unittest.main()

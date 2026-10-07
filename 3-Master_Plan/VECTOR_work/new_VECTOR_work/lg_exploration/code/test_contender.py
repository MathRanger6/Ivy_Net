"""Small checks of contender definitions and the self-excluded count identity."""
import unittest
import numpy as np
from lg_composition.contender_plot import contender_counts


class ContenderChecks(unittest.TestCase):
    def test_team_counts_and_self_exclusion(self):
        flag, counts, peers = contender_counts(
            np.array([-2., -1., 1., 2.]), np.array([0, 0, 1, 1]), 2, 0.)
        np.testing.assert_array_equal(flag, [False, False, True, True])
        np.testing.assert_array_equal(counts, [0, 2])
        np.testing.assert_array_equal(peers, [0, 0, 1, 1])
        self.assertEqual(peers.sum(), flag.sum() * (2 - 1))
        self.assertEqual(counts.mean(), 1.)

    def test_strict_cut_ties_and_singletons(self):
        flag, counts, peers = contender_counts(
            np.array([-1., 0., 1.]), np.array([0, 0, 0]), 1, 0.)
        np.testing.assert_array_equal(flag, [False, False, True])
        np.testing.assert_array_equal(peers, [1, 1, 0])
        _, _, peers = contender_counts(
            np.array([-1., 1.]), np.array([0, 1]), 2, 0.)
        np.testing.assert_array_equal(peers, [0, 0])


if __name__ == "__main__":
    unittest.main()

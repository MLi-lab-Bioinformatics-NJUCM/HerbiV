import unittest
from herbiv import get, analysis
from script import utils


class TestHerbiV(unittest.TestCase):
    def test_herbiv(self):
        get.get_formula('HVPID', ['HVP1625'])

    def test_herbiv_2(self):
        analysis.from_tcm_or_formula(['HVM0001'])


class TestHerbivRunner(unittest.TestCase):
    def test_check_id(self):
        self.assertTrue(utils.check_tcm_id("HVM0000"))
        self.assertFalse(utils.check_tcm_id("123456"))
        self.assertFalse(utils.check_tcm_id("HVM00100"))
        self.assertFalse(utils.check_tcm_id("HVM00100"))
        self.assertFalse(utils.check_tcm_id("HV00100"))
        self.assertTrue(utils.check_formula_id("HVP0001"))
        self.assertFalse(utils.check_formula_id("HVP00001"))
        self.assertFalse(utils.check_formula_id("HVP01"))
        self.assertFalse(utils.check_formula_id("HV00010"))
        self.assertFalse(utils.check_formula_id("HV     "))
        self.assertTrue(utils.check_protein_id("ENSP00000000233"))
        self.assertFalse(utils.check_protein_id("ENSP0000000233"))
        self.assertFalse(utils.check_protein_id("ENS000000000233"))

import unittest
from jsons import lp_params

lp_example = {
  "lp": {
    "facts": [],
    "assumptions": [],
    "clauses": [
      {
        "tag": "Cl",
        "clHead": {
          "idx": 1,
          "label": ""
        },
        "clPAtoms": [
          {
            "idx": 2,
            "label": ""
          },
          {
            "idx": 3,
            "label": ""
          }
        ],
        "clNAtoms": []
      },
      {
        "tag": "Cl",
        "clHead": {
          "idx": 2,
          "label": ""
        },
        "clPAtoms": [
          {
            "idx": 3,
            "label": ""
          }
        ],
        "clNAtoms": []
      },
      {
        "tag": "Cl",
        "clHead": {
          "idx": 2,
          "label": ""
        },
        "clPAtoms": [
          {
            "idx": 1,
            "label": ""
          }
        ],
        "clNAtoms": []
      }
    ]
  }
 }

class Test(unittest.TestCase):
    def test_clauses(self):
        self.assertEqual(lp_params(lp_example)["clauses"]["amount"],3)
        self.assertEqual(lp_params(lp_example)["clauses"]["onlyPos"],3)
        self.assertEqual(lp_params(lp_example)["clauses"]["onlyNeg"],0)
        self.assertEqual(lp_params(lp_example)["clauses"]["mix"],0)
        self.assertEqual(lp_params(lp_example)["clauses"]["headWithH"],0)

    def test_atoms(self):
        self.assertEqual(lp_params(lp_example)["clauses"]["atoms"]["sum"],4)
        self.assertEqual(lp_params(lp_example)["clauses"]["atoms"]["pos"],4)
        self.assertEqual(lp_params(lp_example)["clauses"]["atoms"]["neg"],0)
        self.assertEqual(lp_params(lp_example)["clauses"]["atoms"]["withH"],0)
        self.assertEqual(lp_params(lp_example)["clauses"]["atoms"]["posWithH"],0)
        self.assertEqual(lp_params(lp_example)["clauses"]["atoms"]["negWithH"],0)

    def test_difAtoms(self):
        self.assertEqual(lp_params(lp_example)["clauses"]["difAtoms"]["sum"],3)
        self.assertEqual(lp_params(lp_example)["clauses"]["difAtoms"]["pos"],3)
        self.assertEqual(lp_params(lp_example)["clauses"]["difAtoms"]["neg"],0)
        self.assertEqual(lp_params(lp_example)["clauses"]["difAtoms"]["withH"],0)
        self.assertEqual(lp_params(lp_example)["clauses"]["difAtoms"]["posWithH"],0)
        self.assertEqual(lp_params(lp_example)["clauses"]["difAtoms"]["negWithH"],0)

    def test_facts(self):
        self.assertEqual(lp_params(lp_example)["facts"],0)

    def test_assumptions(self):
        self.assertEqual(lp_params(lp_example)["assumptions"],0)

if __name__ == '__main__':
    unittest.main()

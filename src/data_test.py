
 
from data import load
import unittest

file_names = [
    "src/output_test/sheets/membros-ativos-contracheque-01-2020.xls",
    "src/output_test/sheets/membros-ativos-indenizatorias-01-2020.xls",
]


class TestData(unittest.TestCase):
    def test_validate_existence(self):
        STATUS_DATA_UNAVAILABLE = 4
        with self.assertRaises(SystemExit) as cm:
            dados = load(file_names, "2021", "01", "src/output_test")
            dados.validate("src/output_test/sheets/")
        self.assertEqual(cm.exception.code, STATUS_DATA_UNAVAILABLE)


if __name__ == "__main__":
    unittest.main()
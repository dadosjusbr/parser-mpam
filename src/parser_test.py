from parser import parse
import unittest
import json
from google.protobuf.json_format import MessageToDict
from data import load


class TestParser(unittest.TestCase):
    def test_jan_2020(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open("src/output_test/expected/expected_01_2020.json", "r") as fp:
            expected_01_2020 = json.load(fp)

        files = ["src/output_test/sheets/membros-ativos-contracheque-01-2020.xls",
        "src/output_test/sheets/membros-ativos-indenizatorias-01-2020.xls"]

        dados = load(files, "2020", "01", "src/output_test/sheets")
        result_data = parse(dados, "mpam/01/2020")
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        self.assertEqual(expected_01_2020, result_to_dict)


if __name__ == "__main__":
    unittest.main()
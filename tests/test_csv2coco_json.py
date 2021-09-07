from scripts.csv2coco_json import csv2coco_json
from scripts.utils.json_handler import load_json

info = {}
licenses = []


def test_csv2coco():
    test_result = csv2coco_json(
        info,
        licenses,
        csv_fpath=
        "/host_server/home/yjh2020/Codes/cv-utilities/tests/test_ann.csv",
        save_fpath=
        "/host_server/home/yjh2020/Codes/cv-utilities/tests/test_result.json")
    true_result = load_json(
        "/host_server/home/yjh2020/Codes/cv-utilities/tests/test_ann.json")
    assert test_result == true_result

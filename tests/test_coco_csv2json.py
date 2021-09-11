from scripts.coco_csv2json import coco_csv2json
from scripts.utils.json_handler import load_json

info = {}


def test_coco_csv2json():
    test_result = coco_csv2json(
        info,
        csv_fpath="/host_server/home/yjh2020/Codes/cv-utilities/tests/"
        "test_cases/test_coco_csv2json/test_ann.csv",
        save_fpath="/host_server/home/yjh2020/Codes/cv-utilities/tests/"
        "test_cases/test_coco_csv2json/test_ann_result.json")
    true_result = load_json(
        "/host_server/home/yjh2020/Codes/cv-utilities/tests/"
        "test_cases/test_coco_csv2json/test_ann_gt.json")
    assert test_result == true_result

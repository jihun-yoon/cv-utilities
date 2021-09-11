from pycocotools.coco import COCO
import pycocotools.mask as maskUtils

import pandas as pd
from scripts.coco_mask2csv import coco_mask2csv

test_cats = [{
    "id": 1,
    "name": "a",
    "supercategory": "a"
}, {
    "id": 2,
    "name": "b",
    "supercategory": "b"
}, {
    "id": 3,
    "name": "c",
    "supercategory": "c"
}]

test_pixel_cat_map = {
    1: {
        1: "a"
    },
    2: {
        2: "b"
    },
    3: {
        3: "c"
    },
}


def ann2rle(width, height, segmentation):
    """Convert annotation which can be polygons, uncompressed RLE to RLE.

    Reference: https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/coco.py

    Args:
        width (int): Width of input image
        height (int): Height of input image
        segmentation ([type]): [description]

    Returns:
        np.array: binary mask (numpy 2D array)
    """

    h, w = height, width
    segm = segmentation
    if isinstance(segm, list):
        # polygon -- a single object might consist of multiple parts
        # we merge all parts into one mask rle code
        rles = maskUtils.frPyObjects(segm, h, w)
        rle = maskUtils.merge(rles)
    elif isinstance(segm['counts'], list) == list:
        # uncompressed RLE
        rle = maskUtils.frPyObjects(segm, h, w)
    else:
        # rle
        rle = segmentation
    return rle


def test_mask2bbox_csv():
    dt = coco_mask2csv(
        mask_dir="tests/test_cases/test_coco_mask2csv",
        mask_ext="png",
        save_fpath=
        "tests/test_cases/test_coco_mask2csv/test_mask_result_ann.csv",
        num_process=2,
        bg_pixels=[0, 100],
        coco_cats=test_cats,
        pixel_cat_map=test_pixel_cat_map)

    gt = pd.read_csv(
        "/host_server/home/yjh2020/Codes/cv-utilities/tests/test_cases/"
        "test_coco_mask2csv/test_mask_gt_ann.csv")

    gt_dt = gt.merge(dt, how="outer", left_index=True, right_index=True)
    gt_dt["segmentation_x"] = gt_dt["segmentation_x"].apply(lambda x: eval(x))
    gt_dt["bbox_x"] = gt_dt["bbox_x"].apply(lambda x: eval(x))
    gt_dt["segmentation_y"] = gt_dt["segmentation_y"].apply(lambda x: eval(x))
    gt_dt["bbox_y"] = gt_dt["bbox_y"].apply(lambda x: eval(x))
    for idx, row in gt_dt.iterrows():
        gt_w = row.width_x
        gt_h = row.height_x
        gt_segm = row.segmentation_x
        gt_bbox = list(row.bbox_x)
        gt_ic = row.iscrowd_x

        dt_w = row.width_y
        dt_h = row.height_y
        dt_segm = row.segmentation_y
        dt_bbox = list(row.bbox_y)
        dt_ic = row.iscrowd_y

        assert gt_ic == dt_ic, "iscrowd value is wrong"
        gt_rle = ann2rle(gt_w, gt_h, gt_segm)
        dt_rle = ann2rle(dt_w, dt_h, dt_segm)
        segm_iou = maskUtils.iou([gt_rle], [dt_rle], [gt_ic])
        bbox_iou = maskUtils.iou([gt_bbox], [dt_bbox], [gt_ic])
        assert segm_iou >= 0.98, "Segmentation IoU is lower than 0.98"
        assert bbox_iou >= 0.98, "BBox IoU is lower than 0.98"

        print(f"index: {idx}")
        print(f"segm_iou: {segm_iou}")
        print(f"bbox_iou: {bbox_iou}")
import pandas as pd  # pylint: disable=C0114
from utils.json_handler import dump_json


def table_to_coco_json(coco_info,
                       coco_licenses,
                       coco_df=None,
                       csv_fpath=None,
                       save_fpath=None):
    """Generate COCO style json from Pandas.DataFrame

    Annotation Data Columns:
        image_id (int)
        width (int)
        height (int)
        file_name (str)
        license (int)
        #flickr_url # TODO: 삭제
        #coco_url # TODO: 삭제
        date_captured (datetime)
        ann_id (int)
        segmentation ([polygon])
        area (float)
        bbox ([x,y,width,height])
        iscrowd (int)
        category_id (int)
        category_name (str)
        supercategory (str)

    Args:
        coco_df (Pandas.DataFrame): annotation in Pandas.DataFrame of annota
        info (dict): COCO style information of the annotation
        licenses (list): COCO style lincenses of the annotation
        csv_fpath (str, optional): path of annotation csv file . Defaults to None.
        save_fpath (str, optional): [description]. Defaults to None.

    Returns:
        dict: COCO style json
    """
    if coco_df is None and csv_fpath is None:
        # TODO: assert 추가하기
        return
    if csv_fpath is not None:
        coco_df = pd.read_csv(csv_fpath)

    coco_df.astype({
        "image_id": "int32",
        "width": "int32",
        "height": "int32",
        "file_name": "str",
        "license_id": "int32",
        "date_captured": "str",
        "ann_id": "int32",
        "category_id": "int32",
        "segmentation": "str",
        "area": "float64",
        "bbox": "str",
        "iscrowd": "int32"
    })
    # TODO: get rid of eval()
    coco_df["segmentation"] = coco_df["segmentation"].apply(lambda x: eval(x))  # pylint: disable=W0108
    coco_df["bbox"] = coco_df["bbox"].apply(lambda x: eval(x))  # pylint: disable=W0108

    image_coco_df = coco_df[[
        "image_id", "width", "height", "file_name", "license_id",
        "date_captured"
    ]].copy()
    image_coco_df = image_coco_df.sort_values(["image_id"])
    image_coco_df.rename({"image_id": "id", "license_id": "license"})
    images = list(image_coco_df.to_dict("index").values())

    ann_coco_df = coco_df[[
        "ann_id", "image_id", "category_id", "segmentation", "area", "bbox",
        "iscrowd"
    ]].copy()
    ann_coco_df = ann_coco_df.sort_values("ann_id")
    ann_coco_df = ann_coco_df.rename({"ann_id": "id"})
    annotations = list(ann_coco_df.to_dict("index").values())

    category_coco_df = coco_df.drop_duplicates(
        ["category_id", "category_name", "supercategory"])
    category_coco_df = category_coco_df.sort_values(["category_id"])
    categories = list(category_coco_df.to_dict("index").values())

    coco_format = {
        "info": coco_info,
        "licenses": coco_licenses,
        "images": images,
        "annotations": annotations,
        "categories": categories,
    }
    if save_fpath is not None:
        dump_json(save_fpath, coco_format)

    return coco_format


if __name__ == "__main__":
    info = {}
    licenses = []

    table_to_coco_json(info, licenses, csv_fpath="", save_fpath="")

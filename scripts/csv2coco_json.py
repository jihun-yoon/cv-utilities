import pandas as pd  # pylint: disable=C0114
from .utils.json_handler import dump_json


def csv2coco_json(coco_info,
                  coco_licenses,
                  coco_df=None,
                  csv_fpath=None,
                  save_fpath=None):
    """Generate COCO style json from csv(Pandas.DataFrame)

    Csv columns:
        image_id (int)
        width (int)
        height (int)
        file_name (str)
        license_id (int)
        #flickr_url # TODO: delete
        #coco_url # TODO: delete
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
        csv_fpath (:None:`str`, optional): path of annotation csv file
            where to load. Defaults to None.
        save_fpath (:None:`str`, optional): path of annotation json file
            where to save. Defaults to None.

    Returns:
        dict: COCO style json
    """
    assert coco_df is not None or csv_fpath is not None, \
        "Either of coco_df and csv_fpath must not be none."
    if csv_fpath is not None:
        coco_df = pd.read_csv(csv_fpath)
    print(coco_df.columns)

    coco_df.astype({
        "image_id": "int32",
        "width": "int32",
        "height": "int32",
        "file_name": "str",
        "license_id": "int32",
        "date_captured": "str",
        "ann_id": "int32",
        "segmentation": "str",
        "area": "float64",
        "bbox": "str",
        "iscrowd": "int32",
        "category_id": "int32",
        "category_name": "str",
        "supercategory": "str"
    })
    # TODO: get rid of eval()
    coco_df["segmentation"] = coco_df["segmentation"].apply(lambda x: eval(x))  # pylint: disable=W0108
    coco_df["bbox"] = coco_df["bbox"].apply(lambda x: eval(x))  # pylint: disable=W0108

    image_coco_df = coco_df[[
        "image_id", "width", "height", "file_name", "license_id",
        "date_captured"
    ]].copy()
    image_coco_df = image_coco_df.sort_values(["image_id"])
    image_coco_df = image_coco_df.rename(columns={
        "image_id": "id",
        "license_id": "license"
    })

    images = list(image_coco_df.to_dict("index").values())

    ann_coco_df = coco_df[[
        "ann_id", "image_id", "category_id", "segmentation", "area", "bbox",
        "iscrowd"
    ]].copy()
    ann_coco_df = ann_coco_df.sort_values("ann_id")
    ann_coco_df = ann_coco_df.rename(columns={"ann_id": "id"})
    annotations = list(ann_coco_df.to_dict("index").values())

    category_coco_df = coco_df[[
        "category_id", "category_name", "supercategory"
    ]].copy()
    category_coco_df = category_coco_df.drop_duplicates(
        ["category_id", "category_name", "supercategory"])
    category_coco_df = category_coco_df.sort_values(["category_id"])
    category_coco_df = category_coco_df.rename(columns={
        "category_id": "id",
        "category_name": "name"
    })
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

    csv2coco_json(info, licenses, csv_fpath="", save_fpath="")

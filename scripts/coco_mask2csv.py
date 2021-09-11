import os
from glob import glob
from datetime import date
from itertools import repeat
from itertools import chain
from operator import methodcaller
from collections import defaultdict
import multiprocessing as mp

import numpy as np
import pandas as pd
from PIL import Image
from skimage import measure
from shapely.geometry import Polygon, MultiPolygon
from tqdm import tqdm


def create_ann_from_sub_mask(sub_mask, category_id):
    """Create annotations(segmentation, bounding box, area) from sub mask image.

    Reference:
        https://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch

    Args:
        sub_mask (PIL.Image): sub mask image for a label RGB color
        image_id (str): ID of image
        category_id (str): ID of category

    Returns:
        dict: dictionary of annotation
    """

    # Find contours (boundary lines) around each sub-mask
    # Note: there could be multiple contours if the object
    # is partially occluded. (E.g. an elephant behind a tree)

    contours = measure.find_contours(image=sub_mask,
                                     level=0.5,
                                     positive_orientation="low")

    segmentations = []
    polygons = []
    for contour in contours:
        # Flip from (row, col) representation to (x, y)
        for i in range(len(contour)):
            row, col = contour[i]
            contour[i] = (col - 1, row - 1)  # subtract the padding pixel

        poly = Polygon(contour)
        polygons.append(poly)

        segmentation = np.array(poly.exterior.coords).ravel().tolist()
        segmentation = list(map(max, repeat(0),
                                segmentation))  # Make a value zero if negative
        segmentations.append(segmentation)
    # Follows the definition of iscrowd in COCO.
    # If segmentation is represented as RLE then iscrowd=1
    is_crowd = 0

    # Combine the polygons to calculate the bounding box and area
    multi_poly = MultiPolygon(polygons)
    multi_poly_bounds = multi_poly.bounds
    min_x, min_y, max_x, max_y = list(map(
        max, repeat(0), multi_poly_bounds))  # Make a value zero if negative
    width = max_x - min_x
    height = max_y - min_y
    bbox = [min_x, min_y, width, height]
    area = multi_poly.area

    ann = {
        "segmentation": segmentations,
        "iscrowd": is_crowd,
        "category_id": int(category_id),
        "bbox": bbox,
        "area": area,
    }

    #del sub_mask # TODO: check if it is effective for memory management
    return ann


def gather_ann_from_sub_masks(fpath, bg_pixels, coco_cats, pixel_cat_map):
    """Gather annotations(segmentation, bounding box, area) from sub mask images.

    Reference:
        https://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch

    Args:
        fpath (str): path for mask image
        bg_pixels (list): list of background pixel values

    Returns:
        dict: COCO style annotation(bbox and polygon) from sub mask
    """

    coco_dic = defaultdict(list)
    im = Image.open(fpath)
    width, height = im.size
    # Initialize a dictionary of sub-masks indexed by cat_id
    sub_masks = {}
    for x in range(width):
        for y in range(height):
            # Get the RGB values of the pixel
            pixel = im.getpixel((x, y))
            # If the pixel is not background
            if pixel not in bg_pixels:
                # Check to see if we've created a sub-mask
                pixel_str = str(pixel)  # pixel value means category id
                sub_mask = sub_masks.get(pixel_str)
                if sub_mask is None:
                    # Create a sub-mask (one bit per pixel)
                    # and add to the dictionary
                    # Note: we add 1 pixel of padding in each direction
                    # because the contours module doesn't handle cases
                    # where pixels bleed to the edge of the image
                    sub_masks[pixel_str] = Image.new(
                        "1",  # see Pillow mode
                        (width + 2, height + 2))
                # Set the pixel value to 1 (default is 0),
                # accounting for padding
                sub_masks[pixel_str].putpixel((x + 1, y + 1), 1)

    for cat_id, sub_mask in sub_masks.items():
        ann = create_ann_from_sub_mask(
            sub_mask=np.array(sub_mask),
            category_id=list(pixel_cat_map[int(cat_id)].keys())[0])
        coco_dic["image_id"].append(-1)  # reset later
        coco_dic["width"].append(width)
        coco_dic["height"].append(height)
        coco_dic["file_name"].append(os.path.basename(fpath))
        coco_dic["date_captured"].append(date.today().isoformat())
        coco_dic["ann_id"].append(-1)  # reset later
        coco_dic["segmentation"].append(str(
            ann["segmentation"]))  # TODO: what if doesn't convert into `str`
        coco_dic["area"].append(ann["area"])
        coco_dic["bbox"].append(str(ann["bbox"]))
        coco_dic["iscrowd"].append(ann["iscrowd"])
        coco_dic["category_id"].append(ann["category_id"])
        coco_dic["category_name"].append(coco_cats[ann["category_id"] -
                                                   1]["name"])
        coco_dic["supercategory"].append(coco_cats[ann["category_id"] -
                                                   1]["supercategory"])

    return coco_dic


def coco_mask2csv(mask_dir, mask_ext, save_fpath, num_process, bg_pixels,
                  coco_cats, pixel_cat_map):
    """Convert mask annotation into COCO style annotation(bbox and polygon)
    and save in csv file.

    Args:
        mask_dir (str): directory for mask images
        mask_ext (str): file extension of mask images (e.g. 'png', 'jpg')
        save_fpath (str): csv file path to save
        num_process (int): the number of processes for multi-processing

    Returns:
        Pandas.DataFrame: COCO style annotation in Pandas.Dataframe
    """

    pool = mp.Pool(processes=num_process)
    partial_results = []
    print(os.path.join(mask_dir, f"*.{mask_ext}"))
    fpaths = glob(os.path.join(mask_dir, f"*.{mask_ext}"))

    for fpath in tqdm(fpaths):
        partial_results.append(
            pool.apply_async(gather_ann_from_sub_masks,
                             args=(fpath, bg_pixels, coco_cats,
                                   pixel_cat_map)))
    partial_results = [p.get() for p in partial_results]

    merged_results = defaultdict(list)
    dict_items = map(methodcaller("items"), partial_results)
    for k, v in chain.from_iterable(dict_items):
        merged_results[k].extend(v)

    coco_df = pd.DataFrame(merged_results)
    #print(coco_df)
    coco_df["file_name"] = coco_df.file_name.apply(
        lambda x: os.path.basename(x))
    # image id starts from 1
    coco_df["image_id"] = coco_df.groupby(["file_name"]).ngroup() + 1
    coco_df.sort_values(["image_id", "category_id"], inplace=True)

    coco_df["ann_id"] = range(1, len(coco_df) + 1)
    coco_df.reset_index(drop=True, inplace=True)
    coco_df.to_csv(save_fpath, index=False)

    print(f"Saved: {save_fpath}")

    return coco_df
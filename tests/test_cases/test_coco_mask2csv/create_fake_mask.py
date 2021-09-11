from PIL import Image
import numpy as np


def generate_test_mask(save_fpath, mask_shape, polygon_shape, minxs, minys,
                       cats):
    test_mask = np.zeros((mask_shape[0], mask_shape[1]))
    for minx, miny, cat in zip(minxs, minys, cats):
        test_mask[minx:minx + polygon_shape[0],
                  miny:miny + polygon_shape[1]] = cat
    test_mask = test_mask.astype(np.uint8)
    img = Image.fromarray(test_mask)
    img.save(save_fpath)


# test_mask1.png
generate_test_mask(save_fpath="test_mask1.png",
                   mask_shape=(1000, 1000),
                   polygon_shape=(100, 100),
                   minxs=[100, 260, 510],
                   minys=[100, 260, 510],
                   cats=[1, 1, 3])

# test_mask2.png
generate_test_mask(save_fpath="test_mask2.png",
                   mask_shape=(1000, 1000),
                   polygon_shape=(100, 100),
                   minxs=[200, 360],
                   minys=[200, 360],
                   cats=[2, 1])

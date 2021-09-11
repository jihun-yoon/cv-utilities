"""
Define COCO style categories and a map between mask colors and categories.
COCO style categories follows COCO format.
Reference: https://cocodataset.org/#format-data
"""

coco_cats = [
    {
        "id": 1,
        "name": "HarmonicAce_Head",
        "supercategory": "HarmonicAce"
    },
    {
        "id": 2,
        "name": "HarmonicAce_Body",
        "supercategory": "HarmonicAce"
    },
    {
        "id": 3,
        "name": "MarylandBipolarForceps_Head",
        "supercategory": "MarylandBipolarForceps",
    },
    {
        "id": 4,
        "name": "MarylandBipolarForceps_Wrist",
        "supercategory": "MarylandBipolarForceps",
    },
    {
        "id": 5,
        "name": "MarylandBipolarForceps_Body",
        "supercategory": "MarylandBipolarForceps",
    },
    {
        "id": 6,
        "name": "CadiereForceps_Head",
        "supercategory": "CadiereForceps"
    },
    {
        "id": 7,
        "name": "CadiereForceps_Wrist",
        "supercategory": "CadiereForceps",
    },
    {
        "id": 8,
        "name": "CadiereForceps_Body",
        "supercategory": "CadiereForceps"
    },
    {
        "id": 9,
        "name": "CurvedAtraumaticGrasper_Head",
        "supercategory": "CurvedAtraumaticGrasper",
    },
    {
        "id": 10,
        "name": "CurvedAtraumaticGrasper_Body",
        "supercategory": "CurvedAtraumaticGrasper",
    },
    {
        "id": 11,
        "name": "Stapler_Head",
        "supercategory": "Stapler"
    },
    {
        "id": 12,
        "name": "Stapler_Body",
        "supercategory": "Stapler"
    },
    {
        "id": 13,
        "name": "Medium-LargeClipApplier_Head",
        "supercategory": "Medium-LargeClipApplier",
    },
    {
        "id": 14,
        "name": "Medium-LargeClipApplier_Wrist",
        "supercategory": "Medium-LargeClipApplier",
    },
    {
        "id": 15,
        "name": "Medium-LargeClipApplier_Body",
        "supercategory": "Medium-LargeClipApplier",
    },
    {
        "id": 16,
        "name": "SmallClipApplier_Head",
        "supercategory": "SmallClipApplier",
    },
    {
        "id": 17,
        "name": "SmallClipApplier_Wrist",
        "supercategory": "SmallClipApplier",
    },
    {
        "id": 18,
        "name": "SmallClipApplier_Body",
        "supercategory": "SmallClipApplier",
    },
    {
        "id": 19,
        "name": "Suction-Irrigation",
        "supercategory": "Suction-Irrigation",
    },
    {
        "id": 20,
        "name": "Needle",
        "supercategory": "Needle"
    },
    {
        "id": 21,
        "name": "Endotip",
        "supercategory": "Endotip"
    },
    {
        "id": 22,
        "name": "Specimenbag",
        "supercategory": "Specimenbag"
    },
    {
        "id": 23,
        "name": "DrainTube",
        "supercategory": "DrainTube"
    },
    {
        "id": 24,
        "name": "Liver",
        "supercategory": "Liver"
    },
    {
        "id": 25,
        "name": "Stomach",
        "supercategory": "Stomach"
    },
    {
        "id": 26,
        "name": "Pancreas",
        "supercategory": "Pancreas"
    },
    {
        "id": 27,
        "name": "Spleen",
        "supercategory": "Spleen"
    },
    {
        "id": 28,
        "name": "Gallbladder",
        "supercategory": "Gallbladder"
    },
    {
        "id": 29,
        "name": "Gauze",
        "supercategory": "Gauze"
    },
    {
        "id": 30,
        "name": "The_Other_Instruments",
        "supercategory": "The"
    },
    {
        "id": 31,
        "name": "The_Other_Tissues",
        "supercategory": "The"
    },
]

pixel_cat_map = {
    0: {
        0: "Backgound"
    },
    1: {
        1: "HarmonicAce_Head"
    },
    2: {
        2: "HarmonicAce_Body"
    },
    3: {
        3: "MarylandBipolarForceps_Head"
    },
    4: {
        4: "MarylandBipolarForceps_Wrist"
    },
    5: {
        5: "MarylandBipolarForceps_Body"
    },
    6: {
        6: "CadiereForceps_Head"
    },
    7: {
        7: "CadiereForceps_Wrist"
    },
    8: {
        8: "CadiereForceps_Body"
    },
    9: {
        9: "CurvedAtraumaticGrasper_Head"
    },
    10: {
        10: "CurvedAtraumaticGrasper_Body"
    },
    11: {
        11: "Stapler_Head"
    },
    12: {
        12: "Stapler_Body"
    },
    13: {
        13: "Medium-LargeClipApplier_Head"
    },
    14: {
        14: "Medium-LargeClipApplier_Wrist"
    },
    15: {
        15: "Medium-LargeClipApplier_Body"
    },
    16: {
        16: "SmallClipApplier_Head"
    },
    17: {
        17: "SmallClipApplier_Wrist"
    },
    18: {
        18: "SmallClipApplier_Body"
    },
    19: {
        19: "Suction-Irrigation"
    },
    20: {
        20: "Needle"
    },
    21: {
        21: "Endotip"
    },
    22: {
        22: "Specimenbag"
    },
    23: {
        23: "DrainTube"
    },
    24: {
        24: "Liver"
    },
    25: {
        25: "Stomach"
    },
    26: {
        26: "Pancreas"
    },
    27: {
        27: "Spleen"
    },
    28: {
        28: "Gallbladder"
    },
    29: {
        29: "Gauze"
    },
    30: {
        30: "The_Other_Instruments"
    },
    31: {
        31: "The_Other_Tissues"
    },
    100: {
        0: "Backgound"
    },
    101: {
        1: "HarmonicAce_Head"
    },
    102: {
        2: "HarmonicAce_Body"
    },
    103: {
        3: "MarylandBipolarForceps_Head"
    },
    104: {
        4: "MarylandBipolarForceps_Wrist"
    },
    105: {
        5: "MarylandBipolarForceps_Body"
    },
    106: {
        6: "CadiereForceps_Head"
    },
    107: {
        7: "CadiereForceps_Wrist"
    },
    108: {
        8: "CadiereForceps_Body"
    },
    109: {
        9: "CurvedAtraumaticGrasper_Head"
    },
    110: {
        10: "CurvedAtraumaticGrasper_Body"
    },
    111: {
        11: "Stapler_Head"
    },
    112: {
        12: "Stapler_Body"
    },
    113: {
        13: "Medium-LargeClipApplier_Head"
    },
    114: {
        14: "Medium-LargeClipApplier_Wrist"
    },
    115: {
        15: "Medium-LargeClipApplier_Body"
    },
    116: {
        16: "SmallClipApplier_Head"
    },
    117: {
        17: "SmallClipApplier_Wrist"
    },
    118: {
        18: "SmallClipApplier_Body"
    },
    119: {
        19: "Suction-Irrigation"
    },
    120: {
        20: "Needle"
    },
    121: {
        21: "Endotip"
    },
    122: {
        22: "Specimenbag"
    },
    123: {
        23: "DrainTube"
    },
    124: {
        24: "Liver"
    },
    125: {
        25: "Stomach"
    },
    126: {
        26: "Pancreas"
    },
    127: {
        27: "Spleen"
    },
    128: {
        28: "Gallbladder"
    },
    129: {
        29: "Gauze"
    },
    130: {
        30: "The_Other_Instruments"
    },
    131: {
        31: "The_Other_Tissues"
    },
}

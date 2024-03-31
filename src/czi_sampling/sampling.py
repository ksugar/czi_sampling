from argparse import ArgumentParser
import operator
from pathlib import Path
from typing import Union
import multiprocessing as mp
import re
import xml.etree.ElementTree as ET

from czifile import CziFile
import numpy as np
import tifffile


def process_file(filename: Union[str, Path]):
    filename = Path(filename)
    with CziFile(filename) as czi:
        image = czi.asarray()
    image = np.squeeze(image)
    if image.ndim != 4:
        raise ValueError(f"Image has {image.ndim} dimensions, expected 4.")
    index = int(re.search("pt(\d*).czi", filename.name).group(1))
    return index, image


def main(input_dir: str, output_dir: str):
    p_indir = Path(input_dir)
    p_indir.mkdir(parents=True, exist_ok=True)
    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.map(process_file, p_indir.glob("*.czi"))
    images = list(map(operator.itemgetter(1), sorted(results, key=lambda x: x[0])))
    images = np.array(images)
    print(images.shape, images.dtype)
    czi = CziFile(next(p_indir.glob("*.czi")))
    metadata = czi.metadata()
    root = ET.fromstring(metadata)
    distances = root.find("Metadata").find("Scaling").find("Items")
    scale_x = float(distances[0].find("Value").text)
    scale_y = float(distances[1].find("Value").text)
    scale_z = float(distances[2].find("Value").text)
    unit = "um"
    p_outdir = Path(output_dir)
    p_outdir.mkdir(parents=True, exist_ok=True)
    tifffile.imwrite(
        p_outdir / "original.tif",
        np.swapaxes(images, 1, 2),
        resolution=(1 / scale_x, 1 / scale_y),
        metadata={
            "spacing": scale_z,
            "unit": unit,
            "axes": "TZCYX",
        },
    )
    image_mean4 = np.mean(images, axis=1).clip(0, 255).astype(np.uint8)
    tifffile.imwrite(
        p_outdir / "4E.tif",
        image_mean4,
        imagej=True,
        resolution=(1 / scale_x, 1 / scale_y),
        metadata={
            "spacing": scale_z,
            "unit": unit,
            "axes": "TZYX",
        },
    )
    image_mean2 = np.mean(images[:, ::2], axis=1).clip(0, 255).astype(np.uint8)
    image_mean1 = images[:, 0]
    image_standard = image_mean4[::2, ::2]
    tifffile.imwrite(
        p_outdir / "standard.tif",
        image_standard,
        imagej=True,
        resolution=(1 / scale_x, 1 / scale_y),
        metadata={
            "spacing": scale_z * 2,
            "unit": unit,
            "axes": "TZYX",
        },
    )
    image_improved_z = image_mean2[::2]
    tifffile.imwrite(
        p_outdir / "improved_z.tif",
        image_improved_z,
        imagej=True,
        resolution=(1 / scale_x, 1 / scale_y),
        metadata={
            "spacing": scale_z,
            "unit": unit,
            "axes": "TZYX",
        },
    )
    image_improved_t = image_mean2[:, ::2]
    tifffile.imwrite(
        p_outdir / "improved_t.tif",
        image_improved_t,
        imagej=True,
        resolution=(1 / scale_x, 1 / scale_y),
        metadata={
            "spacing": scale_z * 2,
            "unit": unit,
            "axes": "TZYX",
        },
    )
    image_improved_zt1 = image_mean4[:, :, ::2, ::2]
    tifffile.imwrite(
        p_outdir / "improved_zt1.tif",
        image_improved_zt1,
        imagej=True,
        resolution=(1 / (scale_x * 2), 1 / (scale_y * 2)),
        metadata={
            "spacing": scale_z,
            "unit": unit,
            "axes": "TZYX",
        },
    )
    image_improved_zt2 = image_mean1
    tifffile.imwrite(
        p_outdir / "improved_zt2.tif",
        image_improved_zt2,
        imagej=True,
        resolution=(1 / scale_x, 1 / scale_y),
        metadata={
            "spacing": scale_z,
            "unit": unit,
            "axes": "TZYX",
        },
    )


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Downsample CZI images.",
        epilog="Example: python sampling.py dir_with_czi_files",
    )
    parser.add_argument(
        "input_dir",
        type=str,
        help="Directory with CZI files.",
    )
    parser.add_argument(
        "output_dir",
        type=str,
        help="Directory for saving downsampled images.",
    )
    args = parser.parse_args()
    main(args.input_dir, args.output_dir)

import cv2
import numpy as np
import tqdm
import argparse


# This project tries to take any file and encode it into a valid video file
# that can be played by a video player. The idea is to use pixels to encode
# one of 16 colors, which will represent a hexadecimal character.

# This aproach should give us 1920 * 1080 * 4  bits of data, or 8,294,400 bits
# per frame.

# this aproach should also be resistant to compression, as the data is not read
# directly from the file bits, but from the color of the pixel. This means that
# you could (teorically) upload the video to youtube and download it again and
# the data should be intact.

# Colors are bgr, not rgb
HEX_TO_COLORS: dict[str, tuple[int, int, int]] = {
    "0": (0, 0, 0),  # black
    "1": (0, 0, 128),
    "2": (0, 128, 0),
    "3": (0, 128, 128),
    "4": (128, 0, 0),
    "5": (128, 0, 128),
    "6": (128, 128, 0),
    "7": (192, 192, 192),
    "8": (128, 128, 128),
    "9": (0, 0, 255),
    "a": (0, 255, 0),
    "b": (0, 255, 255),
    "c": (255, 0, 0),
    "d": (255, 0, 255),
    "e": (255, 255, 0),
    "f": (255, 255, 255),  # white
    "eof": (128, 192, 128)  # end of file
}

COLORS_TO_HEX: dict[tuple[int, int, int], str] = {
    (0, 0, 0): "0",  # black
    (0, 0, 128): "1",
    (0, 128, 0): "2",
    (0, 128, 128): "3",
    (128, 0, 0): "4",
    (128, 0, 128): "5",
    (128, 128, 0): "6",
    (192, 192, 192): "7",
    (128, 128, 128): "8",
    (0, 0, 255): "9",
    (0, 255, 0): "a",
    (0, 255, 255): "b",
    (255, 0, 0): "c",
    (255, 0, 255): "d",
    (255, 255, 0): "e",
    (255, 255, 255): "f",  # white
    (128, 192, 128): "eof"  # end of file
}


height = 1080
width = 1920
fps = 24


def encode(path: str, out: str) -> None:
    blank_frame = np.zeros((height, width, 3), np.uint8)
    with open(path, 'rb') as f:
        in_bytes = f.read()

    # add f9 ac hex to the start of the file
    in_bytes = b'\xf9\xac' + in_bytes

    for i in range(len(in_bytes)):
        hex_string = hex(in_bytes[i])[2:].zfill(2)

        color_1 = HEX_TO_COLORS[hex_string[0]]
        color_2 = HEX_TO_COLORS[hex_string[1]]

        x1 = (i * 2) % width  # (0, 1919)
        x2 = x1 + 1  # (0, 1919)

        y1 = y2 = (i * 2) // width

        blank_frame[y1][x1] = color_1
        blank_frame[y2][x2] = color_2

        if i == len(in_bytes) - 1 or (x2 == 1919 and y2 == 1079):
            x = (x1 + 1) % width
            y = ((i + 1) * 2) // width

            # EOF
            blank_frame[y][x] = HEX_TO_COLORS["eof"]
            cv2.imwrite(out, blank_frame)
            blank_frame = np.zeros((height, width, 3), np.uint8)


# given a fram of shape (height, width, 3), return the average color
# (b g r)
def average_color(frame: np.ndarray):
    return np.average(np.average(frame, axis=0), axis=0)


# given a pixel, return true if it is close to enough to zero
def close_to_zero(pixel: np.ndarray):
    return np.all(pixel < 1e-2)


def decode(path: str, out: str) -> None:
    # open png file
    image = cv2.imread(path)

    # get the first 4 pixels
    first_4_pixels = image[0][0:4]

    first_4_string = ""
    for pixel in first_4_pixels:
        first_4_string += COLORS_TO_HEX[tuple(pixel)]

    # get the rest of the pixels
    # we start at 2 because we already read the first 4 pixels
    full_hex = ""

    for i in tqdm.tqdm(range(2, height * width)):
        x1 = (i * 2) % width
        x2 = x1 + 1

        y1 = y2 = (i * 2) // width

        color_1 = image[y1][x1]
        color_2 = image[y2][x2]

        hex_string = COLORS_TO_HEX[tuple(color_1)] + \
            COLORS_TO_HEX[tuple(color_2)]

        if hex_string.endswith("eof") or hex_string.startswith("eof"):
            break

        full_hex += hex_string

    # remove the f9ac from the end of the file
    full_hex = full_hex[:-4]

    # convert the hex string to bytes
    full_bytes = bytes.fromhex(full_hex)

    # write the bytes to the file
    with open(out, 'wb') as f:
        f.write(full_bytes)


def main():
    parser = argparse.ArgumentParser()

    # mode (encode/decode)
    parser.add_argument("mode", type=str, choices=[
                        "encode", "decode"], default="encode")

    # input file
    parser.add_argument("input", type=str)

    # output file
    parser.add_argument("output", type=str)

    args = parser.parse_args()

    if args.mode == "encode":
        encode(args.input, args.output)
    else:
        decode(args.input, args.output)


if __name__ == "__main__":
    main()

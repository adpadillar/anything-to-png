# Anything to png

This is a fun little project that encodes any file into a png image. It's not very efficient, but it works.

The way it works is by taking the binary data of the files and converting each hexadecimel character into a pixel. We can therefore store 1920 x 1080 x 4 = 8 294 400 bits of data in a single image.

## Usage

To encode a file, run the following command:

```bash
python main.py encode <input_file> <output_file>.png
```

To decode a file, run the following command:

```bash
python main.py decode <input_file>.png <output_file>
```

## Examples

Taking the file `bee-movie-script.md` as an example, we can encode it into a png image:

```bash
python main.py encode bee-movie-script.md bee-movie-script.png
```

We get the following image:

!["bee-movie-script.png"](bee-movie.png)

We can then decode the image back into the original file:

```bash
python main.py decode bee-movie.png bee-movie-script.md
```

## Next steps

I want to make this more useful by converting the output from images to videos, the objective is that they can actually withstand compression and be uploaded to YouTube.

## Inspiration

This project was inspired by the following videos

- https://www.youtube.com/watch?v=c_arQ-6ElYI
- https://www.youtube.com/watch?v=wsvnUlfUKlY

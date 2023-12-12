# Synthetic Handwriting Document Images Generator

## 1. Generate synthetic background (Jiaxin, Richa)

## 2. Character modelling with deformations (Qinglin, Chenrui)

## 3. Generate text and ink textures (Francesco)

## 4. Generate entire pages (Flavien)

To run the code execute the following command:
```bash
python main.py [--args]
```

By default, (without any arguments) the code will generate 20 new pages, a new TSV file and remove any previously generated files.

Possible arguments are:
- `--nb X`: This will lead to the generation of X new pages. X is a positive integer, default is 20. The argument is optional.
- `--overwrite [0,1]`: This will define if the newly generated images replace previous ones or are added in addition, including the TSV file. Input value is 0 or 1, default is 1/True. The argument is optional.

The generated files (pages images and TSV) are placed in the '/out/' folder.

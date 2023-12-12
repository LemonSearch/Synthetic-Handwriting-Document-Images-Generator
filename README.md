# Synthetic Handwriting Document Images Generator

## 1. Generate synthetic background (Jiaxin, Richa)

## 2. Character modelling with deformations (Qinglin, Chenrui)

## 3. Generate text and ink textures (Francesco)

## 4. Generate entire pages (Flavien)

To get the statistics about the dataset run the following code:
```bash
python preprocessing.py
```
This only needs to be run once for a dataset. Any change to the dataset would require new measurements. 

The `layout.py` file is used during the page generation by `main.py`

## Requirements and Code execution
 - Numpy
 - Pillow
 - python-opencv
 - Pyyaml


To run the code execute the following command:
```bash
python main.py [--args]
```

By default, (without any arguments) the code will generate 20 new pages, a new TSV file and remove any previously generated files.

Possible arguments are:
- `--nb X`: This will lead to the generation of X new pages. X is a positive integer, default is 20. The argument is optional.
- `--overwrite [0,1]`: This will define if the newly generated images replace previous ones or are added in addition, including the TSV file. Input value is 0 or 1, default is 1/True. The argument is optional.

The generated files (pages images and TSV) are placed in the '/out/' folder.

On a Lenovo L390 Yoga (plugged in) running Ubuntu 22.04, Intel® Core™ i5-8265U CPU @ 1.60GHz × 8, Mesa Intel® UHD Graphics 620 (WHL GT2), 16GB RAM and SSD NVMe, the runtime is about `1 minute` per pages.

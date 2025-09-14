#!/usr/bin/env python3
"""Append visualization cells to `week02_notebook.ipynb` using nbformat.

This script appends a markdown cell and a code cell that displays the generated SVG/PNG files.
"""
import nbformat
from nbformat.v4 import new_markdown_cell, new_code_cell
import os

NB = 'week02_notebook.ipynb'

def main():
    if not os.path.exists(NB):
        print('Notebook not found:', NB)
        return
    nb = nbformat.read(NB, as_version=4)
    md = new_markdown_cell('''### Visualizations: Monthly Wind & Rain\n\nThe plots below are generated from the processed files: `monthly_wind_rain.svg` / `monthly_wind_rain.png` and the summary `7.svg`. If these files are missing, run the scripts in `scripts/` to regenerate them.''')
    code = new_code_cell('''from IPython.display import SVG, Image, display\n\nif os.path.exists('monthly_wind_rain.svg'):\n    display(SVG('monthly_wind_rain.svg'))\nelse:\n    print('monthly_wind_rain.svg not found')\n\nif os.path.exists('monthly_wind_rain.png'):\n    display(Image('monthly_wind_rain.png'))\nelse:\n    print('monthly_wind_rain.png not found')\n\nif os.path.exists('7.svg'):\n    display(SVG('7.svg'))\nelse:\n    print('7.svg not found')''')
    nb['cells'].append(md)
    nb['cells'].append(code)
    nbformat.write(nb, NB)
    print('Appended visualization cells to', NB)

if __name__ == '__main__':
    main()

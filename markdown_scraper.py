"""
Functions for scrapping markdown header cells from jupyter notebooks
"""

import json
import os
import nbformat as nbf

def scrape_markdown(filelist=None, exclude=None,
                    headers_only=False, skip_cells=0):
    """
    pulls all the markdown cells from jupyter notebooks

    arguments:
        filelist: list of notebooks to scrape
        exclude: list of notebooks to skip
        headers_only: when true, skip plain markdown
        skip_cells: skips a number of markdown cells at the beginning of a file
    """
    if filelist != None:
        for file in filelist:
            if not file.endswith('.ipynb'):
                raise ValueError('filenames must end with .ipynb')

    if filelist is None:
        filelist = []
        for file in os.listdir():
            if file.endswith('.ipynb'):
                filelist.append(file)
        if exclude is not None:
            for file in exclude:
                if not file.endswith('.ipynb'):
                    raise ValueError('filenames must end with .ipynb')
                try:
                    filelist.remove(file)
                except ValueError:
                    pass

    markdown_cells = []

    for file in filelist:
        with open(file, 'r') as f:
            json_load = json.load(f)

        cell = nbf.v4.new_markdown_cell('# ' + file)
        markdown_cells.append(cell)

        for i, cell in enumerate(json_load['cells']):
            if cell['cell_type'] == 'markdown'and i > skip_cells-1:
                if cell['source'] != []:
                    if '#' in cell['source'][0]:
                        markdown = '#' + cell['source'][0]
                        cell = nbf.v4.new_markdown_cell(markdown)
                        markdown_cells.append(cell)
                    elif not headers_only:
                        markdown = cell['source'][0]
                        cell = nbf.v4.new_markdown_cell(markdown)
                        markdown_cells.append(cell)
    return markdown_cells


def gen_notebook(markdown_cells, filename='toc.ipynb'):
    """
    generates a jupyter notebook comprised of the input markdown cells

    arguments:
        markdown_cells: list of markdown cells to write
        filename: filename for the output notebook
    """
    if not filename.endswith('.ipynb'):
        raise ValueError('filenames must end with .ipynb')

    nb = nbf.v4.new_notebook()
    nb['cells'] = markdown_cells

    with open(filename, 'w') as f:
        nbf.write(nb, f)

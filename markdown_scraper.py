"""
Functions for scrapping markdown header cells from jupyter notebooks
"""

import json
import os
from IPython.display import display, Markdown
import nbformat as nbf

def scrape_markdown(filelist=None, exclude=[],
                    headers_only=False, skip_cells=0):
    """
    text

    Arguments:
        arg:
    """
    if filelist != None:
        for file in filelist:
            if not file.endswith('.ipynb'):
                raise ValueError('filenames must end with .ipynb')

    if filelist == None:
        filelist = []
        for file in os.listdir():
            if file.endswith('.ipynb'):
                filelist.append(file)

        for file in exclude:
            if not file.endswith('.ipynb'):
                raise ValueError('filenames must end with .ipynb')

            filelist.remove(file)

    markdown_cells = []

    for file in filelist:
        with open(file,'r') as f:
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
    text

    Arguments:
        arg:
    """
    if not filename.endswith('.ipynb'):
        raise ValueError('filenames must end with .ipynb')

    nb = nbf.v4.new_notebook()
    nb['cells'] = markdown_cells

    with open(filename, 'w') as f:
        nbf.write(nb, f)

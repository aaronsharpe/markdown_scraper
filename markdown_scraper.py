"""
Functions for scraping markdown header cells from jupyter notebooks.
"""

import json
import argparse
import nbformat as nbf


def scrape_markdown(files, headers_only=False, skip_cells=0):
    """
    Pulls all the markdown cells from jupyter notebooks.

    Arguments:
        files: notebooks to scrape
        headers_only: when true, skip plain markdown
        skip_cells: skips a number of markdown cells at the beginning of a file
    """
    markdown_cells = []

    for file in list(files):
        with open(file) as f:
            notebook = json.load(f)
        filename_cell = nbf.v4.new_markdown_cell('# ' + file)
        markdown_cells.append(filename_cell)

        for i, cell in enumerate(notebook['cells']):
            if cell['cell_type'] == 'markdown' and i > skip_cells-1:
                if len(cell['source']) != 0:
                    if cell['source'][0][0] == '#':
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
    Generates a jupyter notebook comprised of the input markdown cells.

    Arguments:
        markdown_cells: list of markdown cells to write
        filename: filename for the output notebook
    """

    nb = nbf.v4.new_notebook()
    nb['cells'] = markdown_cells

    with open(filename, 'w') as f:
        nbf.write(nb, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', help='files to scrape')
    parser.add_argument('--headers_only', type=bool, default=False,
                        help='omit regular markdown cells')
    parser.add_argument('-s', '--skip_cells', type=int, default=0,
                        help='number of cells to skip at start of notebook')
    parser.add_argument('-o', default='toc.ipynb', help='output filename')
    args = parser.parse_args()

    markdown_cells = scrape_markdown(args.files,
                                     headers_only=args.headers_only,
                                     skip_cells=args.skip_cells)
    gen_notebook(markdown_cells, filename=args.o)

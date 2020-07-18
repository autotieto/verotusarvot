#!env python

import os
import glob
import re
import csv
import datetime
import xlrd3 as xlrd
import pandas as pd
from functools import partial


RE_YEAR = re.compile('([0-9]{4})', re.M)
COLS = ['make', 'model', 'specification', 'modifier', 'decision_date', 'use_date', 'driven_1000', 'value_eur', 'tax_eur']
DTYPES = {
    'make': 'category',
    'model': 'category',
    'specification': 'category',
    'modifier': 'category',
    'decision_date': 'datetime64',
    'use_date': 'datetime64',
    'driven_1000': 'float32',
    'value_eur': 'float32',
    'tax_eur': 'float32',
}

DEFAULT_STR, DEFAULT_INT, DEFAULT_FLOAT = '', 0, -0.0

def conv(p, n, t, d):
    v = p(n).value
    if v == None or v == '' or v == ' ':
        return d
    else:
        return t(v)

def main():
    table = []
    for fn in sorted(glob.glob('data/*.xls'), key=os.path.basename):
        print(fn)
        book = xlrd.open_workbook(fn)
        for sh in book.sheets():
            if sh.ncols == 0 and sh.nrows == 0:
                continue
            malli_cell = sh.cell(0, 1)
            if malli_cell.value != 'Malli':
                continue
            for rn in range(2, sh.nrows):
                p = partial(sh.cell, rn)
                row = [
                    conv(p, 0, str, DEFAULT_STR),
                    conv(p, 1, str, DEFAULT_STR),
                    conv(p, 2, str, DEFAULT_STR),
                    conv(p, 3, str, DEFAULT_STR),
                    conv(p, 4, int, DEFAULT_INT),
                    conv(p, 5, int, DEFAULT_INT),
                    conv(p, 6, int, DEFAULT_INT),
                    conv(p, 7, float, DEFAULT_FLOAT),
                    conv(p, 8, float, DEFAULT_FLOAT),
                ]
                table.append(row)

    df = pd.DataFrame(data=table, columns=COLS, dtype=str)
    for k, v in DTYPES.items():
        df[k] = df[k].astype(v)

    df.to_parquet('site/dump.parquet')
    df.to_csv('site/dump.csv.bz2', index=False, compression='bz2')

if __name__=='__main__':
    main()

import os
import glob
import re
import xlrd
import polars as pl
from functools import partial


RE_YEAR = re.compile('([0-9]{4})', re.M)
DTYPES = {
    'make': pl.Categorical,
    'model': pl.Categorical,
    'specification': pl.Categorical,
    'modifier': pl.Categorical,
    'decision_date': pl.String,
    'use_date': pl.String,
    'driven_1000': pl.Float32,
    'value_eur': pl.Float32,
    'tax_eur': pl.Float32,
}

DEFAULT_STR, DEFAULT_INT, DEFAULT_FLOAT = '', 0, -0.0

def conv(p, n, t, d):
    v = p(n).value
    if v is None or v == '' or v == ' ':
        return d
    else:
        return t(v)


def conv2(cell, t, d):
    v = cell.value
    if v is None or v == '' or v == ' ':
        return d
    else:
        return t(v)


def conv_new_specification(row):
    return ''


def transfer_normal_sheet(sh, table):
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


def transfer_2021_feb_sheet(sh, table):
    for rn in range(2, sh.nrows):
        row = sh.row(rn)
        if row[0].ctype == xlrd.XL_CELL_EMPTY:
            continue
        item = [
            conv2(row[0], str, DEFAULT_STR),
            conv2(row[1], str, DEFAULT_STR),
            conv_new_specification(row),
            '',
            conv2(row[10], str, DEFAULT_STR),
            conv2(row[11], str, DEFAULT_STR),
            conv2(row[12], int, DEFAULT_INT),
            conv2(row[13], float, DEFAULT_FLOAT),
            conv2(row[15], float, DEFAULT_FLOAT),
        ]
        table.append(item)


def main():
    table = []
    for fn in sorted(glob.glob('data/car_taxes*.xls'), key=os.path.basename):
        print(fn)
        book = xlrd.open_workbook(fn)
        for sh in book.sheets():
            if (sh.ncols == 0 and sh.nrows == 0) or sh.cell(0, 1).value != 'Malli':
                continue
            elif sh.cell(0, 2).value == 'Cm3':
                transfer_2021_feb_sheet(sh, table)
            else:
                transfer_normal_sheet(sh, table)

    df = pl.DataFrame(data=table, schema=DTYPES, orient='row')
    df = df.with_columns(
        pl.col("decision_date").str.to_date(format="%Y%m%d"),
        pl.col("use_date").str.to_date(format="%Y%m%d"),
    )

    print(df)

    df.write_parquet('./site/verotusarvot.parquet', compression='zstd')

if __name__=='__main__':
    main()

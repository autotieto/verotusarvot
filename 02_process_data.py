import os
import glob
import re
import pyexcel
import polars as pl


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

DEFAULT_STR, DEFAULT_INT, DEFAULT_FLOAT, DEFAULT_DATE = '', 0, -0.0, '9999-12-31'


def convert(value, transformer, default):
    if value is None or value == '' or value == ' ':
        return default
    else:
        return transformer(value)


def transfer_normal_sheet(sheet: pyexcel.Sheet, table: list[list]):
    n = 2 if sheet[1, 0] == 'Märke' else 1
    for row in list(sheet)[n:]:
        if set(row) == {""} or row[0]== '':
            continue
        item = [
            convert(row[0], str, DEFAULT_STR),
            convert(row[1], str, DEFAULT_STR),
            convert(row[2], str, DEFAULT_STR),
            convert(row[3], str, DEFAULT_STR),
            convert(row[4], str, DEFAULT_DATE),
            convert(row[5], str, DEFAULT_DATE),
            convert(row[6], int, DEFAULT_INT),
            convert(row[7], float, DEFAULT_FLOAT),
            convert(row[8], float, DEFAULT_FLOAT),
        ]
        table.append(item)


def transfer_2021_feb_sheet(sheet: pyexcel.Sheet, table: list[list]):
    n = 2 if sheet[1, 0] == 'Märke' else 1
    for row in list(sheet)[n:]:
        if set(row) == {""} or row[0]== '':
            continue
        item = [
            convert(row[0], str, DEFAULT_STR),
            convert(row[1], str, DEFAULT_STR),
            '',
            '',
            convert(row[10], str, DEFAULT_DATE),
            convert(row[11], str, DEFAULT_DATE),
            convert(row[12], int, DEFAULT_INT),
            convert(row[13], float, DEFAULT_FLOAT),
            convert(row[15], float, DEFAULT_FLOAT),
        ]
        table.append(item)


def main():
    table = []
    for fn in sorted(glob.glob('data/car_taxes*.xls'), key=os.path.basename):
        print(f'procesing {fn}')
        book = pyexcel.get_book(file_name = fn)
        for sheet in list(book)[1:]:
            if len(sheet) == 0 or sheet[0, 1] != 'Malli':
                continue
            elif sheet[0, 2] == 'Cm3':
                transfer_2021_feb_sheet(sheet, table)
            else:
                transfer_normal_sheet(sheet, table)

    df = pl.DataFrame(data=table, schema=DTYPES, orient='row')
    df = df.with_columns(
        pl.col("decision_date").str.to_date(format="%Y%m%d"),
        pl.col("use_date").str.to_date(format="%Y%m%d"),
    )

    print(df)

    df.write_parquet('./site/verotusarvot.parquet', compression_level=19)

if __name__=='__main__':
    main()

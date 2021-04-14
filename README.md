# Taulukoita ajoneuvojen sovelletuista verotusarvoista

Data: https://www.vero.fi/henkiloasiakkaat/auto/autoverotus/autoveron_maara/taulukoita_ajoneuvojen_sovelletuista_ve/

```sh
pip install --user --upgrade pandas pyarrow
```

```python
import pandas as pd
df = pd.read_parquet('https://autotieto.github.io/verotusarvot/verotusarvot.parquet')
print(df.dtypes)
print(df.describe())
print(df)
```

```text
make                   category
model                  category
specification          category
modifier               category
decision_date    datetime64[ns]
use_date         datetime64[ns]
driven_1000             float32
value_eur               float32
tax_eur                 float32
dtype: object

         driven_1000      value_eur        tax_eur
count  285075.000000  285075.000000  285075.000000
mean      122.860947   20096.556641    4908.002930
std        97.222397   18417.396484    5830.296875
min         0.000000       0.000000       0.000000
25%        64.000000    8510.000000    1853.974976
50%       119.000000   17004.550781    3678.979980
75%       169.000000   25904.150391    6153.480225
max      9500.000000  559372.000000  275211.031250

              make                model              specification modifier decision_date   use_date  driven_1000     value_eur      tax_eur
0       ALFA ROMEO                  156               2.0 4D 114KW        N    2011-01-19 2000-04-26        200.0   2310.000000   651.419983
1       ALFA ROMEO                  156       2.0 5D STW AUT 122KW        N    2011-01-11 2002-11-01        181.0   3545.399902  1088.430054
2       ALFA ROMEO                  159             1.9 D 4D 110KW        N    2011-01-12 2006-08-24         99.0  13062.000000  3174.060059
3       ALFA ROMEO                  159               2.2 4D 136KW        N    2011-01-19 2007-08-29        122.0  13315.000000  3741.510010
4       ALFA ROMEO                  159             2.4 D 4D 154KW        N    2011-01-05 2007-08-13         99.0  16267.349609  4343.379883
...            ...                  ...                        ...      ...           ...        ...          ...           ...          ...
285070       VOLVO                 XC90  2.4 D 5D MA 4WD AUT 147KW             2020-12-09 2012-08-30        215.0  16750.900391  6298.330078
285071       VOLVO                 XC90      2.4 D 5D MA AUT 120KW             2020-12-01 2013-03-20        246.0  14473.750000  5369.759766
285072       VOLVO  XC90 T8 TWIN ENGINE    2.0 5D MA 4WD AUT 223KW             2020-12-07 2019-01-31          9.0  73033.648438  4016.850098
285073       VOLVO  XC90 T8 TWIN ENGINE    2.0 5D MA 4WD AUT 223KW             2020-12-21 2019-08-27         19.0  72815.148438  3640.750000
285074       VOLVO             p1800 ES            2.0 2D STW 93KW             2020-12-16 1973-10-03          0.0    128.000000    23.680000

[285075 rows x 9 columns]
```

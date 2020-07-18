# Taulukoita ajoneuvojen sovelletuista verotusarvoista

Data: https://www.vero.fi/henkiloasiakkaat/auto/autoverotus/autoveron_maara/taulukoita_ajoneuvojen_sovelletuista_ve/

```text
$ venv/bin/python
Python 3.8.2 (default, Apr 27 2020, 15:53:34) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pandas as pd
>>> df = pd.read_parquet('https://autotieto.github.io/verotusarvot/dump.parquet')
>>> df.dtypes
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
>>> df
              make model              specification modifier decision_date   use_date  driven_1000     value_eur      tax_eur
0       ALFA ROMEO   156               2.0 4D 114KW        N    2011-01-19 2000-04-26        200.0   2310.000000   651.419983
1       ALFA ROMEO   156       2.0 5D STW AUT 122KW        N    2011-01-11 2002-11-01        181.0   3545.399902  1088.430054
2       ALFA ROMEO   159             1.9 D 4D 110KW        N    2011-01-12 2006-08-24         99.0  13062.000000  3174.060059
3       ALFA ROMEO   159               2.2 4D 136KW        N    2011-01-19 2007-08-29        122.0  13315.000000  3741.510010
4       ALFA ROMEO   159             2.4 D 4D 154KW        N    2011-01-05 2007-08-13         99.0  16267.349609  4343.379883
...            ...   ...                        ...      ...           ...        ...          ...           ...          ...
261231       VOLVO  XC90  2.4 D 5D MA 4WD AUT 136KW             2020-06-12 2008-12-10        250.0   9074.000000  2395.530029
261232       VOLVO  XC90  2.4 D 5D MA 4WD AUT 136KW             2020-06-30 2010-01-22        208.0  13002.000000  4186.640137
261233       VOLVO  XC90  2.4 D 5D MA 4WD AUT 136KW             2020-06-01 2010-07-05        167.0  14955.400391  4815.629883
261234       VOLVO  XC90  2.4 D 5D MA 4WD AUT 147KW             2020-06-03 2011-06-23        105.0  20389.400391  6443.049805
261235       VOLVO  XC90    3.2 5D MA 4WD AUT 173KW             2020-06-24 2006-08-18        145.0  10093.000000  2725.110107

[261236 rows x 9 columns]
```

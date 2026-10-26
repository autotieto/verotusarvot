### Calamine

If you know about your sheets and headers beforehand...

```python
import polars as pl

def rename_cols(orig: str) -> str:
    cols = {
        'Merkki': 'brand',
        'Malli': 'model',
        'Cm3': 'displace_cm3',
        'Käyttövoima': 'fuel',
        'OvienLkm': 'doors',
        'Korimalli': 'chassis_type',
        'Vetotapa': 'traction_type',
        'Vaihteisto': 'shifter',
        'Kw': 'power_kw',
        'Yksilölliset ominaisuudet': 'unique_features',
        'Mallin tarkennin': 'model_specifier',
        'Kunto H=Huono N=Normaali Y=Hyvä': 'repair',
        'Käyttöönottopvä': 'use_date',
        'Ensirekisteröintipäivä': 'use_date',
        'Päätöspäivä': 'decision_date',
        'Ajokm/1000': 'driven_1000km',
        'Verotusarvo': 'tax_value',
        'Veroprosentti': 'tax_pct',
        'Autovero': 'car_tax',
    }
    if orig in cols:
        return cols[orig]
    else:
        return orig

df = (
    pl.concat(
        pl.read_excel(
            'data/car_taxes_2022.xls',
            engine='calamine',
            sheet_id=range(2, 14),
            drop_empty_rows=True,
            read_options={'skip_rows': 0},
        )
        .values()
    )
    .filter(pl.col("Merkki") != 'Märke')
    .rename(rename_cols)
    .cast({
        'driven_1000km': pl.UInt16,
        'displace_cm3': pl.UInt16,
        'brand': pl.Categorical,
        'model': pl.Categorical,
        'fuel': pl.Categorical,
        'chassis_type': pl.Categorical,
        'traction_type': pl.Categorical,
        'shifter': pl.Categorical,
    })
    .with_columns(
        pl.col("decision_date").str.to_date(format="%Y%m%d"),
        pl.col("use_date").str.to_date(format="%Y%m%d"),
    )
)
```

```text

```

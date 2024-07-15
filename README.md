# uspszipcode

USPS Zip Code from [USPS ZIP Codes by Area and District codes](https://postalpro.usps.com/ZIP_Locale_Detail)

## How this File is Generated?

The Excel file from the data source has three sheets (`ZIP_DETAIL`, `Unique_ZIP_DETAIL`, `Other`).
This file unifies the naming convention across these three sheets and add a new column `sheet` to identify where the row comes from. 
That's it. 

## How to Use

Use the `usps.csv` directly or run `python main.py` to download a new one from USPS.
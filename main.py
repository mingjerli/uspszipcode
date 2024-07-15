import logging
import datetime

import pandas as pd

DEFAULT_URL = "https://postalpro.usps.com/mnt/glusterfs/2024-07/ZIP_Locale_Detail.xls"

def _download_xls_sheets(ct=5):
    i = 0
    dfs = None
    file_date = datetime.datetime.now()
    while i<ct and dfs is None:
        year = str(file_date.year)
        month = str(file_date.month).zfill(2)
        url = f"https://postalpro.usps.com/mnt/glusterfs/{year}-{month}/ZIP_Locale_Detail.xls"
        try:
            dfs=pd.read_excel(url, engine="calamine", sheet_name=None)
            return dfs
        except:
            ct += 1
            file_date = file_date - datetime.timedelta(days=28) # Not perfect, but will iterate through all months

    logging.warning(f"Failed to download USPS ZIPCODE data after {ct} attempts. Use default url to download")
    url = DEFAULT_URL
    dfs=pd.read_excel(url, engine="calamine", sheet_name=None)
    return dfs

def get_usps_zipcode_data(save_path="usps.csv"):
    dfs = _download_xls_sheets()
    df = pd.concat([
        dfs['ZIP_DETAIL'].rename({
            'DELIVERY ZIPCODE': 'ZIP CODE',
        }, axis=1).assign(
            sheet='ZIP_DETAIL'
        ),
        dfs['Unique_ZIP_DETAIL'].assign(sheet='Unique_ZIP_DETAIL'),
        dfs['Other'].rename({
            'District Name': 'DISTRICT NAME', 
            'District': 'DISTRICT NO',
        }, axis=1).assign(sheet='Other'),
    ])
    df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")
    df.ZIP_CODE = df.ZIP_CODE.astype(str).str.zfill(5)
    df.PHYSICAL_ZIP = df.PHYSICAL_ZIP.fillna('').astype(str).str.split(".").str[0].str.zfill(5)
    df.PHYSICAL_ZIP[df.PHYSICAL_ZIP == '00000'] = ''
    df.PHYSICAL_ZIP_4 = df.PHYSICAL_ZIP_4.fillna('').astype(str).str.split(".").str[0]
    df.LEAD_FINANCE_NBR = df.LEAD_FINANCE_NBR.fillna('').astype(str).str.split(".").str[0]
    if save_path is not None:
        logging.info(f"Save USPS ZIPCODE data to {save_path}")
        df.to_csv(save_path, index=False)
    return df

if __name__ == "__main__":
    get_usps_zipcode_data()
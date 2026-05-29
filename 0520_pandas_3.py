import os
import sys

try:
    import pandas as pd
except ModuleNotFoundError:
    sys.exit(1)


def main():
    file_name = 'SuperMarket Analysis.csv'

    if not os.path.exists(file_name):
        return

    df = pd.read_csv(file_name)

    print(f"資料筆數: {df.shape[0]}")
    print(df.head(5))

    if 'Sales' not in df.columns and 'Total' in df.columns:
        df = df.rename(columns={'Total': 'Sales'})

    filter_condition = df['Branch'].str.startswith('A') & (df['Customer type'] == 'Member')
    filtered_df = df[filter_condition]

    analysis_df = filtered_df

    product_summary = analysis_df.groupby('Product line').agg(
        總銷售額=('Sales', 'sum'),
        平均評分=('Rating', 'mean')
    ).round(2).reset_index()

    product_summary = product_summary.rename(columns={'Product line': '產品線'})

    print(product_summary)

    city_gender_summary = analysis_df.groupby(['City', 'Gender']).agg(
        平均銷售額=('Sales', 'mean'),
        交易筆數=('Sales', 'count')
    ).round(2).reset_index()

    city_gender_summary = city_gender_summary.rename(columns={'City': '城市', 'Gender': '性別'})

    print(city_gender_summary)

    if not product_summary.empty:
        highest_idx = product_summary['總銷售額'].idxmax()
        highest_product = product_summary.loc[highest_idx, '產品線']
        highest_sales = product_summary.loc[highest_idx, '總銷售額']
        print(f"總銷售額最高的產品線: {highest_product} ({highest_sales})")

    output_file = '0520_pandas_3OK.CSV'
    product_summary.to_csv(output_file, index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    main()
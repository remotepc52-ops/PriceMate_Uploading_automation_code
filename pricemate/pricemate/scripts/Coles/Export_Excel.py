import pandas as pd
from config import *

def Export_Data(Website):

    # Retrieve data from MongoDB and load it into a DataFrame
    data = list(product_data.find().limit(1000000))
    df = pd.DataFrame(data)

    # Specify the columns you want to export
    columns_to_export = [
        "ProductURL",
        "ProductCode",
        "Name",
        "Price",
        "WasPrice",
        "RRP",
        "Offer_info",
        "per_unit_price",
        "Pack_size",
        "Barcode",
        "Category_Hierarchy",
        "Brand",
        "Promo_Type",
        "is_available"
    ]  # Example columns
    # columns_to_export = ["ProductURL", "ProductCode", "Name", "Price", "WasPrice",
    #                      "RRP",  "Offer_info",  "per_unit_price", "Pack_size", "Barcode",
    #                      "Category_Hierarchy", "Brand", "Promo_Type", "Variation_Data"]  # Example columns
    df = df[columns_to_export]

    # Insert Sr. No. column as the first column
    df.insert(0, '#', range(1, len(df) + 1))
    df.insert(1, 'Id', range(1, len(df) + 1))

    # Drop the MongoDB default '_id' column if it exists
    if '_id' in df.columns:
        df.drop('_id', axis=1, inplace=True)

    # Save DataFrame to Excel file
    excel_file_path = f'{excel_path}\\{Website}_{today}.xlsx'
    df.to_excel(excel_file_path, index=False, engine_kwargs={"options": {'strings_to_numbers': False, 'strings_to_urls': False}})
    print(f"Excel file saved to {excel_file_path}")

    # Save DataFrame to JSON file
    json_file_path = f'{excel_path}\\{Website}_{today}.json'
    df.to_json(json_file_path, orient='records', lines=True)
    print(f"JSON file saved to {json_file_path}")


if __name__ == '__main__':
    Export_Data(website)



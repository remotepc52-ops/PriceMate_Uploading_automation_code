import pandas as pd
from pymongo import MongoClient
import datetime
import os
from dateutil.relativedelta import relativedelta, MO

# first_monday_date = (datetime.datetime.today() + relativedelta(weekday=MO(0))).date()
Today1 = datetime.date.today()
today = Today1.strftime("%Y_%m_%d")

# MONGO_URI = "mongodb://localhost:27017/"  # Change this if needed
MONGO_URI = "mongodb://localhost:27017"  # Change this if needed
DATABASE_NAME = "pricemate_eshop_healthpost_nz"             # Replace with your DB name
COLLECTION_NAME = "Product_Data_2025_12_10"              # Replace with your collection name
# Export Settings
folder_path = fr"E:\\Projects\\Avhinandan\\sample_pf_price\{today}\Excel_Data"
os.makedirs(folder_path, exist_ok=True)  # <-- add this line
# Folder path to save files


def Export_Data(Website):
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    product_data = db[COLLECTION_NAME]

    # Retrieve data from MongoDB and load it into a DataFrame
    # change the retailer name
    data = list(product_data.find({"Status": "Done", "retailer_name":"healthpost-nz"}).limit(1000000))
    df = pd.DataFrame(data)

    # Specify the columns you want to export
    columns_to_export = [    "ProductURL",    "ProductCode",    "Name",    "Price",
                             "WasPrice",    "RRP",    "Offer_info",    "per_unit_price",
                             "Pack_size",    "Barcode",    "Category_Hierarchy",    "Brand",
                             "Promo_Type",    "is_available", "retailer"]

    #Sample For Blibli

    # columns_to_export = ["ProductURL", "ProductCode", "Name", "Price",
    #                      "WasPrice", "RRP", "Offer_info", "per_unit_price",
    #                      "Pack_size", "Barcode", "Category_Hierarchy", "Brand",
    #                      "Promo_Type", "is_available", "retailer"]

    df = df[columns_to_export]

    # Insert Sr. No. column as the first column
    df["per_unit_price"] = df["per_unit_price"].astype(str).str.strip()

    # Drop the MongoDB default '_id' column if it exists
    if '_id' in df.columns:
        df.drop('_id', axis=1, inplace=True)

    # Save DataFrame to Excel file
    excel_file_path = f'{folder_path}\\UNT_{Website}_{today}.xlsx'
    # df["ProductCode"]= df["ProductCode"].astype(str)
    df.to_excel(
    excel_file_path,
    index=False
)
    print(f"Excel file saved to {excel_file_path}")

    # # Save DataFrame to JSON file
    # csv_file_path = f'{folder_path}\\UNT_site-{Website}_{today}.csv'
    # df.to_csv(csv_file_path, index=False)
    # print(f"CSV file saved to {csv_file_path}")


if __name__ == '__main__':
    Website = "healthpost"  # Change this to your actual website name
    Export_Data(Website)

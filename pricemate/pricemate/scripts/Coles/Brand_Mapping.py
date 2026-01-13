def barcode_map_process(product_table):
    from pymongo import MongoClient

    # Step 1: Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["PriceMate_Coles"]

    # product_table = db["Product_Data_2025_04_28"]
    barcode_table = db["brand_mapping_data"]

    # Step 2: Create a lookup dictionary from the barcode_table
    barcode_map = {
        doc["coles_code"]: doc["barcode"]
        for doc in barcode_table.find({}, {"_id": 0, "coles_code": 1, "barcode": 1})
    }

    # Step 3: Update product_table with barcode info
    for product in product_table.find({}, {"_id": 1, "ProductCode": 1}):
        product_code = product.get("ProductCode")
        barcode = barcode_map.get(product_code)

        if barcode and '-' not in barcode:
            product_table.update_one(
                {"_id": product["_id"]},
                {"$set": {"Barcode": barcode}}
            )

    print("Barcodes mapped successfully.")

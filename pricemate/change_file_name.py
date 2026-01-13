import os

def rename_shopee_domain(folder="."):
    """
    Renames files from:
      shopee.id_xxx → shopee.co.id_xxx
    Keeps the rest of the filename the same.
    """
    for filename in os.listdir(folder):
        old_path = os.path.join(folder, filename)
        if not os.path.isfile(old_path):
            continue  # skip folders

        if filename.startswith("shopee.id_"):
            new_name = filename.replace("shopee.id_", "shopee.co.id_", 1)
            new_path = os.path.join(folder, new_name)
            print(f"Renaming: {filename} → {new_name}")
            os.rename(old_path, new_path)

if __name__ == "__main__":
    # rename_shopee_domain("E:/Data/Crawl_Data_Collection/PriceMate/shopee_watson/2025_11_08/HTML_Files")  # current directory
    rename_shopee_domain("E:/Data/Crawl_Data_Collection/PriceMate/shopee_supermarket/2025_11_08/HTML_Files")  # current directory

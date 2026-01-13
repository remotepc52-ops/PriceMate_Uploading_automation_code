import pandas as pd
import requests
import datetime
from pymongo import MongoClient
from tabulate import tabulate

# === Step 1: Setup Dates ===
today_dt = datetime.date.today()
yesterday_dt = today_dt - datetime.timedelta(days=1)

today_str = today_dt.strftime("%Y_%m_%d")
yesterday_str = yesterday_dt.strftime("%Y_%m_%d")

today_display = today_dt.strftime("%Y-%m-%d")
yesterday_display = yesterday_dt.strftime("%Y-%m-%d")

print(f"📅 Today: {today_display}, Yesterday: {yesterday_display}\n")

# === Step 2: Fetch Planned Jobs ===
url = (
    f"https://cfuzczvkhrhdztwbcttj.supabase.co/functions/v1/get-planned-jobs?start_date={yesterday_display}T16%3A00%3A00.000Z&end_date={today_display}T15%3A59%3A59.999Z&limit=500"
)
headers = {
    "Cookie": "__cf_bm=ubvSLm0muChe1KteC6bdmK8rG71EYhFTKUV4ji6NPyU-1761569822.9497013-1.0.1.1-iPk.ZHoVOX.KzPBzGXxd4EfC1GrEhhD4j7nPoKRvLvRXeNpn0P_ZaQNM4wOLP42gia3w2.hL4.rvn3PdgdwE5lk0QbJXmciFWo3mlOGM22jcUUiDf590.y7O1a3Xuh6v"
}

print("🌐 Fetching planned jobs from Supabase...\n")
response = requests.get(url, headers=headers)
data = response.json()
jobs_data = data.get("data", {}).get("jobs", [])

rows = []
for jb in jobs_data:
    try:
        retailer_name = jb.get("source", {}).get("retailers", {}).get("code")
        job_url = jb.get("source", {}).get("url")
        frequency_type = jb.get("frequency_type")
        day_name = jb.get("day_of_week_name")
        source_type = jb.get("source", {}).get("source_type")
        time_singapor = jb.get("scheduled_at")

        retailer_name = retailer_name.replace("-", "_").lower()

        if retailer_name == "amazon_fresh_sg":
            retailer_name = "amazon_sg"
        elif retailer_name == "wizard_au":
            retailer_name = "wizardpharmacy_au"
        elif retailer_name == "redmart-sg":
            retailer_name = "lazada_redmart_sg"

        rows.append({
            "retailer_name": retailer_name,
            "url": job_url,
            "frequency_type": frequency_type,
            "day_name": day_name,
            "source_type": source_type,
            "time": time_singapor,
            "status": "Pending"
        })
    except Exception as e:
        print("⚠️ Error parsing job:", e)

if not rows:
    print("⚠️ No planned jobs found. Exiting...")
    exit()

df = pd.DataFrame(rows)
df = df[df["source_type"].str.lower() == "eshop"]

if df.empty:
    print("⚠️ No 'eshop' retailers found. Exiting...\n")
    exit()

print(f"🛒 Total 'eshop' retailers to process: {df['retailer_name'].nunique()}\n")

# === Step 3: MongoDB Connection ===
mongo_uri = "mongodb://192.168.1.52:27017"
client = MongoClient(mongo_uri)
all_dbs = client.list_database_names()
all_dbs_lower = {db.lower(): db for db in all_dbs}  # lowercase mapping for safe matching

# === Step 4: Retailer mapping ===
retailer_to_db = {
    "amazon_fresh_sg": "amazon_sg",
    "wizard_au": "wizardpharmacy_au",
    "redmart_sg": "lazada_redmart_sg",
}

# === Step 5: Compare Mongo Collections ===
print("🔍 Checking MongoDB collections for each 'eshop' retailer...\n")
result_rows = []

for retailer in df["retailer_name"].unique():
    if not retailer or str(retailer).lower() == "nan":
        continue

    # First try mapping
    db_name_lookup = retailer_to_db.get(retailer)
    db_name = None

    if db_name_lookup and db_name_lookup.lower() in all_dbs_lower:
        db_name = all_dbs_lower[db_name_lookup.lower()]
    else:
        # fallback: endswith match
        matches = [db for db in all_dbs if db.lower().endswith(retailer)]
        if matches:
            db_name = matches[0]

    if not db_name:
        print(f"⚠️ {retailer:25s} → No matching database found")
        result_rows.append({
            "Retailer": retailer,
            "Prev Date": None,
            "Prev Done": 0,
            "Prev Pending": 0,
            "Today Done": 0,
            "Today Pending": 0,
            "Diff": 0,
            "Not Found": "All"
        })
        continue

    db = client[db_name]

    # Get collections
    collections = [col for col in db.list_collection_names() if col.startswith("Product_Data_")]
    if not collections:
        result_rows.append({
            "Retailer": retailer,
            "Prev Date": "❌ Not Found",
            "Prev Done": 0,
            "Prev Pending": 0,
            "Today Done": 0,
            "Today Pending": 0,
            "Diff": 0,
            "Not Found": "No product data"
        })
        continue

    # Find available dates
    available_dates = []
    for col in collections:
        try:
            date_str = col.replace("Product_Data_", "")
            parsed = datetime.datetime.strptime(date_str, "%Y_%m_%d").date()
            available_dates.append(parsed)
        except Exception:
            pass

    if not available_dates:
        result_rows.append({
            "Retailer": retailer,
            "Prev Date": "❌ Parse Err",
            "Prev Done": 0,
            "Prev Pending": 0,
            "Today Done": 0,
            "Today Pending": 0,
            "Diff": 0,
            "Not Found": "No valid date collections"
        })
        continue

    available_dates.sort()
    last_date = available_dates[-1] if available_dates[-1] < today_dt else available_dates[-2] if len(
        available_dates) > 1 else None

    if not last_date:
        result_rows.append({
            "Retailer": retailer,
            "Prev Date": "⚠️ Only Today Found",
            "Prev Done": 0,
            "Prev Pending": 0,
            "Today Done": 0,
            "Today Pending": 0,
            "Diff": 0,
            "Not Found": "No previous data"
        })
        continue

    prev_col = f"Product_Data_{last_date.strftime('%Y_%m_%d')}"
    today_col = f"Product_Data_{today_str}"

    prev_done = prev_pending = today_done = today_pending = not_found = 0

    if prev_col in db.list_collection_names():
        prev_done = db[prev_col].count_documents({"Status": "Done"})
        prev_pending = db[prev_col].count_documents({"Status": {"$ne": "Done"}})
        not_found = db[prev_col].count_documents({"Status": "Not Found"})

    if today_col in db.list_collection_names():
        today_done = db[today_col].count_documents({"Status": "Done"})
        today_pending = db[today_col].count_documents({"Status": {"$ne": "Done"}})
        not_found += db[today_col].count_documents({"Status": "Not Found"})

    diff = today_done - prev_done

    result_rows.append({
        "Retailer": retailer,
        "Prev Date": last_date.strftime("%Y-%m-%d"),
        "Prev Done": prev_done,
        "Prev Pending": prev_pending,
        "Today Done": today_done,
        "Today Pending": today_pending,
        "Diff": diff,
        "Not Found": not_found
    })

client.close()

# === Step 6: Print Summary Table ===
summary_df = pd.DataFrame(result_rows)
print("\n📊 MongoDB Summary (Done / Pending / Not Found Comparison)\n")
print(tabulate(summary_df, headers='keys', tablefmt='grid', showindex=False))

# import pandas as pd
# import requests
# import datetime
# from pymongo import MongoClient
# from tabulate import tabulate
# import os
#
# # === Step 1: Setup Dates ===
# today_dt = datetime.date.today()
# yesterday_dt = today_dt - datetime.timedelta(days=1)
#
# today_str = today_dt.strftime("%Y_%m_%d")
# yesterday_str = yesterday_dt.strftime("%Y_%m_%d")
#
# today_display = today_dt.strftime("%Y-%m-%d")
# yesterday_display = yesterday_dt.strftime("%Y-%m-%d")
#
# print(f"📅 Today: {today_display}, Yesterday: {yesterday_display}\n")
#
# # === Step 2: Fetch Planned Jobs ===
# url = (
#     f"https://cfuzczvkhrhdztwbcttj.supabase.co/functions/v1/get-planned-jobs?"
#     f"start_date={yesterday_display}T16%3A00%3A00.000Z&"
#     f"end_date={today_display}T15%3A59%3A59.999Z&limit=500"
# )
# headers = {
#     "Cookie": "__cf_bm=YOUR_COOKIE_HERE"
# }
#
# response = requests.get(url, headers=headers)
# data = response.json()
# jobs_data = data.get("data", {}).get("jobs", [])
#
# rows = []
# for jb in jobs_data:
#     try:
#         retailer_name = jb.get("source", {}).get("retailers", {}).get("code")
#         if retailer_name is None:
#             continue
#
#         # === Step 2a: Map special retailers to DB names ===
#         if retailer_name == "amazon_fresh_sg":
#             db_name_map = "amazon_sg"
#         elif retailer_name == "wizard_au":
#             db_name_map = "wizardpharmacy-au"
#         elif retailer_name == "redmart_sg":
#             db_name_map = "lazada_redmart_sg"
#         else:
#             db_name_map = retailer_name.replace("-", "_").lower()
#
#         rows.append({
#             "retailer_name": retailer_name,
#             "db_name": db_name_map,
#             "url": jb.get("source", {}).get("url"),
#             "frequency_type": jb.get("frequency_type"),
#             "day_name": jb.get("day_of_week_name"),
#             "source_type": jb.get("source", {}).get("source_type"),
#             "time": jb.get("scheduled_at"),
#             "status": "Pending"
#         })
#     except Exception as e:
#         print("⚠️ Error parsing job:", e)
#
# if not rows:
#     print("⚠️ No planned jobs found. Exiting...")
#     exit()
#
# df = pd.DataFrame(rows)
# df = df[df["source_type"].str.lower() == "eshop"]
#
# if df.empty:
#     print("⚠️ No 'eshop' retailers found. Exiting...\n")
#     exit()
#
# print(f"🛒 Total 'eshop' retailers to process: {df['retailer_name'].nunique()}\n")
#
# # === Step 3: MongoDB Connection ===
# mongo_uri = "mongodb://192.168.1.52:27017"
# client = MongoClient(mongo_uri)
# all_dbs = client.list_database_names()
#
# # === Step 4: Compare Mongo Collections ===
# result_rows = []
#
# for _, row in df.iterrows():
#     retailer = row["retailer_name"]
#     db_name = row["db_name"]
#
#     if db_name not in all_dbs:
#         print(f"⚠️ {retailer:25s} → No matching database found")
#         result_rows.append({
#             "Retailer": retailer,
#             "Prev Date": None,
#             "Prev Done": 0,
#             "Prev Pending": 0,
#             "Today Done": 0,
#             "Today Pending": 0,
#             "Diff": 0,
#             "Not Found": "All"
#         })
#         continue
#
#     db = client[db_name]
#     collections = [col for col in db.list_collection_names() if col.startswith("Product_Data_")]
#     if not collections:
#         result_rows.append({
#             "Retailer": retailer,
#             "Prev Date": "❌ Not Found",
#             "Prev Done": 0,
#             "Prev Pending": 0,
#             "Today Done": 0,
#             "Today Pending": 0,
#             "Diff": 0,
#             "Not Found": "No product data"
#         })
#         continue
#
#     available_dates = []
#     for col in collections:
#         try:
#             date_str = col.replace("Product_Data_", "")
#             parsed = datetime.datetime.strptime(date_str, "%Y_%m_%d").date()
#             available_dates.append(parsed)
#         except Exception:
#             pass
#
#     if not available_dates:
#         continue
#
#     available_dates.sort()
#     last_date = available_dates[-1] if available_dates[-1] < today_dt else available_dates[-2] if len(available_dates) > 1 else None
#     if not last_date:
#         result_rows.append({
#             "Retailer": retailer,
#             "Prev Date": "⚠️ Only Today Found",
#             "Prev Done": 0,
#             "Prev Pending": 0,
#             "Today Done": 0,
#             "Today Pending": 0,
#             "Diff": 0,
#             "Not Found": "No previous data"
#         })
#         continue
#
#     prev_col = f"Product_Data_{last_date.strftime('%Y_%m_%d')}"
#     today_col = f"Product_Data_{today_str}"
#
#     prev_done = prev_pending = today_done = today_pending = not_found = 0
#
#     if prev_col in db.list_collection_names():
#         prev_done = db[prev_col].count_documents({"Status": "Done"})
#         prev_pending = db[prev_col].count_documents({"Status": {"$ne": "Done"}})
#         not_found = db[prev_col].count_documents({"Status": "Not Found"})
#
#     if today_col in db.list_collection_names():
#         today_done = db[today_col].count_documents({"Status": "Done"})
#         today_pending = db[today_col].count_documents({"Status": {"$ne": "Done"}})
#         not_found += db[today_col].count_documents({"Status": "Not Found"})
#
#     diff = today_done - prev_done
#
#     result_rows.append({
#         "Retailer": retailer,
#         "Prev Date": last_date.strftime("%Y-%m-%d"),
#         "Prev Done": prev_done,
#         "Prev Pending": prev_pending,
#         "Today Done": today_done,
#         "Today Pending": today_pending,
#         "Diff": diff,
#         "Not Found": not_found
#     })
#
# client.close()
#
# # === Step 5: Save to Excel ===
# daily_jobs = r"E:\Daily Jobs\Master"
# os.makedirs(daily_jobs, exist_ok=True)
# summary_df = pd.DataFrame(result_rows)
# summary_path = os.path.join(daily_jobs, f"mongo_summary_{today_display}.xlsx")
# summary_df.to_excel(summary_path, index=False)
# print(f"\n📊 MongoDB summary saved at: {summary_path}")
#
# # === Step 6: Print Table ===
# print("\n📊 MongoDB Summary (Done / Pending / Not Found Comparison)\n")
# print(tabulate(summary_df, headers='keys', tablefmt='grid', showindex=False))

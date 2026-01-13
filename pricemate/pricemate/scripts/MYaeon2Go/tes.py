from datetime import datetime

date_str = "2025-10-06"  # your search_date or main_date
date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

calendar_week = date_obj.isocalendar()[1]-1  # [0]=year, [1]=week, [2]=weekday
print("Calendar Week:", calendar_week)

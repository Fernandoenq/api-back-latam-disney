from datetime import datetime, timedelta


class Constants:
    initial_margin_time = datetime.strptime("23:30:01", "%H:%M:%S").time()
    final_margin_time = datetime.strptime("23:59:00", "%H:%M:%S").time()

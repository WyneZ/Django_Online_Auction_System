from datetime import timedelta, datetime

delta = datetime.strptime("2 days, 9:22:04.175845", "%Y-%m-%dT%H:%M")

# s = int(delta.total_seconds())

print(delta)
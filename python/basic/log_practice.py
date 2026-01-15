logs = [
    "2026-01-15 10:45:12 INFO I200 Service started",
    "2026-01-15 10:46:01 ERROR E101 Invalid user input",
    "2026-01-15 10:47:05 WARNING W300 Disk almost full",
    "2026-01-15 10:48:22 ERROR E102 Database connection failed",
    "2026-01-15 10:49:10 ERROR E101 Invalid user input",
]

error_logs = [line for line in logs if " ERROR " in line]
print(error_logs)

timeStamps = [x.split()[0] +" "+x.split()[1] for x in error_logs]
print(timeStamps)
error_codes = {line.split()[3] for line in error_logs}
print(error_codes)
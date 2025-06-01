# Rclone

Docs:
https://rclone.org/docs/

Install:
sudo -v ; curl https://rclone.org/install.sh | sudo bash

Configure:
rclone config

Copy a file (if changed):
rclone copy data/db.json gdrive:podcast-history/

View files:
rclone ls gdrive:

Copy a file (if changed) with backup of previous file
rclone copy foo.txt gdrive:podcast-history/current/ --backup-dir gdrive:podcast-history/archive/ --suffix ".2025-06-01"

Copy a file (if changed) to other than its current name
rclone copyto foo.txt gdrive:podcast-history/foo.2025-06-01.txt

# Systemd timers

TLDR for running the app periodically with a systemd timer.

**TL;DR – run `/root/podcast-history/.venv/bin/python /root/podcast-history/main.py --rclone-remote gdrive` every day at 03:00 with a systemd timer**

1. **Create the service file**

```bash
sudo tee /etc/systemd/system/podcast-backup.service >/dev/null <<'EOF'
[Unit]
Description=Daily podcast-history backup

[Service]
Type=oneshot
ExecStart=/root/podcast-history/.venv/bin/python /root/podcast-history/main.py --rclone-remote gdrive
WorkingDirectory=/root/podcast-history
# optional: nicer log line-breaks
StandardOutput=journal
StandardError=journal
EOF
```

2. **Create the timer**

```bash
sudo tee /etc/systemd/system/podcast-backup.timer >/dev/null <<'EOF'
[Unit]
Description=Run podcast-backup.service daily

[Timer]
OnCalendar=03:00
Persistent=true          # run missed jobs after reboot

[Install]
WantedBy=timers.target
EOF
```

3. **Enable & start the timer**

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now podcast-backup.timer
```

4. **Check it**

```bash
# Next scheduled run
systemctl list-timers podcast-backup.timer

# Force a run right now
sudo systemctl start podcast-backup.service

# View logs
journalctl -u podcast-backup.service -f
```

That’s it—systemd will invoke your virtual-env Python command once a day, and any output (or stack-trace) is in `journalctl`.


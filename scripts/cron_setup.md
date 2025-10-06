# Cron Job Setup Instructions

This document provides instructions for setting up automated daily updates for the S&P 500 stock data.

## Prerequisites

1. Ensure the Python environment is set up correctly
2. Make sure the daily update script is executable
3. Have the project directory path available

## Linux/macOS Setup

### 1. Make the script executable
```bash
chmod +x /path/to/Stock-Predictive-Model/scripts/daily_update.py
```

### 2. Edit crontab
```bash
crontab -e
```

### 3. Add cron job entry
Add one of the following lines to run the daily update:

**Option A: Run at 6:00 AM every day (market close)**
```bash
0 6 * * * cd /path/to/Stock-Predictive-Model && /usr/bin/python3 scripts/daily_update.py --mode all --delay 0.1 >> logs/daily_update.log 2>&1
```

**Option B: Run at 9:30 PM every weekday (after market close)**
```bash
30 21 * * 1-5 cd /path/to/Stock-Predictive-Model && /usr/bin/python3 scripts/daily_update.py --mode all --delay 0.1 >> logs/daily_update.log 2>&1
```

**Option C: Run every 4 hours during market hours**
```bash
0 9,13,17,21 * * 1-5 cd /path/to/Stock-Predictive-Model && /usr/bin/python3 scripts/daily_update.py --mode all --delay 0.1 >> logs/daily_update.log 2>&1
```

### 4. Create logs directory
```bash
mkdir -p /path/to/Stock-Predictive-Model/logs
```

## Windows Setup (Task Scheduler)

### 1. Open Task Scheduler
- Press `Win + R`, type `taskschd.msc`, press Enter

### 2. Create Basic Task
- Click "Create Basic Task..." in the Actions panel
- Name: "S&P 500 Daily Update"
- Description: "Daily update of S&P 500 stock data"

### 3. Set Trigger
- Choose "Daily"
- Set start time (e.g., 6:00 AM)
- Set to recur every 1 day

### 4. Set Action
- Choose "Start a program"
- Program/script: `python`
- Add arguments: `scripts/daily_update.py --mode all --delay 0.1`
- Start in: `C:\path\to\Stock-Predictive-Model`

### 5. Configure Settings
- Check "Run whether user is logged on or not"
- Check "Run with highest privileges"
- Configure for Windows 10/11

## Monitoring and Logs

### Check Cron Job Status (Linux/macOS)
```bash
# View cron logs
tail -f /var/log/cron

# Check if cron is running
systemctl status cron

# View your crontab
crontab -l
```

### Check Task Scheduler Status (Windows)
- Open Task Scheduler
- Navigate to Task Scheduler Library
- Find your task and check last run time and result

### Log Files
- Daily update logs: `logs/daily_update.log`
- Application logs: `logs/app.log` (if configured)

## Troubleshooting

### Common Issues

1. **Permission denied**
   ```bash
   chmod +x scripts/daily_update.py
   ```

2. **Python path not found**
   - Use full path to python executable
   - Or add python to PATH environment variable

3. **Working directory issues**
   - Always use `cd /path/to/project` before running the script
   - Or use absolute paths in the script

4. **Import errors**
   - Ensure PYTHONPATH includes the project directory
   - Or run from the project root directory

### Testing the Setup

1. **Manual test**
   ```bash
   cd /path/to/Stock-Predictive-Model
   python3 scripts/daily_update.py --mode all
   ```

2. **Check data freshness**
   ```bash
   python3 scripts/daily_update.py --mode check
   ```

3. **Update specific tickers**
   ```bash
   python3 scripts/daily_update.py --mode specific --tickers AAPL MSFT GOOGL
   ```

## Alternative Scheduling Options

### Using systemd (Linux)
Create a service file for more advanced scheduling and monitoring.

### Using Docker Cron
If running in Docker, use a cron container or add cron to your existing container.

### Cloud-based Scheduling
- AWS EventBridge/CloudWatch Events
- Google Cloud Scheduler
- Azure Logic Apps

## Security Considerations

1. **File permissions**: Ensure log files have appropriate permissions
2. **Network access**: The script needs internet access to fetch data
3. **Resource limits**: Consider CPU and memory usage during updates
4. **Rate limiting**: Use appropriate delays to avoid being blocked by data providers

## Performance Optimization

1. **Parallel processing**: Consider updating multiple tickers simultaneously
2. **Incremental updates**: Only fetch new data since last update
3. **Database optimization**: Regular maintenance of SQLite database
4. **Error handling**: Implement retry logic for failed requests

## Backup Strategy

1. **Database backup**: Regular backups of the SQLite database
2. **Configuration backup**: Backup of cron jobs and configuration
3. **Log rotation**: Implement log rotation to prevent disk space issues

## Example Complete Cron Setup

```bash
# S&P 500 Daily Update at 6 AM
0 6 * * * cd /home/user/Stock-Predictive-Model && /usr/bin/python3 scripts/daily_update.py --mode all --delay 0.1 >> logs/daily_update.log 2>&1

# Database cleanup weekly (Sunday at 2 AM)
0 2 * * 0 cd /home/user/Stock-Predictive-Model && /usr/bin/python3 scripts/cleanup_database.py >> logs/cleanup.log 2>&1

# Log rotation monthly
0 0 1 * * find /home/user/Stock-Predictive-Model/logs -name "*.log" -mtime +30 -delete
```

Remember to replace `/home/user/Stock-Predictive-Model` with your actual project path.

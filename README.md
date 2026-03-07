# DeadlineHQ

A comprehensive Python CLI task manager with deadlines, reminders, priorities, tags, and email notifications — your command center for staying on track.

## Features

- ✅ Create tasks with deadlines, priorities, and tags
- 📋 Add sub-tasks to tasks
- 🔔 Set reminders for tasks
- 📧 Send daily status updates to subscribers
- ⚠️ Alert when deadlines are approaching
- 🏷️ Tag-based organization
- 🎯 Priority levels (LOW, MEDIUM, HIGH, URGENT)
- 🔍 Advanced search and filtering
- 💾 Automatic backup functionality
- 📊 Comprehensive logging
- ⚙️ Configurable email and scheduler settings

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy the example configuration file:
```bash
cp config.json.example config.json
```

4. Edit `config.json` with your settings (see Configuration section)

## Configuration

### Email Settings

DeadlineHQ supports two email providers. Choose the one that works best for you:

#### Option 1: Resend (Recommended — easiest setup)

[Resend](https://resend.com) is a modern email API. Free tier: 3,000 emails/month. No personal email password needed.

1. Sign up at https://resend.com
2. Get your API key from https://resend.com/api-keys
3. Set the environment variable:

```bash
# Windows (cmd)
set DEADLINEHQ_RESEND_API_KEY=re_your_api_key_here

# Windows (PowerShell)
$env:DEADLINEHQ_RESEND_API_KEY="re_your_api_key_here"

# Linux/Mac
export DEADLINEHQ_RESEND_API_KEY=re_your_api_key_here
```

4. In `config.json`, set the provider to `"resend"`:

```json
{
  "email": {
    "provider": "resend",
    "resend_from": "DeadlineHQ <onboarding@resend.dev>"
  }
}
```

> **Tip:** For production use, verify your own domain in Resend and update `resend_from` to use it.

#### Option 2: SMTP (Gmail / other providers)

Uses traditional SMTP to send from your own email account. Requires a Gmail App Password (not your regular password).

1. Enable 2-factor authentication on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Generate an app password for "Mail"
4. Set environment variables:

```bash
# Windows (cmd)
set DEADLINEHQ_EMAIL_PASSWORD=your_app_password
set DEADLINEHQ_SENDER_EMAIL=your_email@gmail.com

# Windows (PowerShell)
$env:DEADLINEHQ_EMAIL_PASSWORD="your_app_password"
$env:DEADLINEHQ_SENDER_EMAIL="your_email@gmail.com"

# Linux/Mac
export DEADLINEHQ_EMAIL_PASSWORD=your_app_password
export DEADLINEHQ_SENDER_EMAIL=your_email@gmail.com
```

5. In `config.json`, set the provider to `"smtp"`:

```json
{
  "email": {
    "provider": "smtp",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your_email@gmail.com"
  }
}
```

### Configuration File

Edit `config.json` to customize all settings:

```json
{
  "email": {
    "provider": "resend",
    "resend_from": "DeadlineHQ <onboarding@resend.dev>",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your_email@gmail.com",
    "use_env_password": true
  },
  "scheduler": {
    "daily_update_time": "09:00",
    "deadline_check_interval_hours": 1,
    "deadline_alert_threshold_days": 1
  },
  "storage": {
    "tasks_file": "tasks.json",
    "backup_enabled": true,
    "backup_directory": "backups"
  }
}
```

## Usage

### Create a Task

```bash
python main.py create "Task Name" "Description" "2024-12-31T23:59:59"

# With priority and tags
python main.py create "Important Task" "Description" "2024-12-31T23:59:59" --priority HIGH --tags "work,urgent"
```

### List All Tasks

```bash
python main.py list
```

### Search and Filter Tasks

```bash
# Search by keyword
python main.py search --query "meeting"

# Filter by tag
python main.py search --tag "work"

# Filter by priority
python main.py search --priority HIGH

# Filter by completion status
python main.py search --completed false

# Combine filters
python main.py search --tag "work" --priority HIGH --completed false
```

### Add a Sub-Task

```bash
python main.py add_sub "Task Name" "Sub Name" "Sub Description" "2024-12-30T23:59:59"
```

### Complete Tasks

```bash
# Complete a task
python main.py complete "Task Name"

# Complete a sub-task
python main.py complete_sub "Task Name" "Sub Task Name"
```

### Update Tasks

```bash
# Update task name
python main.py update "Old Name" --name "New Name"

# Update deadline
python main.py update "Task Name" --deadline "2025-01-15T12:00:00"

# Update description
python main.py update "Task Name" --description "New description"

# Update sub-task
python main.py update_sub "Task Name" "Sub Name" --deadline "2024-12-25T10:00:00"
```

### Manage Tags

```bash
# Add a tag
python main.py add_tag "Task Name" "important"

# Remove a tag
python main.py remove_tag "Task Name" "important"
```

### Set Priority

```bash
python main.py set_priority "Task Name" HIGH
# Options: LOW, MEDIUM, HIGH, URGENT
```

### Delete Tasks

```bash
# Delete a task
python main.py delete "Task Name"

# Delete a sub-task
python main.py delete_sub "Task Name" "Sub Task Name"
```

### Add Email Subscribers

```bash
python main.py add_subscriber "Task Name" "email@example.com"
```

### Start the Scheduler

The scheduler runs in the background and:
- Sends daily status updates at the configured time (default: 9:00 AM)
- Checks for approaching deadlines every hour (configurable)
- Sends alerts when deadlines are within the threshold (default: 1 day)

```bash
python main.py start
```

Press `Ctrl+C` to stop the scheduler gracefully.

## Project Structure

```
deadlinehq/
├── main.py                 # CLI entry point
├── config.json            # Configuration file (create from example)
├── config.json.example    # Example configuration
├── requirements.txt       # Python dependencies
├── tasks.json            # Task storage (auto-created)
├── README.md             # This file
├── src/
│   ├── __init__.py
│   ├── task.py           # Task and SubTask classes
│   ├── storage.py        # JSON storage with backup
│   ├── scheduler.py      # Background scheduler
│   ├── reminder.py       # Email notification system
│   ├── config.py         # Configuration management
│   ├── validation.py     # Input validation
│   └── logger.py         # Logging system
├── tests/
│   ├── __init__.py
│   ├── test_task.py
│   ├── test_task_methods.py
│   ├── test_storage.py
│   └── test_validation.py
├── logs/                 # Log files (auto-created)
└── backups/             # Task backups (auto-created if enabled)
```

## Running Tests

```bash
pytest tests/
```

## Logging

Logs are automatically created in the `logs/` directory with daily rotation:
- File: `logs/deadlinehq_YYYYMMDD.log`
- Console: Only warnings and errors are shown
- File logs: All operations are logged (INFO level and above)

## Backup

When backup is enabled in `config.json`, the system automatically creates timestamped backups before saving changes:
- Location: `backups/tasks_backup_YYYYMMDD_HHMMSS.json`
- Automatic: Created on every save operation

## Priority Levels

- **LOW**: Nice to have, no urgency
- **MEDIUM**: Normal priority (default)
- **HIGH**: Important, should be done soon
- **URGENT**: Critical, needs immediate attention

## Examples

### Complete Workflow

```bash
# 1. Create a high-priority work task
python main.py create "Quarterly Report" "Prepare Q4 report" "2024-12-31T17:00:00" --priority HIGH --tags "work,report"

# 2. Add sub-tasks
python main.py add_sub "Quarterly Report" "Gather Data" "Collect all metrics" "2024-12-20T17:00:00"
python main.py add_sub "Quarterly Report" "Write Report" "Draft the report" "2024-12-28T17:00:00"

# 3. Add email subscriber for updates
python main.py add_subscriber "Quarterly Report" "manager@company.com"

# 4. Complete sub-tasks as you progress
python main.py complete_sub "Quarterly Report" "Gather Data"

# 5. Search for all high-priority work tasks
python main.py search --priority HIGH --tag "work"

# 6. Mark task as complete when done
python main.py complete "Quarterly Report"
```

## Troubleshooting

### Email not sending

1. Verify environment variables are set correctly
2. For Gmail, ensure you're using an App Password, not your regular password
3. Check that 2-factor authentication is enabled on your Google account
4. Verify SMTP settings in `config.json`

### Tasks not saving

1. Check file permissions in the project directory
2. Review logs in `logs/` directory for error messages
3. Ensure `tasks.json` is not corrupted (check backups if needed)

### Scheduler not running

1. Ensure the scheduler command is running: `python main.py start`
2. Check logs for any errors
3. Verify email configuration is correct

## License

MIT License — feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

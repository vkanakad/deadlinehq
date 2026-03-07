import schedule
import time
import signal
import sys
from datetime import datetime, timedelta
from .storage import load_tasks, save_tasks
from .reminder import send_daily_status, send_deadline_alert
from .config import get_config


# Global flag for graceful shutdown
_running = True


def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    global _running
    print("\nShutting down scheduler gracefully...")
    _running = False


def check_deadlines():
    """Check for approaching deadlines and send alerts."""
    config = get_config()
    tasks = load_tasks()
    now = datetime.now()
    
    threshold_days = config.get('scheduler', 'deadline_alert_threshold_days', default=1)
    alert_threshold = timedelta(days=threshold_days)
    
    for task in tasks:
        time_left = task.deadline - now
        print(f"\nTask: {task.name}")
        print(f"  Deadline: {task.deadline}")
        print(f"  Time left: {time_left}")
        print(f"  Completed: {task.completed}")
        print(f"  Subscribers: {task.subscribers}")
        
        if not task.completed and time_left <= alert_threshold and time_left.total_seconds() > 0:
            print(f"  >>> ALERT: Deadline approaching!")
            for sub in task.subscribers:
                send_deadline_alert(task, sub)
        elif task.deadline <= now:
            print(f"  (skipped - deadline passed)")
        else:
            print(f"  (no alert needed - deadline not within threshold)")
        
        # Check sub-tasks
        for st in task.sub_tasks:
            st_time_left = st.deadline - now
            print(f"  Sub-task: {st.name}")
            print(f"    Deadline: {st.deadline}")
            print(f"    Time left: {st_time_left}")
            print(f"    Completed: {st.completed}")
            
            if not st.completed and st_time_left <= alert_threshold and st_time_left.total_seconds() > 0:
                print(f"    >>> ALERT: Sub-task deadline approaching!")
                for sub in task.subscribers:
                    send_deadline_alert(task, sub)
            elif st.deadline <= now:
                print(f"    (skipped - deadline passed)")
            else:
                print(f"    (no alert needed - deadline not within threshold)")


def send_daily_updates():
    """Send daily status updates to all subscribers."""
    tasks = load_tasks()
    email_count = 0
    for task in tasks:
        for sub in task.subscribers:
            send_daily_status(task, sub)
            email_count += 1
            # Add delay to respect Resend API rate limit (2 requests/second max)
            if email_count % 2 == 0:
                time.sleep(0.6)  # 0.6 second delay after every 2 emails


def start_scheduler():
    """Start the task scheduler with configured intervals.
    
    Runs until interrupted with Ctrl+C or SIGTERM.
    """
    global _running
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    config = get_config()
    
    # Get configuration
    daily_time = config.get('scheduler', 'daily_update_time', default='09:00')
    check_interval = config.get('scheduler', 'deadline_check_interval_hours', default=1)
    
    # Schedule jobs
    schedule.every().day.at(daily_time).do(send_daily_updates)
    schedule.every(check_interval).hours.do(check_deadlines)
    
    print(f"Scheduler started. Daily updates at {daily_time}, deadline checks every {check_interval} hour(s).")
    print("Press Ctrl+C to stop.")

    while _running:
        schedule.run_pending()
        time.sleep(60)  # check every minute
    
    print("Scheduler stopped.")
    sys.exit(0)
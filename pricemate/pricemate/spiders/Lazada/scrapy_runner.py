import subprocess
import time
import signal
import sys
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Configuration
RETRY_INTERVAL = 15 * 60  # 15 minutes in seconds
MAX_DURATION = 12 * 60 * 60  # 12 hours in seconds
PROCESS_TIMEOUT = 14 * 60  # 14 minutes (kill before next retry)
MAX_WORKERS = 9  # Number of parallel spiders

# List of all spider commands
SPIDER_COMMANDS = [
"scrapy crawl lazada_shop -a retailer=lazada_id -a region=id -a Type=eshop -a RetailerCode=lazada_watsons_id",
"scrapy crawl lazada_shop -a retailer=lazada_ph -a region=ph -a Type=marketplace -a RetailerCode=lazada_watsons_ph",
"scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_bigpharmacy_my",
"scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_guardian_my",
"scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_petsmore_my",
"scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_mydin_my",
"scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_watsons_my",
"scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_caring_my",
"scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_aeon_my",
"scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_villagegrocer_my",
"scrapy crawl lazada_shop -a retailer=lazada_sg -a region=sg -a Type=marketplace -a RetailerCode=lazada_sg",
"scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_my",
"scrapy crawl lazada_shop -a retailer=lazada_ph -a region=ph -a Type=marketplace -a RetailerCode=lazada_ph",
"scrapy crawl lazada_shop -a retailer=lazada_id -a region=id -a Type=marketplace -a RetailerCode=lazada_id",
]

# Thread-safe logging
log_lock = threading.Lock()


def log_message(message, retailer_code=None):
    """Print timestamped log messages (thread-safe)"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_lock:
        if retailer_code:
            print(f"[{timestamp}] [{retailer_code}] {message}")
        else:
            print(f"[{timestamp}] {message}")


def extract_retailer_code(command):
    """Extract RetailerCode from command for logging"""
    try:
        parts = command.split("RetailerCode=")
        if len(parts) > 1:
            return parts[1].split()[0]
    except:
        pass
    return "unknown"


def kill_process(process):
    """Kill a running process and its children"""
    if process and process.poll() is None:
        try:
            # Try graceful termination first
            process.terminate()
            time.sleep(2)

            # Force kill if still running
            if process.poll() is None:
                process.kill()
        except Exception as e:
            pass


def run_spider_command(command, timeout, command_index):
    """Run a single spider command with timeout"""
    retailer_code = extract_retailer_code(command)
    log_message(f"Starting command #{command_index}", retailer_code)

    start_time = time.time()

    try:
        process = subprocess.Popen(
            command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'  # Replace undecodable characters with ?
        )

        try:
            stdout, stderr = process.communicate(timeout=timeout)
            elapsed = time.time() - start_time

            if process.returncode == 0:
                log_message(f"✓ Completed successfully in {elapsed:.1f}s", retailer_code)
                return {
                    'command_index': command_index,
                    'retailer_code': retailer_code,
                    'success': True,
                    'elapsed': elapsed
                }
            else:
                log_message(f"✗ Failed with return code: {process.returncode}", retailer_code)
                return {
                    'command_index': command_index,
                    'retailer_code': retailer_code,
                    'success': False,
                    'elapsed': elapsed,
                    'error': f"Return code: {process.returncode}"
                }

        except subprocess.TimeoutExpired:
            elapsed = time.time() - start_time
            log_message(f"⏱ Timeout after {elapsed:.1f}s", retailer_code)
            kill_process(process)
            return {
                'command_index': command_index,
                'retailer_code': retailer_code,
                'success': False,
                'elapsed': elapsed,
                'error': 'Timeout'
            }

    except Exception as e:
        elapsed = time.time() - start_time
        log_message(f"✗ Exception: {e}", retailer_code)
        return {
            'command_index': command_index,
            'retailer_code': retailer_code,
            'success': False,
            'elapsed': elapsed,
            'error': str(e)
        }


def run_all_spiders_parallel():
    """Run all spider commands in parallel"""
    log_message("=" * 80)
    log_message("Starting PARALLEL spider batch execution")
    log_message(f"Running {len(SPIDER_COMMANDS)} spiders concurrently")
    log_message("=" * 80)

    results = []
    batch_start = time.time()

    # Run all commands in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all tasks
        future_to_command = {
            executor.submit(run_spider_command, cmd, PROCESS_TIMEOUT, i + 1): (i + 1, cmd)
            for i, cmd in enumerate(SPIDER_COMMANDS)
        }

        # Process completed tasks as they finish
        for future in as_completed(future_to_command):
            command_index, command = future_to_command[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                log_message(f"✗ Unexpected error in command #{command_index}: {e}")
                results.append({
                    'command_index': command_index,
                    'success': False,
                    'error': str(e)
                })

    batch_elapsed = time.time() - batch_start

    # Sort results by command index for consistent reporting
    results.sort(key=lambda x: x['command_index'])

    # Summary
    success_count = sum(1 for r in results if r['success'])
    fail_count = len(results) - success_count

    log_message("\n" + "=" * 80)
    log_message(f"Batch completed in {batch_elapsed:.1f}s")
    log_message(f"Success: {success_count}/{len(results)} | Failed: {fail_count}/{len(results)}")

    # Show failed commands
    if fail_count > 0:
        log_message("\nFailed commands:")
        for r in results:
            if not r['success']:
                log_message(f"  - #{r['command_index']} [{r['retailer_code']}]: {r.get('error', 'Unknown error')}")

    log_message("=" * 80)

    return success_count, fail_count


def main():
    """Main execution loop with retry logic"""
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=MAX_DURATION)

    log_message("*" * 80)
    log_message("SCRAPY SPIDER RUNNER - PARALLEL EXECUTION WITH RETRY LOGIC")
    log_message("*" * 80)
    log_message(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_message(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_message(f"Retry interval: {RETRY_INTERVAL // 60} minutes")
    log_message(f"Max duration: {MAX_DURATION // 3600} hours")
    log_message(f"Number of commands: {len(SPIDER_COMMANDS)} (running in parallel)")
    log_message(f"Max parallel workers: {MAX_WORKERS}")
    log_message("*" * 80)

    run_count = 0
    total_success = 0
    total_fail = 0

    try:
        while datetime.now() < end_time:
            run_count += 1
            current_time = datetime.now()
            remaining = end_time - current_time

            log_message(f"\n{'#' * 80}")
            log_message(f"RUN #{run_count}")
            log_message(f"Time remaining: {remaining.seconds // 3600}h {(remaining.seconds % 3600) // 60}m")
            log_message(f"{'#' * 80}\n")

            # Run all spiders in parallel
            success_count, fail_count = run_all_spiders_parallel()
            total_success += success_count
            total_fail += fail_count

            # Check if we have time for another run
            current_time = datetime.now()
            if current_time + timedelta(seconds=RETRY_INTERVAL) >= end_time:
                log_message("\nNot enough time for another run. Exiting...")
                break

            # Wait for retry interval
            next_run = current_time + timedelta(seconds=RETRY_INTERVAL)
            log_message(f"\n⏳ Waiting {RETRY_INTERVAL // 60} minutes before next run...")
            log_message(f"Next run scheduled at: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(RETRY_INTERVAL)

    except KeyboardInterrupt:
        log_message("\n\n⚠ Script interrupted by user (Ctrl+C)")

    finally:
        total_duration = datetime.now() - start_time
        log_message("\n" + "*" * 80)
        log_message("EXECUTION SUMMARY")
        log_message("*" * 80)
        log_message(f"Total runs completed: {run_count}")
        log_message(f"Total commands executed: {run_count * len(SPIDER_COMMANDS)}")
        log_message(f"Total successful: {total_success}")
        log_message(f"Total failed: {total_fail}")
        log_message(f"Success rate: {(total_success / (total_success + total_fail) * 100):.1f}%")
        log_message(f"Total duration: {total_duration.seconds // 3600}h {(total_duration.seconds % 3600) // 60}m")
        log_message(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log_message("*" * 80)


if __name__ == "__main__":
    main()
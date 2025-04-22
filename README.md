# Multi Progress Bar

## Introduction

This file defines a class called ProgressBar designed to create and manage multiple text-based progress bars that can run concurrently in your terminal or console window. This is useful when you have several tasks running simultaneously (like downloads, processing steps, etc.) and want to visualize their progress individually. ProgressBar class that uses threading (Lock, Timer) and ANSI escape codes to display and update multiple progress bars simultaneously in the console without them interfering with each other visually. The class handles redrawing them periodically in the correct position on the screen.

## ProgressBar Methods

- `__init__(self, bar_len: int = 30)`:
  - This is the constructor. When you create a ProgressBar object, this method runs.
  - It takes an optional bar_len argument, which sets the visual width (number of characters like ===---) of the progress bars.
  - It ensures the bar_len is within a reasonable range (10 to 80 characters); otherwise, it defaults to 30.
  - It initializes an empty dictionary self.lanes to store information about each individual progress bar (which it calls a "lane").
  - It creates a threading.Lock called update_lock. This is crucial for thread safety. If multiple threads try to update the progress bars at the same time, the lock ensures that only one thread can modify the lanes dictionary at a time, preventing data corruption.
  - It sets a timer_flag to True, which is used to control the automatic refreshing of the display.

- `get_random_4_digit_number(self)`:
  - A simple helper method that generates a random integer between 1000 and 9999. This is used to create unique IDs for new progress bar lanes.

- `add_lane(self, status: str, total: int) -> int`:
  - This method adds a new progress bar (a "lane") to be displayed.
  - It takes a status string (e.g., "Downloading file X") and a total integer (the maximum value the progress count will reach, e.g., file size in bytes).
  - If total is 0, it means the progress bar won't show a percentage or the [===---] bar, just the status text. This is useful for tasks where the total isn't known or progress isn't easily quantifiable.
  - It generates a random lane_id using get_random_4_digit_number.
  - It acquires the update_lock to safely modify the lanes dictionary.
  - It adds a new entry to self.lanes using the lane_id as the key. The value is another dictionary containing the status, total, and an initial empty display string.
  - It releases the lock.
  - It returns the generated lane_id so you can refer to this specific progress bar later.

- `clear_all_lanes(self)`:
  - This method is used to remove all currently displayed progress bars.
  - It first calls display_flush to update the screen one last time.
  - It then uses ANSI escape codes (\033[{n}B) to move the cursor down n lines (where n is the number of lanes), effectively moving past the area where the progress bars were displayed.
  - Finally, it clears the self.lanes dictionary.

- `update_lane(self, lane_id, string: str, total: int)`:
  - Allows you to change the status text and the total value of an existing lane after it has been added.
  - It finds the lane using its lane_id.
  - It acquires the lock, updates the status and total in the lanes dictionary for that specific lane_id, and potentially updates the initial display string if the total becomes non-zero.
  - It releases the lock.

- `update(self, count, lane_id)`:
  - This is the core method for updating the progress of a specific lane.
  - It takes the current count (how much progress has been made) and the lane_id.
  - It acquires the lock.
  - It retrieves the total and status for the given lane_id.
  - If the total is 0, it does nothing (as it's just a status message).
  - If total is greater than 0, it calculates:
    - filled_len: How many = characters to show in the bar.
    - percents: The percentage completion.
    - bar_filled: The actual string representation of the bar (e.g., [=======---]).
  - It updates the display string for that lane in the self.lanes dictionary with the formatted progress bar, percentage, and status.
  - It releases the lock.

- `start_timed_flush(self)`:
  - This method initiates the automatic refreshing of the display.
  - It creates a threading.Timer that will call the display_flush method after a 1.0-second delay.
  - It starts the timer. The display_flush method itself will schedule the next flush, creating a loop.

- `display_flush(self)`:
  - This method handles the actual printing of the progress bars to the console.
  - It checks if there are any lanes to display (n > 0).
  - It acquires the lock.
  - It iterates through the self.lanes dictionary and concatenates the display string (or just the status if total is 0) for each lane into a single screen string, adding newlines between them.
  - It releases the lock.
  - It prints the entire screen string to the console.
  - Crucially, it then prints an ANSI escape code (\033[{n}A). This code moves the cursor up n lines. This positions the cursor back at the beginning of the progress bar display area, so the next time display_flush runs, it overwrites the previous display, creating the animation effect.
  - It flushes the output buffer (sys.stdout.flush()) to ensure the text appears immediately.
  - If `self.timer_flag` is still True, it calls `start_timed_flush()` again to schedule the next update in one second.

"""
Multi progress bar module for displaying multiple concurrent progress bars in
the console.

> _Author_: Claudio Olmi
> _Github_: superolmo


"""
import sys
from random import randint
from threading import Lock, Timer


class MultiProgressBar():
    """A class for managing and displaying multiple progress bars concurrently.

    Attributes:
        timer_flag (bool): Flag to control the timed display updates
        bar_len (int): Length of each progress bar lane
        lanes (dict): Dictionary containing progress bar lane data
        update_lock (Lock): Thread lock for concurrent updates
    """
    timer_flag = True

    # Length of each individual progress bar lane
    bar_len = 0
    # Dictionary of active lanes with their status and progress information
    lanes = {}

    update_lock = Lock()

    def __init__(self, bar_len: int = 30):

        # Only allow from 10 to 80 characters progress bar width
        if bar_len in range(10, 80):
            self.bar_len = bar_len
        else:
            self.bar_len = 30

    def get_random_4_digit_number(self):
        """Generates a random 4-digit number.

        Returns:
            int: A random integer between 1000 and 9999 (inclusive).
        """
        return randint(1000, 9999)

    def add_lane(self, status: str, total: int) -> int:
        """Adds a new progress bar lane with the given status and total count.

        Args:
            status (str): The status message to display for this lane
            total (int): The total count for progress calculation
                         If zero, the progress bar does not show.

        Returns:
            int: The unique lane ID for this progress bar
        """
        with self.update_lock:
            r = self.get_random_4_digit_number()
            new_lane = {r: {'status': status, 'total': total, 'display': ''}}
            self.lanes.update(new_lane)
        return r

    def clear_all_lanes(self):
        """Clears all progress bar lanes and resets the console position.

        This method flushes the display and moves the cursor down to clear the
        progress bar display area before emptying the lanes dictionary.
        """
        n = len(self.lanes)
        self.display_flush()
        sys.stdout.write(f"\033[{n}B")
        sys.stdout.flush()
        self.lanes = {}

    def update_lane(self, lane_id, string: str, total: int):
        """Updates the status message for a specific progress bar lane.

        Args:
            lane_id (int): The unique ID of the lane to update
            string (str): The new status message
            total (int): The new total number
        """
        if lane_id in self.lanes:
            with self.update_lock:
                self.lanes[lane_id]["status"] = string
                self.lanes[lane_id]['total'] = total
                if total > 0:
                    self.lanes[lane_id]["display"] = f"{string}\n"

    def update(self, count, lane_id):
        """Updates the progress count for a specific lane.

        Args:
            count (int): The current progress count
            lane_id (int): The unique ID of the lane to update
        """
        if lane_id in self.lanes:
            with self.update_lock:
                total = self.lanes[lane_id]['total']
                status = self.lanes[lane_id]['status']
                if self.lanes[lane_id]['total'] == 0:
                    return

                filled_len = int(round(self.bar_len * count / float(total)))

                percents = round(100.0 * count / float(total), 1)
                percents_str = f'{percents:.1f}'
                bar_filled = '=' * filled_len + '-' * \
                             (self.bar_len - filled_len)
                self.lanes[lane_id]["display"] = f'[{bar_filled}] ' \
                                                 f'{percents_str:>5}% - {status}\n'

    def start_timed_flush(self):
        """Starts a timer to periodically update the progress display.

        This method schedules display updates every second to ensure the
        progress bars are refreshed regularly.
        """
        t = Timer(1.0, self.display_flush)
        t.start()

    def display_flush(self):
        """Flushes all progress bars to the console.

        This method renders all progress bars to the console and
        repositions the cursor to allow for continuous updates.
        """
        n = len(self.lanes)
        if n > 0:
            with self.update_lock:
                screen = ""
                for _, lane_data in self.lanes.items():
                    if lane_data['total'] == 0:
                        screen += lane_data['status'] + "\n"
                    else:
                        screen += lane_data['display']
            sys.stdout.write(screen + f"\033[{n}A")
            sys.stdout.flush()
        if self.timer_flag:
            self.start_timed_flush()

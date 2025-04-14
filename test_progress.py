import threading
import time

from multi_progress_bar import MultiProgressBar

# Create a progress bar
pb = MultiProgressBar()

# Add some lanes
laneID1 = pb.add_lane(status="Task 1", total=100)
laneID2 = pb.add_lane(status="Task 2", total=50)
laneID3 = pb.add_lane(status="Downloading", total=0)

# Start the timed flush
pb.start_timed_flush()


def task1():
    for i in range(1, 101):
        pb.update(i, laneID1)
        time.sleep(0.05)


def task2():
    for i in range(1, 51):
        pb.update(i, laneID2)
        time.sleep(0.2)


def task3():
    for i in range(1, 500):
        pb.update_lane(laneID3, f"Downloading {i}", 0)
        time.sleep(0.01)
    pb.update_lane(laneID3, "Processing", 500)
    for i in range(1, 500):
        pb.update(i, laneID3)
        time.sleep(0.01)


# Start the tasks in separate threads
thread1 = threading.Thread(target=task1)
thread2 = threading.Thread(target=task2)
thread3 = threading.Thread(target=task3)
thread1.start()
thread2.start()
thread3.start()

thread1.join()
thread2.join()
thread3.join()

pb.clear_all_lanes()
pb.timer_flag = False

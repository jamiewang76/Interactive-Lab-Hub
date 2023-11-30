import threading
import time

def countdown(timer_name, initial_time):
    while initial_time > 0:
        print(f"{timer_name}: {initial_time} seconds")
        time.sleep(1)
        initial_time -= 1
    print(f"{timer_name}: Time's up!")

# Set initial times for each timer
time1 = 10
time2 = 15
time3 = 8
time4 = 5

# Create threads for each timer
timer_thread1 = threading.Thread(target=countdown, args=("Timer 1", time1))
timer_thread2 = threading.Thread(target=countdown, args=("Timer 2", time2))
timer_thread3 = threading.Thread(target=countdown, args=("Timer 3", time3))
timer_thread4 = threading.Thread(target=countdown, args=("Timer 4", time4))

# Start the threads
timer_thread1.start()
timer_thread2.start()
timer_thread3.start()
timer_thread4.start()

# Wait for all threads to finish
timer_thread1.join()
timer_thread2.join()
timer_thread3.join()
timer_thread4.join()

print("All timers have finished.")

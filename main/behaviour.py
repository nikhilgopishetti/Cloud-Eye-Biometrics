
# import keyboard
# import time
# import pyautogui
# import time

# # Function to calculate mouse movement distance
# def calculate_distance(x1, y1, x2, y2):
#     return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

# # Thresholds for abnormal mouse behavior
# distance_threshold = 500  # pixels
# click_interval_threshold = 0.1  # seconds
# abnormalinstance = 0

# # Monitor mouse events
def monitor_mouse_behavior():
    count = 0
#     last_position = pyautogui.position()
#     last_click_time = time.time()

#     while True:
#         try:
#             current_position = pyautogui.position()
#             distance = calculate_distance(last_position[0], last_position[1], current_position[0], current_position[1])
#             if distance > distance_threshold:
#                 print("Abnormal mouse movement detected!")
#                 abnormalinstance + 1
                
            
#             current_time = time.time()
#             click_interval = current_time - last_click_time
#             if click_interval < click_interval_threshold:
#                 print("Abnormal mouse clicking frequency detected!")
#                 abnormalinstance + 1

#             last_position = current_position
#             last_click_time = current_time
#             return abnormalinstance

#             time.sleep(0.1)  # Adjust the sleep time as needed
#         except Exception as e:
#             print("Error:", e)
#         return abnormalinstance
# #monitor_mouse_behavior(logout=3)


# # Function to calculate typing speed
# def calculate_typing_speed(start_time, end_time, num_characters):
#     typing_time = end_time - start_time
#     typing_speed = num_characters / typing_time
#     return typing_speed

# # Threshold for extreme typing speed (characters per second)
# threshold_speed = 50

# # Monitor keyboard events 
def monitor_typing_speed():
    count= 2
#     characters_typed = 0
#     start_time = time.time()
#     while True:
#         try:
#             event = keyboard.read_event()
#             if event.event_type == keyboard.KEY_DOWN:
#                 characters_typed += 1
#                 end_time = time.time()
#                 typing_speed = calculate_typing_speed(start_time, end_time, characters_typed)
#                 if typing_speed > threshold_speed:
#                     print("Extreme typing speed detected! Typing speed:", typing_speed, "characters per second")
#                     abnormalinstance + 1
#                 start_time = time.time()
#                 characters_typed = 0
#                 return abnormalinstance
#         except Exception as e:
#             print("Error:", e)


import picar_4wd as fc
import math
from Astar import A_star, visualize_path
from speed import Speed
import time
import obj_det2
from vision import scan_surroundings

def left_90(cell_jump):
    fc.turn_left(10)
    time.sleep(1.21)
    fc.forward(10)
    time.sleep(0.16 * cell_jump)


def left_45(cell_jump):
    fc.turn_left(10)
    time.sleep(0.66)
    fc.forward(10)
    time.sleep(0.16 * math.sqrt(2)* cell_jump * 1.1)

def forward_0(cell_jump):
    fc.forward(10)
    time.sleep(0.17 * cell_jump)

def right_45(cell_jump):
    fc.turn_right(10)
    time.sleep(0.58)
    fc.forward(10)
    time.sleep(0.16 * math.sqrt(2) * cell_jump)


def right_90(cell_jump):
    fc.turn_right(10)
    time.sleep(1.08)
    fc.forward(10)
    time.sleep(0.16 * cell_jump)

action_dict = {
    -2: left_90,
    -1: left_45,
    0: forward_0,
    1: right_45,
    2: right_90
}


def navigate(rescan_step = 25):
    origin = (99, 49)  # origin coor
    target = (0, 49)    # Goal coor
    padded_map, path = scan_plan(origin, target)
    current_row, current_col = origin

    test_run = Speed(25)
    test_run.start()
    fc.forward(10)
    current_direction = 2
    # direction key: 0=full left, 1=left diag, 2=up,3=right diag, 4=full right
    cell_jump = 1.1
    reach_target = False
    error = False

    while True:
        if error or reach_target or len(path) == 1:
            break # reached the target or no path left
        for next_i in range(1, len(path)):
            next_row, next_col = path[next_i]
            print("Step:", next_i, " at:", path[next_i]," currently at:", current_row, current_col)

            # """Integrating PEOPLE and SIGN Detection Here """ # need to adjust
            # if next_i%2==0:
            #     fc.forward(0)
            #     person, traffic_sign = obj_det2.run_obj_det('efficientdet_lite0.tflite', 0, 640, 480, 4, False)
            #     while person:
            #         print("Person ahead, Stop and check again in 2 seconds")
            #         fc.stop()
            #         time.sleep(2)
            #         person, traffic_sign = obj_det2.run_obj_det('efficientdet_lite0.tflite', 0, 640, 480, 4, False)
            #     if traffic_sign:
            #         fc.stop()
            #         print("Stopping for 5 seconds for stop sign")
            #         time.sleep(5)
            #     fc.forward(10)
            # """ END - HUMAN - SIGN Detection"""

            # rescan the map
            if (origin[0]-current_row) >= rescan_step and current_direction == 2:
                test_run.deinit()
                fc.stop()
                target[0] += (origin[0] - current_row)               
                target[1] -= (current_col - origin[1])
                target[0] = min(max(0, target[0]), 99)
                target[1] = min(max(0, target[1]), 99)
                print("New target:", target)
                # target = (0, 49)    # Goal coor
                padded_map, path = scan_plan(origin, target)
                break

            if next_row == current_row and next_col == current_col - 1:  # NEED TO GO FULL LEFT
                next_direction = 0
            elif next_row == current_row - 1 and next_col == current_col - 1:  # NEED TO GO DIAG LEFT
                next_direction = 1
            elif next_row == current_row - 1 and next_col == current_col:  # NEED TO GO UP
                next_direction = 2
            elif next_row == current_row - 1 and next_col == current_col + 1:  # NEED TO GO DIAG right)
                next_direction = 3
            elif next_row == current_row and next_col == current_col + 1:  # NEED TO GO FULL right
                next_direction = 4
            else:
                print("Error: Invalid next direction")
                error = True
                break
                
            direction_diff = next_direction - current_direction
            if direction_diff in action_dict:
                action_dict[(current_direction-next_direction)](cell_jump)
                current_row = next_row
                current_col = next_col
                current_direction = next_direction
            else:
                print("Error: Invalid direction change")
                error = True
                break
    test_run.deinit()
    fc.stop()


def scan_plan(origin, target):
    # scan the environment and plan the route
    padded_map = scan_surroundings(90)
    # print(map[target])
    path = A_star(padded_map, origin, target)
    visualize_path(padded_map, path)
    return padded_map, path


def main():

    navigate(rescan_step=25)

if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()


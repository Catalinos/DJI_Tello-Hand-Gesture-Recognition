from djitellopy import Tello

class MyTelloControl:
    def __init__(self, tello: Tello):
        self.tello = tello

    def key_control(self, key):
        if key == ord('w'):
            self.tello.move_forward(30)
        elif key == ord('s'):
            self.tello.move_back(30)
        elif key == ord('a'):
            self.tello.move_left(30)
        elif key == ord('d'):
            self.tello.move_right(30)
        elif key == ord('e'):
            self.tello.rotate_clockwise(30)
        elif key == ord('q'):
            self.tello.rotate_counter_clockwise(30)
        elif key == ord('r'):
            self.tello.move_up(30)
        elif key == ord('f'):
            self.tello.move_down(30)


    def gesture_control(self,gestureID):

        if gestureID == 0:
            self.tello.move_forward(30)
        elif gestureID == 1:
            self.tello.move_back(30)
        elif gestureID == 2:
            self.tello.move_left(30)
        elif gestureID == 3:
            self.tello.move_right(30)
        elif gestureID == 4:
            self.tello.move_up(30)
        elif gestureID == 5:
            self.tello.move_down(30)
        elif gestureID == 6:
            self.tello.rotate_clockwise(30)
        elif gestureID == 7:
            self.tello.rotate_counter_clockwise(30)
        elif gestureID == 9:
            self.tello.land()

import math

class Camera:
    def __init__(self):

        self.x = 0
        self.y = 0
        self.z = -800

        self.yaw = 0
        self.pitch = 0

        self.dragging_rotate = False
        self.dragging_move = False

        self.last_mouse = (0, 0)

    def handle_mouse_down(self, button, pos):

        self.last_mouse = pos

        if button == 1:
            self.dragging_rotate = True

        if button == 3:
            self.dragging_move = True

    def handle_mouse_up(self, button):

        if button == 1:
            self.dragging_rotate = False

        if button == 3:
            self.dragging_move = False

    def handle_mouse_motion(self, pos):

        dx = pos[0] - self.last_mouse[0]
        dy = pos[1] - self.last_mouse[1]

        self.last_mouse = pos

        if self.dragging_rotate:
            self.yaw += dx * 0.005
            self.pitch += dy * 0.005

        if self.dragging_move:
            self.x -= dx * 2
            self.y += dy * 2

    def world_to_camera(self, x, y, z):

        x -= self.x
        y -= self.y
        z -= self.z

        cos_y = math.cos(self.yaw)
        sin_y = math.sin(self.yaw)

        rx = x * cos_y - z * sin_y
        rz = x * sin_y + z * cos_y

        x = rx
        z = rz

        cos_p = math.cos(self.pitch)
        sin_p = math.sin(self.pitch)

        ry = y * cos_p - z * sin_p
        rz = y * sin_p + z * cos_p

        return x, ry, rz
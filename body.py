class Body:

    def __init__(

        self,

        x, y, z,

        vx, vy, vz,

        mass,

        color

    ):

        self.x = x
        self.y = y
        self.z = z

        self.vx = vx
        self.vy = vy
        self.vz = vz

        self.mass = mass

        self.color = color

        
        # 궤적 저장
        # 절대 사라지지 않음

        self.trail = []

    def update_trail(self):

        self.trail.append(

            (
                self.x,
                self.y,
                self.z
            )

        )
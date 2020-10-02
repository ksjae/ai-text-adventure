class Head:
    pass
class Torso:
    pass
class Arm:
    pass
class Leg:
    pass
class Pose:
    standing = 0
    defending = 1
    off_balance = 2
    on_ground = 3
    extended = 4
class Anatomy:
    def __init__(self,
                head: Head,
                torso: Torso,
                arm: Arm,
                leg: Leg):

        self.pose = Pose.standing
        self.head = head
        self.torso = torso
        self.arm = arm
        self.leg = leg
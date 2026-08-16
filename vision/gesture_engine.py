import math


def distance(a, b):
    return math.sqrt(
        (a.x - b.x) ** 2 +
        (a.y - b.y) ** 2
    )


class GestureEngine:
    def __init__(self):
        self.previous_x = None

    def analyze(self, results):
        if not results.multi_hand_landmarks:
            self.previous_x = None

            return {
                "hands": 0,
                "pinch": False,
                "zoom": 0,
                "move_x": 0,
            }

        hands = results.multi_hand_landmarks

        # -------------------------
        # PINCH
        # -------------------------

        pinch = False

        for hand in hands:
            thumb = hand.landmark[4]
            index = hand.landmark[8]

            if distance(thumb, index) < 0.055:
                pinch = True

        # -------------------------
        # TWO HAND ZOOM
        # -------------------------

        zoom = 0

        if len(hands) == 2:
            left = hands[0].landmark[8]
            right = hands[1].landmark[8]

            d = distance(left, right)

            # Normalized distance
            zoom = int((d - 0.15) * 800)

            zoom = max(-100, min(100, zoom))

        # -------------------------
        # LEFT / RIGHT MOVEMENT
        # -------------------------

        center_x = sum(
            hand.landmark[9].x for hand in hands
        ) / len(hands)

        move_x = 0

        if self.previous_x is not None:
            delta = center_x - self.previous_x

            if abs(delta) > 0.015:
                move_x = delta * 1000

        self.previous_x = center_x

        return {
            "hands": len(hands),
            "pinch": pinch,
            "zoom": zoom,
            "move_x": move_x,
        }

import math
import sys

NAME = "Anna"
SURNAME = "Havula"
GROUP = "IT-32"

ROOM_L, ROOM_W, ROOM_H = 4.2, 3.5, 2.7
DOOR_W, DOOR_H = 0.9, 2.0
WINDOW_W, WINDOW_H = 1.4, 1.5
TILE_W, TILE_H = 0.30, 0.30
TILE_PRICE = 42.30

SPARE = 0.10
PAINT_L_PER_M2 = 1 / 10
LAYERS = 2
CAN_L = 2.5


def show(label, value):
    print(f"{label:<15}{value}")


def main():
    print(f"{NAME} {SURNAME}, {GROUP}")

    sizes = (ROOM_L, ROOM_W, ROOM_H, DOOR_W, DOOR_H, WINDOW_W, WINDOW_H,
             TILE_W, TILE_H, TILE_PRICE)
    if any(s <= 0 for s in sizes):
        print("error: all sizes and the price must be positive", file=sys.stderr)
        sys.exit(1)

    floor_area = ROOM_L * ROOM_W
    wall_area = (2 * (ROOM_L + ROOM_W) * ROOM_H
                 - DOOR_W * DOOR_H - WINDOW_W * WINDOW_H)
    if wall_area <= 0:
        print("error: door and window are larger than the walls", file=sys.stderr)
        sys.exit(1)

    floor_diag = math.hypot(ROOM_L, ROOM_W)
    room_diag = math.dist((0, 0, 0), (ROOM_L, ROOM_W, ROOM_H))

    show("room:", f"{ROOM_L} x {ROOM_W} x {ROOM_H} m")
    show("floor area:", f"{floor_area:.2f} m2")
    show("wall area:", f"{wall_area:.2f} m2 (without door and window)")
    show("floor diag:", f"{floor_diag:.2f} m")
    show("room diag:", f"{room_diag:.2f} m")
    print()

    tiles_exact = floor_area / (TILE_W * TILE_H)
    show("tiles exact:", f"{tiles_exact:.2f}")
    show("  round:", round(tiles_exact))
    show("  floor:", math.floor(tiles_exact))
    show("  ceil:", math.ceil(tiles_exact))

    tiles_to_buy = math.ceil(round(tiles_exact * (1 + SPARE), 9))
    show("tiles to buy:", f"{tiles_to_buy} (+{SPARE:.0%} spare)")

    paint_l = wall_area * PAINT_L_PER_M2 * LAYERS
    cans = math.ceil(round(paint_l / CAN_L, 9))
    show("paint:", f"{paint_l:.2f} l -> {cans} cans of {CAN_L} l")
    print()

    cost_mul = tiles_to_buy * TILE_PRICE
    cost_sum = 0.0
    for _ in range(tiles_to_buy):
        cost_sum += TILE_PRICE

    show("tiles cost:", f"{cost_mul:.2f} UAH")
    show("sum == mul:", cost_sum == cost_mul)
    show("isclose:", math.isclose(cost_sum, cost_mul))
    show("difference:", abs(cost_sum - cost_mul))


if __name__ == "__main__":
    main()
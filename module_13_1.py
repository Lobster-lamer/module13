import asyncio
from consoleTextStyle import ConsoleTextStyle as CoTeSt

BALLS_COUNT = 5


async def start_strongman(name: str, power: int):
    if 0 < power < 10:
        global BALLS_COUNT
        print(f"Качок {CoTeSt.colorful_str(name, CoTeSt.Color.CYAN)} начал соревнования")
        time_to_lift_up_the_ball = 10 - power
        for ball_number in range(1, BALLS_COUNT+1):
            await asyncio.sleep(time_to_lift_up_the_ball)
            print(f"Качок {CoTeSt.colorful_str(name, CoTeSt.Color.CYAN)} поднял шар №"
                  f"{CoTeSt.colorful_str(str(ball_number), CoTeSt.Color.BLUE)}")
        print(f"{CoTeSt.colorful_str(name, CoTeSt.Color.CYAN)} "
              f"{CoTeSt.Color.GREEN}закончил соревнования{CoTeSt.REGULAR}")


async def start_tournament():
    first_jock = asyncio.create_task(start_strongman("Man", 9))
    second_jock = asyncio.create_task(start_strongman("M'eh", 7))
    third_jock = asyncio.create_task(start_strongman("Dude", 8))
    await first_jock
    await second_jock
    await third_jock


asyncio.run(start_tournament())
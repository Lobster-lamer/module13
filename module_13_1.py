import asyncio
from consoleTextStyle import ConsoleTextStyle as CoTeSt

BALLS_COUNT = 5


async def start_strongman(name: str, power: int):
    if 0 < power < 10:
        global BALLS_COUNT
        print(f"Силач {CoTeSt.colorful_str(name, CoTeSt.Color.CYAN)} начал соревнования")
        time_to_lift_up_the_ball = 10 / power
        for ball_number in range(1, BALLS_COUNT+1):
            await asyncio.sleep(time_to_lift_up_the_ball)
            print(f"Силач {CoTeSt.colorful_str(name, CoTeSt.Color.CYAN)} поднял "
                  f"{CoTeSt.colorful_str(str(ball_number), CoTeSt.Color.BLUE)} шар")
        print(f"{CoTeSt.colorful_str(name, CoTeSt.Color.CYAN)} "
              f"{CoTeSt.Color.GREEN}закончил соревнования{CoTeSt.REGULAR}")


async def start_tournament():
    first_strongman = asyncio.create_task(start_strongman("Appolon", 5))
    second_strongman = asyncio.create_task(start_strongman("Denis", 4))
    third_strongman = asyncio.create_task(start_strongman("Pasha", 3))
    await first_strongman
    await second_strongman
    await third_strongman


asyncio.run(start_tournament())
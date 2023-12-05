import asyncio
import time

async def count():
    for i in range(10):
        print(i)
        await asyncio.sleep(0.5)

async def main():
    loop = asyncio.get_event_loop()

    task1 = loop.create_task(count())
    task2 = loop.create_task(count())

    await asyncio.gather(task1, task2)

if __name__ == "__main__":
    start = time.time()

    asyncio.run(main())

    end = time.time()
    print(end - start)

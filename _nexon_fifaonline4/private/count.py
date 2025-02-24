import asyncio


async def count_seconds():
    seconds = 0
    while True:
        print(f"경과 시간: {seconds}초")
        await asyncio.sleep(1)
        seconds += 1

async def main():
    try:
        await count_seconds()
    except KeyboardInterrupt:
        print("\n카운트가 중지되었습니다.")

if __name__ == "__main__":
    asyncio.run(main())
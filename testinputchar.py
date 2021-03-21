import asyncio
import ttyio5

async def main():
    ch = ttyio5.inputchar("prompt: ", "YN", "")

if __name__ == "__main__":
    asyncio.run(main())


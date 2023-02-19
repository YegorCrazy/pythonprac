import asyncio

async def prod():
    for i in range(5):
        val = f'value_{i + 1}'
        await q1.put(val)
        print(f'prod: put {val} to q1')
        await asyncio.sleep(1)

async def mid():
    while True:
        res = await q1.get()
        print(f'prod: get {res} from q1')
        await q2.put(res)
        print(f'prod: put {res} to q2')

async def cons():
    while True:
        res = await q2.get()
        print(f'prod: get {res} from q2')

async def main():
    await asyncio.gather(
        prod(),
        mid(),
        cons())

q1 = asyncio.Queue()
q2 = asyncio.Queue()

asyncio.run(main())

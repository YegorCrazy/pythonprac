import asyncio

def sqroots(coeffs: str) -> str:
    try:
        a, b, c = map(int, coeffs.split())
    except Exception as ex:
        raise ex
    if a == 0:
        raise ZeroDivisionError
    d = (b ** 2) - (4 * a * c)
    if d < 0:
        return ''
    elif d == 0:
        return str((-b) / (2 * a))
    elif d > 0:
        return ' '.join(map(str, sorted([((-b + d**0.5) / (2 * a)),
                                         ((-b - d**0.5) / (2 * a))])))


async def server_func(reader, writer):
    print('New client connected')
    while data := await reader.readline():
        data = data.decode()
        try:
            ans = sqroots(data)
        except Exception:
            ans = ''
        writer.write((ans + '\n').encode())
        print(f'Request: {data.strip()}, response: {ans}')
    print('Client is off')
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(server_func, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Server is down')

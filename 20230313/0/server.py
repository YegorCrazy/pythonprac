import asyncio

async def echo(reader, writer):
    try:
        while not reader.at_eof():
            data = await reader.readline()
            data = data.decode().split(maxsplit=1)
            if data == []:
                continue
            if data[0] == 'print':
                writer.write(data[1].encode())
            elif data[0] == 'info':
                info = data[1].strip()
                peer_info = writer.get_extra_info('peername')
                if info == 'host':
                    writer.write((peer_info[0] + '\n').encode())
                elif info == 'port':
                    writer.write((str(peer_info[1]) + '\n').encode())
            await writer.drain()
    except Exception as ex:
        print(ex)
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())

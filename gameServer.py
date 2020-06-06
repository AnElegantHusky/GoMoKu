from play.gamePlay import ChessBoard
import asyncio
import websockets
import socket

EMPTY = 0
BLACK = 1
WHITE = 2

playerPool = []
# matchPool = []
# socketPool = []

# def players_event():
#     return json.dumps({'type': 'users', 'count': len(playerPool)})
#
#
# async def notify_players():
#     if playerPool:
#         message = players_event()


async def GamePlay(blk_socket, blk_name, wht_socket, wht_name):
    board = ChessBoard()
    board.reset()
    player_info = "Info:{}:{}".format(blk_name, wht_name)
    print("    GamePlay: "+player_info)
    await blk_socket.send(player_info)
    await wht_socket.send(player_info)
    while True:
        try:
            blk_step = await blk_socket.recv()
            await wht_socket.send("Step:"+blk_step)
            print("      Step Black:"+blk_step)
            blk_step = blk_step.split(':')
            board.move(int(blk_step[0]), int(blk_step[1]), 'Black')
            if board.win(int(blk_step[0]), int(blk_step[1]), BLACK):
                await blk_socket.send("Done:"+blk_name)
                await wht_socket.send("Done:"+blk_name)
                break
            # await blk_socket.send("Cntn:")
            # await wht_socket.send("Cntn:")

            wht_step = await wht_socket.recv()
            await blk_socket.send("Step:"+wht_step)
            print("      Step White:"+wht_step)
            wht_step = wht_step.split(':')
            board.move(int(wht_step[0]), int(wht_step[1]), 'White')
            if board.win(int(wht_step[0]), int(wht_step[1]), WHITE):
                await blk_socket.send("Done:"+wht_name)
                await wht_socket.send("Done:"+wht_name)
                break
            # await blk_socket.send("Cntn:")
            # await wht_socket.send("Cntn:")
        except websockets.exceptions.ConnectionClosed:
            print("    GamePlay: ConnectionClosed:"+player_info[5:])
            break
    blk_socket.close()
    print("  Close Black: "+blk_name)
    # wht_socket.close()
        # blk_flag = await blk_socket.recv()
        # wht_flag = await wht_socket.recv()
        # if blk_flag == 'Rfus:' and wht_flag == 'Rfus:':
        #     break
        # elif blk_flag == 'Cntn:' and wht_flag == 'Cntn:':
        #     continue
        # elif blk_flag == 'Cntn:':
        #     playerPool.append((blk_socket, blk_name))
        # elif wht_flag == 'Cntn:':
        #     playerPool.append((wht_socket, wht_name))


async def register(websocket, name):
    if playerPool:
        opponent = playerPool.pop(0)
        op_socket = opponent[0]
        op_name = opponent[1]
        await GamePlay(op_socket, op_name, websocket, name)
    else:
        playerPool.append((websocket, name))


async def GoMoKu(websocket, path):
    name = await websocket.recv()
    name = name[5:]
    print("GoMoKu: "+websocket.remote_address[0]+str(websocket.remote_address[1])+'-->'+name)
    # while True:
    if len(playerPool) >= 1:
        opponent = playerPool.pop(0)
        op_socket = opponent[0]
        op_name = opponent[1]
        await GamePlay(op_socket, op_name, websocket, name)
        print("  Close White: "+name)
    else:
        print("  Waiting...")
        playerPool.append((websocket, name))
        await websocket.wait_closed()
        print("  Close Black: "+name)


start_server = websockets.serve(GoMoKu, "0.0.0.0", 6789)
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(start_server)
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
finally:
    loop.close()







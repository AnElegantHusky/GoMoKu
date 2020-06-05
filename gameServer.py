from play.gamePlay import ChessBoard
import asyncio
import websockets
import json

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
    await blk_socket.send(player_info)
    await wht_socket.send(player_info)
    while True:
        blk_step = await blk_socket.recv()
        await wht_socket.send("Step:"+blk_step)
        blk_step = blk_step.split(':')
        board.move(int(blk_step[0]), int(blk_step[1]), 'Black')
        if board.win(int(blk_step[0]), int(blk_step[1]), BLACK):
            await blk_socket.send("Done:"+blk_name)
            await wht_socket.send("Done:"+blk_name)
            return
        await blk_socket.send("Cntn:")
        await wht_socket.send("Cntn:")

        wht_step = await wht_socket.recv()
        await blk_socket.send("Step:"+wht_socket)
        wht_step = wht_step.split(':')
        board.move(int(wht_step[0]), int(wht_step[1]), 'White')
        if board.win(int(wht_step[0]), int(wht_step[1]), WHITE):
            await blk_socket.send("Done:"+wht_name)
            await wht_socket.send("Done:"+wht_name)
            return
        await blk_socket.send("Cntn:")
        await wht_socket.send("Cntn:")


async def register(websocket, name):
    if playerPool:
        opponent = playerPool.pop(0)
        op_socket = opponent[0]
        op_name = opponent[1]
        await GamePlay(op_socket, op_name, websocket, name)
    else:
        playerPool.append((websocket, name))


async def GoMoKu(websocket, path):
    print("here")
    name = await websocket.recv()
    print(websocket.remote_address[0]+' '+name)
    await register(websocket, name)
    # message = await websocket.recv()
    # print(f"< {message}")
    # while True:
    #     name = await websocket.recv()
    #     if name[0:5] == 'name:':
    #         if len(playerPool) == 0:
    #             # socketPool.append(websocket)
    #             playerPool.append((name[5:], websocket))
    #             while len(playerPool) == 1:
    #                 await asyncio.sleep(1)
    #         else:
    #             opponent = playerPool.pop(0)
    #             matchPool.append((opponent[0], opponent[1], websocket, name[5:]))
    #     break
    #
    # if len(playerPool) >= 2:


# async def waitForPlayer():
#     while len(playerPool) == 1:
#         await asyncio.sleep(1)
#     return

    # greeting = f"Hello {message}!"
    #
    # await websocket.send(greeting)
    # print(f"> {greeting}")

start_server = websockets.serve(GoMoKu, 'localhost', 6789)
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(start_server)
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
finally:
    loop.close()







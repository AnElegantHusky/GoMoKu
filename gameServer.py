from play.gamePlay import ChessBoard
import asyncio
import websockets

EMPTY = 0
BLACK = 1
WHITE = 2

# waiting players
playerPool = []

# control the GoMoKu game play
async def GamePlay(black_socket, black_name, white_socket, white_name):
    try:
        # init a new game
        board = ChessBoard()
        player_info = "Info:{}:{}".format(black_name, white_name)
        print("    GamePlay: "+player_info)
        # await blk_socket.send(player_info)
        # await wht_socket.send(player_info)
        while True:
            # waiting for black player
            while True:
                black_step = await black_socket.recv()
                black_step = black_step.split(':')
                black_x = int(black_step[0])
                black_y = int(black_step[1])
                if board.board[black_x][black_y] == EMPTY:
                    break
            # await wht_socket.send("Step:"+blk_step)
            print("      Step Black: {},{}".format(black_x, black_y))
            # blk_step = blk_step.split(':')
            board.move(black_x, black_y, 'Black')
            await black_socket.send("Step:" + board.sequence())
            await white_socket.send("Step:" + board.sequence())
            if board.win(black_x, black_y, BLACK):
                await black_socket.send("Done:"+black_name)
                await white_socket.send("Done:"+black_name)
                break

            # white player move
            while True:
                white_step = await white_socket.recv()
                white_step = white_step.split(':')
                white_x = int(white_step[0])
                white_y = int(white_step[1])
                if board.board[white_x][white_y] == EMPTY:
                    break
            # await wht_socket.send("Step:"+blk_step)
            print("      Step White: {},{}".format(white_x, white_y))
            # blk_step = blk_step.split(':')
            board.move(white_x, white_y, 'White')
            await black_socket.send("Step:" + board.sequence())
            await white_socket.send("Step:" + board.sequence())
            if board.win(white_x, white_y, WHITE):
                await black_socket.send("Done:" + white_name)
                await white_socket.send("Done:" + white_name)
                break
    except (KeyboardInterrupt, websockets.exceptions.ConnectionClosed, websockets.exceptions.ConnectionClosedOK):
        try:
            print("    GamePlay: ConnectionClosed:"+ player_info[5:])
            await black_socket.send("Lost:")
            await white_socket.send("Lost:")
        except:
            return
        return

# every websocket from browser will create a new coroutine 
async def main(websocket):
    socket_list = [i[0] for i in playerPool]
    if websocket in socket_list:
        return

    op_socket = websocket
    try:
        message = await websocket.recv()
        name = message[5:]
        print("GoMoKu: "+websocket.remote_address[0]+':'+str(websocket.remote_address[1])+'-->'+name)

        # if players are waiting, then start a game
        #    and this player will be White
        if len(playerPool) >= 1 and (websocket, name) not in playerPool:
            opponent = playerPool.pop(0)
            op_socket = opponent[0]
            op_name = opponent[1]

            board = ChessBoard()
            # lock = asyncio.Lock()

            player_info = "Info:{}:{}".format(op_name, name)
            print("    GamePlay: " + player_info)
            await op_socket.send(player_info)
            await websocket.send(player_info)
            await GamePlay(op_socket, op_name, websocket, name)
            return
        else:
            print("  Waiting...")
            playerPool.append((websocket, name))
            await websocket.wait_closed()
            print("  Close Black: "+name)
    except (KeyboardInterrupt, websockets.exceptions.ConnectionClosed, websockets.exceptions.ConnectionClosedOK):
        print("    GoMoKu: ConnectionClosed:"+ player_info[5:])
        return

start_server = websockets.serve(main, "0.0.0.0", 6791)
loop = asyncio.get_event_loop()
print("game listening 0.0.0.0:6791")
try:
    loop.run_until_complete(start_server)
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
finally:
    loop.close()


# async def blackPlayer(player_socket, player_name, opponent_socket, opponent_name, board, lock=None):
#     player_info = "Info:{}:{}".format(opponent_name, player_name)
#     # black player's first step
#     # async with lock:
#     print("debug: black player get first lock")
#     # first_step = await player_socket.recv()
#     first_step = "2:3"
#     print("      Step Black:" + first_step)
#     black_location = first_step.split(':')
#     board.move(int(black_location[0]), int(black_location[1]), 'Black')
#
#     # sync board with players
#     await player_socket.send("Step:" + board.sequence())
#     await opponent_socket.send("Step:" + board.sequence())
#         # yield
#     try:
#         while True:
#             if board.finish is True:
#                 winner_name = player_name if board.winner == BLACK else opponent_name
#                 await player_socket.send("Done:" + winner_name)
#                 await opponent_socket.send("Done:" + winner_name)
#                 return
#             # wait for white move
#             if board.step_count % 2 == 1:
#                 continue
#                 # yield
#             # wait for lock
#             else:
#                 # async with lock:
#                 print("debug: black player get lock")
#                 x = 0
#                 y = 0
#                 while True:
#                     step = await player_socket.recv()
#                     location = step.split(':')
#                     x = int(location[0])
#                     y = int(location[1])
#                     if board.board[x][y] == 0:
#                         break
#                 print("      Step Black: {},{}".format(x, y))
#                 board.move(x, y, 'Black')
#                 await player_socket.send("Step:" + board.sequence())
#                 await opponent_socket.send("Step:" + board.sequence())
#                 if board.win(x, y, BLACK):
#                     await player_socket.send("Done:" + player_name)
#                     await opponent_socket.send("Done:" + player_name)
#                     return
#                 # yield
#     except (websockets.exceptions.ConnectionClosed, websockets.exceptions.ConnectionClosedOK):
#         print("    GamePlay: ConnectionClosed:" + player_info[5:])
#
#
# async def whitePlayer(player_socket, player_name, opponent_socket, opponent_name, board, lock=None):
#     print("debug: white player init")
#     player_info = "Info:{}:{}".format(opponent_name, player_name)
#     try:
#         while True:
#             if board.finish is True:
#                 winner_name = player_name if board.winner == WHITE else opponent_name
#                 await player_socket.send("Done:" + winner_name)
#                 await opponent_socket.send("Done:" + winner_name)
#                 return
#
#             if board.step_count % 2 == 0:
#                 continue
#                 # yield
#             # wait for lock
#             else:
#                 # async with lock:
#
#                 # while True:
#                 #     step = await player_socket.recv()
#                 #     location = step.split(':')
#                 #     x = int(location[0])
#                 #     y = int(location[1])
#                 #     if board.board[x][y] == 0:
#                 #         break
#                 # print("      Step White: {},{}".format(x, y))
#
#                 x = 0
#                 y = 6
#
#                 board.move(x, y, 'White')
#                 await player_socket.send("Step:" + board.sequence())
#                 await opponent_socket.send("Step:" + board.sequence())
#                 if board.win(x, y, WHITE):
#                     await player_socket.send("Done:" + player_name)
#                     await opponent_socket.send("Done:" + player_name)
#                     return
#                 # yield
#     except (websockets.exceptions.ConnectionClosed, websockets.exceptions.ConnectionClosedOK):
#         print("    GamePlay: ConnectionClosed:" + player_info[5:])
#
#
# async def main():
#     loop = asyncio.get_running_loop()
#     stop = loop.create_future()
#     try:
#         # port = int(os.environ.get("PORT", "6789"))
#         async with websockets.serve(GoMoKu, "", "6791"):
#             await stop
#     except KeyboardInterrupt:
#         loop.close()
#
# # main event loop
# # init websocket and event loop
# if __name__ == "__main__":
#     asyncio.run(main())


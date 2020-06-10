var url = "ws://47.95.0.1:6789"
var socket = new WebSocket(url)
socket.onmessage = function(evt) { onMessage(evt) }
var yourColor = 0
var yourName = ''
var blackName = ''
var whiteName = ''
var turn = 0 // 0: black turn; 1: white turn
var board = []
var empty = 0
var black = 1
var white = 2
var winner = ''

// init ChessBoard when page loaded, then draw the board
window.onload = function game() {
  for (var i = 0; i < 10; i++) {
    board[i] = []
    for (var j = 0; j < 10; j++) {
      board[i][j] = 0
    }
  }
  var left = 0
  var top = 0
  for (var i = 0; i < 10; i++) {
    left = 0
    for (var j = 0; j < 10; j++) {
      var image = document.createElement("img");
      var canvas = document.getElementById("chessBoard")
      image.src = "background.png"
      image.setAttribute("id", i.toString()+":"+j.toString())
      image.style = "width:40px;height:40px;position:absolute;border:1px solid black; \
            left:"+left.toString()+"px;top:"+top.toString()+"px;"
      // image.onclick = "clickBoard"
      canvas.appendChild(image);
      left += 40
    }
    top += 40
  }
}

// player input name, waiting for a new game
function initPlayer(event) {
  var name = document.getElementById("name").value;
  if (name != "") {
    // alert(name)
    socket.send("name:" + name)
    yourName = name
    var div = document.getElementById("name")
    div.parentNode.removeChild(div)
    div = document.getElementById("submit-btn")
    div.parentNode.removeChild(div)
    div = document.getElementById("wait-player")
    div.style = "display:true;"
  }
}



// when (row, col) is empty and it's this player's turn, player can make a move
//     draw the new legal move
function clickBoard(event) {
  if (yourColor == turn + 1) {
    var image = document.getElementById(event.target.id)
    var tuple = event.target.id.split(":")
    var row = tuple[0]
    var col = tuple[1]
    if (board[row][col] == 0) {
      socket.send(event.target.id)
      board[row][col] = yourColor
      turn = (turn + 1) % 2
      if (yourColor == black) {
        image.src = "blackStone.png"
      }
      else {
        image.src = "whiteStone.png"
      }
    }
  }
}

// when websocket receive a new message, extract the opcode and data
//     Info: a new game start and init opponent's information
//     Step: a move from opponent
//     Done: someone win the game
function onMessage(event) {
  var message = event.data
  var opcode = message.substring(0, 5)
  var data = message.substring(5)

  if (opcode == 'Info:') {
    div = document.getElementById("wait-player")
    div.style = "display:none;"
    player = data.split(':')
    blackName = player[0]
    whiteName = player[1]
    if (yourName == player[0]) {
      yourColor = black
    }
    else if (yourName == player[1]) {
      yourColor = white
    }
    var div = document.getElementById("black-player")
    div.textContent = "Black: "+blackName
    div = document.getElementById("white-player")
    div.textContent = "White: "+whiteName
    turn = 0
  }

  if (opcode == 'Step:') {
    step = data.split(':')
    row = parseInt(data[0])
    col = parseInt(data[1])
    board[row][col] = turn + 1
    var image = document.getElementById(data)
    if (yourColor == black) {
      image.src = "whiteStone.png"
    }
    else {
      image.src = "blackStone.png"
    }
    turn = (turn + 1) % 2
  }

  if (opcode == 'Done:') {
    var div = document.getElementById("winner")
    div.textContent = "Winner: "+data
    alert(div.textContent)
    winner = data
    turn = -2
    setTimeout(continueGame(), 1000)
  }
}

// when game over, websocket will be closed
//     so init a new websocket in continueGame
function continueGame() {
  socket.close()
  socket = new WebSocket(url)
  for (var i = 0; i < 10; i++) {
    board[i] = []
    for (var j = 0; j < 10; j++) {
      board[i][j] = 0
      var image = document.getElementById(i.toString() + ':' + j.toString())
      image.src = "background.png"
    }
  }
  blackName = ''
  whiteName = ''
  turn = 0
  yourColor = 0
  var div = document.getElementById("black-player")
  div.textContent = "Black: "
  div = document.getElementById("white-player")
  div.textContent = "White: "
  div = document.getElementById("winner")
  div.textContent = "Winner: "

  // wait until connection established
  waitForSocketConnection(socket, function () {
    console.log("new game begin")
    socket.onmessage = function (evt) {
      onMessage(evt)
    }
    socket.send("name:" + yourName)
  })
}


// wait for socket connection
function waitForSocketConnection(socket, callback) {
  setTimeout(
    function () {
      if (socket.readyState === 1) {
        console.log("Connection is made")
        if (callback != null) {
          callback()
        }
        return
      } else {
        console.log("wait for connection...")
        waitForSocketConnection(socket, callback)
      }
    }, 5)
}

  // while (1) {
  //   var readyState = socket.readyState
  //   if (readyState == WebSocket.OPEN) {
  //     break
  //   }

  // }
  // socket.send("name:"+name)

    // socket.send("Cntn:")
  // }


// function refuseGame(event) {
//   // if (winner != '') {
//     // socket.send("Rfus:")
//   socket.close();
//   // }
// }

// // draw ChessBoard
// function drawBoard()
// {
//   var left = 0
//   var top = 0
//   for (var i = 0; i < 10; i++) {
//     left = 0
//     for (var j = 0; j < 10; j++) {
//       var image = document.createElement("img");
//       var canvas = document.getElementById("chessBoard")
//       image.src = "background.png"
//       image.setAttribute("id", i.toString()+":"+j.toString())
//       image.style = "width:40px;height:40px;position:absolute;border:1px solid black; \
//             left:"+left.toString()+"px;top:"+top.toString()+"px;"
//       // image.onclick = "clickBoard"
//       canvas.appendChild(image);
//       left += 40
//     }
//     top += 40
//   }
// }
var url = "ws://localhost:6791"
var socket = new WebSocket(url)
socket.onmessage = function(evt) { onMessage(evt) }
var yourColor = 0
var yourName = ''
var blackName = ''
var whiteName = ''
var step_count = 0 //
var board = []
var empty = 0
var black = 1
var white = 2
var winner = ''

// init ChessBoard when page loaded, then draw the board
window.onload = function game() {
  step_count = 0
  blackName = ''
  whiteName = ''
  div = document.getElementById("black-player")
  div.textContent = "Black: "
  div = document.getElementById("white-player")
  div.textContent = "White: "
  var name_div = document.getElementById("name")
  name_div.style.visibility = 'visible'
  var submit_div = document.getElementById("submit-btn")
  submit_div.style.visibility = 'visible'
  var wait_div = document.getElementById("wait-player")
  wait_div.style.visibility = 'hidden'

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
      image.src = "./images/background.png"
      image.setAttribute("id", i.toString()+":"+j.toString())
      image.style = "width:40px;height:40px;position:absolute;border:1px solid black; \
            left:"+left.toString()+"px;top:"+top.toString()+"px;"
      image.onclick = "clickBoard"
      canvas.appendChild(image);
      left += 40
    }
    top += 40
  }
}

// draw board on web page based on the board sequence
function drawBoard(board_sequence) {
  var board_array = board_sequence.split(',')
  var index = 0
  for (var i = 0; i < 10; i++) {
    for (var j = 0; j < 10; j++) {
      var image = document.getElementById(i.toString()+":"+j.toString());
      const color = parseInt(board_array[index])
      board[i][j] = color
      if (color === 0) {
        image.src = "./images/background.png"
      }
      if (color === 1) {
        image.src = "./images/blackStone.png"
      }
      if (color === 2) {
        image.src = "./images/whiteStone.png"
      }
      index += 1
    }
  }
}

// player input name, waiting for a new game
function initPlayer(event) {
  var name = document.getElementById("name").value;
  if (name != "") {
    // alert(name)
    socket.send("name:" + name)
    yourName = name
    var name_div = document.getElementById("name")
    // name_div.parentNode.removeChild(name_div)
    name_div.style.visibility = 'hidden'
    var submit_div = document.getElementById("submit-btn")
    // submit_div.parentNode.removeChild(submit_div)
    submit_div.style.visibility = 'hidden'
    var wait_div = document.getElementById("wait-player")
    wait_div.style.visibility = 'visible'
  }
}




// when (row, col) is empty and it's this player's turn, player can make a move
function clickBoard(event) {
  if (yourColor == 1 + (step_count % 2)) {
    // var image = document.getElementById(event.target.id)
    var tuple = event.target.id.split(":")
    var row = tuple[0]
    var col = tuple[1]
    if (board[row][col] == 0) {
      socket.send(row.toString() + ':' + col.toString())
      }
    }
  }


// when websocket receive a new message, extract the opcode and data
//     Info: a new game start and init opponent's information
//     Step: confirm a move and update the board
//     Done: someone win the game
//     Lost: handle connection lost, but not fully implemented
function onMessage(event) {
  var message = event.data
  var opcode = message.substring(0, 5)
  var data = message.substring(5)

  if (opcode == 'Info:') {
    var div = document.getElementById("wait-player")
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
    div = document.getElementById("black-player")
    div.textContent = "Black: "+blackName
    div = document.getElementById("white-player")
    div.textContent = "White: "+whiteName
    step_count = 0
  }

  if (opcode == 'Step:') {
    drawBoard(data)
    step_count = (step_count + 1) % 2
  }

  if (opcode == 'Done:') {
    var div = document.getElementById("winner")
    div.textContent = "Winner: "+data
    alert(div.textContent)
    winner = data
    step_count = 0
    window.onload()
  }

  if (opcode == 'Lost') {
    alert("Connection Lost")
    // winner = data
    // step_count = 0
    window.onload()
  }
}

setInterval(function () {
  if (socket.readyState === WebSocket.CLOSED) {
    alert("Connection Lost")
    window.onload()
  }
}, 5000)

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

// // when game over, websocket will be closed
// //     so init a new websocket in continueGame
// function continueGame() {
//   socket.close()
//   socket = new WebSocket(url)
//   for (var i = 0; i < 10; i++) {
//     board[i] = []
//     for (var j = 0; j < 10; j++) {
//       board[i][j] = 0
//       var image = document.getElementById(i.toString() + ':' + j.toString())
//       image.src = "./images/background.png"
//     }
//   }
//   blackName = ''
//   whiteName = ''
//   step_count = 0
//   yourColor = 0
//   var div = document.getElementById("black-player")
//   div.textContent = "Black: "
//   div = document.getElementById("white-player")
//   div.textContent = "White: "
//   div = document.getElementById("winner")
//   div.textContent = "Winner: "
//
//   // wait until connection established
//   waitForSocketConnection(socket, function () {
//     console.log("new game begin")
//     socket.onmessage = function (evt) {
//       onMessage(evt)
//     }
//     socket.send("name:" + yourName)
//   })
// }



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
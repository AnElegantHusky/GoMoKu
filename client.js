var url = "ws://47.95.0.1:6789"
var socket = new WebSocket(url)
var websocket
var yourColor = 0
var yourName = ''
var blackName = ''
// var oppoColor
var whiteName = ''
var turn = 0 // 0: black turn; 1: white turn
var board = []
var empty = 0
var black = 1
var white = 2
var winner = ''

window.onload = function game() {
  for (var i = 0; i < 10; i++) {
    board[i] = []
    for (var j = 0; j < 10; j++) {
      board[i][j] = 0
    }
  }
  this.drawBoard()
  // var div = document.getElementById("wait-player")
  // div.style = "display:true;"
}

function initPlayer(event) {
  var name = document.getElementById("name").value;
  if (name != "")
  {
    // alert(name)
    socket.send("name:"+name)
    yourName = name
    var div = document.getElementById("name")
    div.parentNode.removeChild(div)
    div = document.getElementById("submit-btn")
    div.parentNode.removeChild(div)
    div = document.getElementById("wait-player")
    div.style = "display:true;"
  }
  
}

function drawBoard()
{
  // this.alert("drawBoard")
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

// function updateBoard() {
//   for (var i = 0; i < 10; i++) {
//     for (var j = 0; j < 10; j++)
//   }
// }

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
      // drawBoard()
    }
  }
}

// socket.onopen = function(event) {
//   socket.send("hello")
// }

socket.onmessage = function(event) {
  var message = event.data
  alert(message)
  // alert(message)
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
    var div = document.getElementById("winnerr")
    div.textContent = "Winner: "+data
    winner = data
  }
}

function continueGame(event) {
  // if (winner != '') {
  socket.close()
  socket = new WebSocket(url)
  game()
  initPlayer()
    // socket.send("Cntn:")
  // }
}

function continueGame(event) {
  // if (winner != '') {
    // socket.send("Rfus:")
  socket.close();
  // }
}
# Botwars

A logic and validation module for a RISK like game built for a hackhaton competition.

## Rules

- The game is played by two player bots on an 8x8 grid. 
- The objective is to occupy the whole grid.
- The game is turn based (i.e `bot1 -> server -> bot2 -> server -> bot1 -> ...`
- Bots start at the top left and bottom right corners.

- Bots get 5 soldiers at the start of the game. 
- At the end of each turn, 1 soldier is added per each grid cell owned by the player. 
- Bots can move any number of soldiers from a cell they own to any nearby cell, except a blocked cell.
- Movement is allowed in all  8 directions
- No movement is also allowed
- When moving to an enemy cell, the player with most soldiers wins.
- The defeated side loses all soldiers, the wining side loses as many soldiers as the enemy had. 
- The attacker can also be defeated. 

```
let socket = io.connect('http://192.168.0.254:7000');
    socket.emit("finish-turn", {"user":user, "moves":moves});
socket.on('turn-' + user, function (board) {}
socket.emit("finish-turn", {"user":user, "moves":moves});
socket.emit("connect-game", user);


 move = {"num", "prev_x", "prev_y", "next_x", "next_y" };
```



```json
{
	"board":[
		[5,0,0,0,0,0,0,0],
		[-1,0,0,0,0,0,0,0],
		[0,0,NaN,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,NaN,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,-5]]
    
	"moves":[
		[2,0,0,0,1],
		[2,0,0,1,0]]
}

```

```
{"board":[[1,2,0,0,0,0,0,0],[1,0,0,0,0,0,0,0],[0,0,NaN,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,NaN,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,-5]],"ok":1,"win":0}
```








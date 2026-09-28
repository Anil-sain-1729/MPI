const cells=[...document.querySelectorAll(".cell")],boardEl=document.getElementById("board"),lineEl=document.getElementById("winLine"),statusEl=document.getElementById("status");
const humanMode=document.getElementById("humanMode"),robotMode=document.getElementById("robotMode"),symbol=document.getElementById("symbol"),difficulty=document.getElementById("difficulty"),difficultyBox=document.getElementById("difficultyBox"),opponent=document.getElementById("opponent");
const humanScore=document.getElementById("humanScore"),robotScore=document.getElementById("robotScore");
const wins=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
let board=Array(9).fill(""),current="X",gameOver=false,mode="robot",human="X",robot="O",history=[],scores={human:0,robot:0};

function render(){cells.forEach((c,i)=>{c.textContent=board[i];c.className="cell";if(board[i])c.classList.add(board[i].toLowerCase())})}
function check(b=board){for(let n=0;n<wins.length;n++){let[a,c,d]=wins[n];if(b[a]&&b[a]===b[c]&&b[a]===b[d])return{winner:b[a],line:n}}return b.every(Boolean)?{winner:"draw",line:-1}:null}
function available(b=board){return b.map((v,i)=>v?null:i).filter(i=>i!==null)}
function status(t,lose=false){statusEl.textContent=t;statusEl.style.background=lose?"#ffe0e5":"#d7f5df";statusEl.style.color=lose?"#d51e3b":"#0b8a35"}
function turn(){status(mode==="robot"?(current===human?"Your Turn":"Robot's Turn"):`Player ${current}'s Turn`)}
function drawLine(n){let[a,,c]=wins[n],r1=cells[a].getBoundingClientRect(),r2=cells[c].getBoundingClientRect(),br=boardEl.getBoundingClientRect();let x=r1.left+r1.width/2-br.left,y=r1.top+r1.height/2-br.top,x2=r2.left+r2.width/2-br.left,y2=r2.top+r2.height/2-br.top;lineEl.style.width=Math.hypot(x2-x,y2-y)+"px";lineEl.style.left=x+"px";lineEl.style.top=y-4+"px";lineEl.style.transform=`rotate(${Math.atan2(y2-y,x2-x)*180/Math.PI}deg)`;lineEl.classList.add("show")}
function move(i,p){if(board[i]||gameOver)return false;history.push([...board]);board[i]=p;render();return true}
function finish(){let r=check();if(!r){current=current==="X"?"O":"X";turn();return}gameOver=true;if(r.winner==="draw"){status("Game Draw!");return}drawLine(r.line);if(mode==="robot"&&r.winner===robot){scores.robot++;status("Robot Wins!",true)}else{scores.human++;status(mode==="robot"?"You Win!":`Player ${r.winner} Wins!`)}updateScore()}
function updateScore(){humanScore.textContent=scores.human;robotScore.textContent=scores.robot}
function newGame(){board=Array(9).fill("");history=[];gameOver=false;lineEl.classList.remove("show");render();current="X";turn();if(mode==="robot"&&human==="O")setTimeout(robotMove,350)}
function winningMove(p){for(let i of available()){let b=[...board];b[i]=p;if(check(b)?.winner===p)return i}return null}
function minimax(b,max){let r=check(b);if(r?.winner===robot)return 10;if(r?.winner===human)return -10;if(r?.winner==="draw")return 0;let best=max?-Infinity:Infinity;for(let i of available(b)){b[i]=max?robot:human;let s=minimax(b,!max);b[i]="";best=max?Math.max(best,s):Math.min(best,s)}return best}
function bestMove(){let best=-Infinity,m=available()[0];for(let i of available()){board[i]=robot;let s=minimax(board,false);board[i]="";if(s>best){best=s;m=i}}return m}
function robotMove(){if(mode!=="robot"||gameOver||current!==robot)return;let a=available(),m;if(difficulty.value==="easy")m=a[Math.floor(Math.random()*a.length)];else if(difficulty.value==="medium")m=winningMove(robot)??winningMove(human)??(Math.random()<.5?a[Math.floor(Math.random()*a.length)]:bestMove());else m=bestMove();move(m,robot);finish()}
cells.forEach(c=>c.addEventListener("click",()=>{if(gameOver||(mode==="robot"&&current!==human))return;let i=+c.dataset.i;if(move(i,current)){finish();if(mode==="robot"&&!gameOver&&current===robot)setTimeout(robotMove,350)}}));
humanMode.onclick=()=>{mode="human";humanMode.classList.add("active");robotMode.classList.remove("active");difficultyBox.style.visibility="hidden";opponent.textContent="Player 2";human="X";robot="O";newGame()};
robotMode.onclick=()=>{mode="robot";robotMode.classList.add("active");humanMode.classList.remove("active");difficultyBox.style.visibility="visible";opponent.textContent="Robot";human=symbol.value;robot=human==="X"?"O":"X";newGame()};
symbol.onchange=()=>{human=symbol.value;robot=human==="X"?"O":"X";newGame()};
document.getElementById("newGame").onclick=newGame;
document.getElementById("resetScore").onclick=()=>{scores={human:0,robot:0};updateScore();newGame()};
document.getElementById("undo").onclick=()=>{if(!history.length||gameOver)return;board=history.pop();if(mode==="robot"&&history.length)board=history.pop();render();lineEl.classList.remove("show");gameOver=false;current=mode==="robot"?human:"X";turn()};
window.onresize=()=>{let r=check();if(r&&r.winner!=="draw"&&gameOver)drawLine(r.line)};
difficultyBox.style.visibility="visible";newGame();

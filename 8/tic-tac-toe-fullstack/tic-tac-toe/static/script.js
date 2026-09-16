let game=null,busy=false;

const cells=document.querySelectorAll(".cell");
const turn=document.getElementById("turn");
const statusText=document.getElementById("status");
const scoreX=document.getElementById("scoreX");
const scoreO=document.getElementById("scoreO");
const scoreDraw=document.getElementById("scoreDraw");
const oName=document.getElementById("oName");
const computerMode=document.getElementById("computerMode");
const playerMode=document.getElementById("playerMode");
const winLine=document.getElementById("winLine");
const modal=document.getElementById("modal");
const resultIcon=document.getElementById("resultIcon");
const resultTitle=document.getElementById("resultTitle");
const resultText=document.getElementById("resultText");

async function load(){
    try{
        const r=await fetch("/api/state");
        const d=await r.json();
        game=d.game;
        render();
    }catch(e){
        statusText.textContent="Could not connect to Python backend.";
    }
}
load();

function render(){
    if(!game)return;

    cells.forEach((cell,i)=>{
        const v=game.board[i];
        cell.textContent=v;
        cell.classList.remove("x","o","winner");
        if(v)cell.classList.add(v.toLowerCase());
    });

    scoreX.textContent=game.score.X;
    scoreO.textContent=game.score.O;
    scoreDraw.textContent=game.score.draw;
    oName.textContent=game.mode==="computer"?"COMPUTER O":"PLAYER O";

    computerMode.classList.toggle("active",game.mode==="computer");
    playerMode.classList.toggle("active",game.mode==="player");

    if(!game.game_over){
        turn.textContent=`Player ${game.current}'s Turn`;
        statusText.textContent=
            game.mode==="computer"&&game.current==="O"
            ?"Computer is thinking..."
            :"Choose an empty box.";
    }
}

cells.forEach(cell=>{
    cell.addEventListener("click",()=>makeMove(Number(cell.dataset.index)));
});

async function makeMove(position){
    if(busy||!game||game.game_over)return;
    if(game.mode==="computer"&&game.current==="O")return;

    if(game.board[position]){
        statusText.textContent="This box is already occupied.";
        return;
    }

    busy=true;

    try{
        const r=await fetch("/api/move",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({position})
        });

        const d=await r.json();

        if(!d.success){
            statusText.textContent=d.message;
            return;
        }

        game=d.game;
        render();

        if(d.winner){
            showResult(d.winner,d.combination);
            return;
        }

        if(d.computer_move!==undefined){
            const ai=cells[d.computer_move];
            ai.style.transform="scale(1.08)";
            setTimeout(()=>ai.style.transform="",300);
        }

    }catch(e){
        statusText.textContent="Python server error.";
    }finally{
        busy=false;
        render();
    }
}

function showResult(winner,combo){
    if(winner==="draw"){
        resultIcon.textContent="🤝";
        resultTitle.textContent="It's a Draw!";
        resultText.textContent="Nobody won this round.";
    }else{
        combo.forEach(i=>cells[i].classList.add("winner"));
        drawLine(combo);

        if(winner==="X"){
            resultIcon.textContent="🏆";
            resultTitle.textContent="Player X Wins!";
            resultText.textContent="Congratulations!";
        }else{
            resultIcon.textContent="🤖";
            resultTitle.textContent=game.mode==="computer"?"Computer Wins!":"Player O Wins!";
            resultText.textContent="This round is over.";
        }
    }

    setTimeout(()=>modal.classList.remove("hidden"),500);
}

function drawLine(combo){
    const a=cells[combo[0]].getBoundingClientRect();
    const c=cells[combo[2]].getBoundingClientRect();
    const board=document.getElementById("board");
    const r=board.getBoundingClientRect();

    const x1=a.left-r.left+a.width/2;
    const y1=a.top-r.top+a.height/2;
    const x2=c.left-r.left+c.width/2;
    const y2=c.top-r.top+c.height/2;
    const len=Math.hypot(x2-x1,y2-y1);
    const angle=Math.atan2(y2-y1,x2-x1)*180/Math.PI;

    winLine.style.display="block";
    winLine.style.width=`${len}px`;
    winLine.style.left=`${x1}px`;
    winLine.style.top=`${y1}px`;
    winLine.style.transform=`rotate(${angle}deg)`;
}

document.getElementById("newGame").addEventListener("click",newGame);
document.getElementById("playAgain").addEventListener("click",newGame);

async function newGame(){
    if(busy)return;

    const mode=game?game.mode:"computer";

    const r=await fetch("/api/new-game",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({mode})
    });

    const d=await r.json();
    game=d.game;
    modal.classList.add("hidden");
    winLine.style.display="none";
    cells.forEach(c=>c.classList.remove("winner"));
    render();
}

computerMode.addEventListener("click",()=>changeMode("computer"));
playerMode.addEventListener("click",()=>changeMode("player"));

async function changeMode(mode){
    if(busy)return;

    const r=await fetch("/api/new-game",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({mode})
    });

    const d=await r.json();
    game=d.game;
    modal.classList.add("hidden");
    winLine.style.display="none";
    render();
}

document.getElementById("resetScore").addEventListener("click",async()=>{
    if(busy)return;
    const r=await fetch("/api/reset-score",{method:"POST"});
    const d=await r.json();
    game=d.game;
    render();
});

window.addEventListener("resize",()=>{
    if(game&&game.winner&&game.winner!=="draw"){
        const combo=findWin(game.board);
        if(combo.length)drawLine(combo);
    }
});

function findWin(board){
    const wins=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
    return wins.find(c=>board[c[0]]&&board[c[0]]===board[c[1]]&&board[c[1]]===board[c[2]])||[];
}

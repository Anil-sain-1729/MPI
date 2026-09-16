const pieces = {
  K:"♔", Q:"♕", R:"♖", B:"♗", N:"♘", P:"♙",
  k:"♚", q:"♛", r:"♜", b:"♝", n:"♞", p:"♟"
};

let game = null;
let selected = null;

async function api(url, options={}) {
  const r = await fetch(url, {headers: {"Content-Type":"application/json"}, ...options});
  const data = await r.json();
  if (!r.ok) throw new Error(data.error || "Request failed");
  return data;
}

function render() {
  const board = document.getElementById("board");
  board.innerHTML = "";
  const legal = selected ? getLegalFromSelected() : [];

  for(let r=0;r<8;r++){
    for(let c=0;c<8;c++){
      const s=document.createElement("div");
      s.className="square "+((r+c)%2===0?"light":"dark");
      if(selected && selected[0]===r && selected[1]===c) s.classList.add("selected");
      if(game.last_move && ((game.last_move[0]===r&&game.last_move[1]===c)||(game.last_move[2]===r&&game.last_move[3]===c))) s.classList.add("last");
      const target=legal.find(x=>x[0]===r&&x[1]===c);
      if(target){
        if(game.board[r][c]===".") s.classList.add("legal"); else s.classList.add("capture");
      }
      const p=game.board[r][c];
      if(p!=="."){
        const span=document.createElement("span");
        span.className="piece";
        span.textContent=pieces[p];
        s.appendChild(span);
      }
      s.onclick=()=>clickSquare(r,c);
      board.appendChild(s);
    }
  }

  document.getElementById("turn").textContent=game.turn==="w"?"White":"Black";
  let msg = game.turn==="w"?"White to move":"Black to move";
  if(game.status==="check") msg += " — CHECK!";
  if(game.status==="checkmate") msg = `${game.winner==="w"?"White":"Black"} wins by checkmate!`;
  if(game.status==="draw") msg = "Draw — stalemate.";
  document.getElementById("status").textContent=msg;
  renderHistory();
  if(game.status==="checkmate" || game.status==="draw") showModal();
}

function getLegalFromSelected(){
  // Frontend only mirrors basic movement highlighting; backend remains authoritative.
  const [r,c]=selected, p=game.board[r][c], out=[];
  const side=game.turn;
  if((side==="w" && p!==p.toUpperCase()) || (side==="b" && p!==p.toLowerCase())) return out;
  const P=p.toLowerCase();
  const add=(rr,cc)=>{
    if(rr<0||rr>7||cc<0||cc>7)return;
    const t=game.board[rr][cc];
    if(t==="." || (side==="w"?t===t.toLowerCase():t===t.toUpperCase())) out.push([rr,cc]);
  };
  if(P==="p"){
    const d=side==="w"?-1:1, start=side==="w"?6:1;
    if(r+d>=0&&r+d<8&&game.board[r+d][c]==="."){out.push([r+d,c]); if(r===start&&game.board[r+2*d][c]===".")out.push([r+2*d,c]);}
    for(const dc of [-1,1]){const rr=r+d,cc=c+dc;if(rr>=0&&rr<8&&cc>=0&&cc<8&&game.board[rr][cc]!=="."&&(side==="w"?game.board[rr][cc]===game.board[rr][cc].toLowerCase():game.board[rr][cc]===game.board[rr][cc].toUpperCase()))out.push([rr,cc]);}
  } else if(P==="n"){[[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[1,-2],[-1,2],[-1,-2]].forEach(([a,b])=>add(r+a,c+b))}
  else if(P==="k"){for(let a=-1;a<=1;a++)for(let b=-1;b<=1;b++)if(a||b)add(r+a,c+b)}
  else {
    let dirs=[]; if(P==="b"||P==="q")dirs.push([1,1],[1,-1],[-1,1],[-1,-1]); if(P==="r"||P==="q")dirs.push([1,0],[-1,0],[0,1],[0,-1]);
    for(const [dr,dc] of dirs){let rr=r+dr,cc=c+dc;while(rr>=0&&rr<8&&cc>=0&&cc<8){if(game.board[rr][cc]===".")out.push([rr,cc]);else{if((side==="w"?game.board[rr][cc]===game.board[rr][cc].toLowerCase():game.board[rr][cc]===game.board[rr][cc].toUpperCase()))out.push([rr,cc]);break}rr+=dr;cc+=dc}}
  }
  return out;
}

async function clickSquare(r,c){
  if(game.status==="checkmate"||game.status==="draw") return;
  const p=game.board[r][c];
  if(!selected){
    if(p!=="." && ((game.turn==="w"&&p===p.toUpperCase())||(game.turn==="b"&&p===p.toLowerCase()))){
      selected=[r,c]; render();
    }
    return;
  }
  if(selected[0]===r && selected[1]===c){selected=null;render();return}
  try{
    game=await api("/api/move",{method:"POST",body:JSON.stringify({fr:selected[0],fc:selected[1],tr:r,tc:c})});
    selected=null; render();
  }catch(e){
    if(p!=="." && ((game.turn==="w"&&p===p.toUpperCase())||(game.turn==="b"&&p===p.toLowerCase()))){
      selected=[r,c];render();
    } else {
      document.getElementById("status").textContent=e.message;
    }
  }
}

function renderHistory(){
  const el=document.getElementById("history");
  if(!game.history.length){el.textContent="No moves yet.";return}
  el.innerHTML=game.history.map((h,i)=>{
    return `<div class="move-row">${i+1}. Move played</div>`;
  }).join("");
  el.scrollTop=el.scrollHeight;
}

async function newGame(){
  selected=null;
  game=await api("/api/new-game",{method:"POST"});
  document.getElementById("gameModal").classList.add("hidden");
  render();
}

function showModal(){
  const modal=document.getElementById("gameModal");
  document.getElementById("modalTitle").textContent=game.status==="draw"?"Draw!":"Checkmate!";
  document.getElementById("modalText").textContent=game.status==="draw"?"No legal move remains.":"The "+(game.winner==="w"?"White":"Black")+" king wins the game.";
  modal.classList.remove("hidden");
}

document.getElementById("newGame").onclick=newGame;
document.getElementById("undo").onclick=async()=>{try{game=await api("/api/undo",{method:"POST"});selected=null;document.getElementById("gameModal").classList.add("hidden");render()}catch(e){alert(e.message)}};
document.getElementById("modalNew").onclick=newGame;

(async()=>{game=await api("/api/state");render()})();

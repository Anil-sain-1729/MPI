let gameState=null,selectedSource=null,isAnimating=false,isAutoSolving=false,paused=false,timerSeconds=0,timerInterval=null,messageTimeout=null;

const towerElements=[document.getElementById("tower0"),document.getElementById("tower1"),document.getElementById("tower2")];
const towerWrappers=document.querySelectorAll(".tower-wrapper");
const board=document.getElementById("board");
const arrowSvg=document.getElementById("arrowSvg");
const arrowLine=document.getElementById("arrowLine");
const moveText=document.getElementById("moveText");
const message=document.getElementById("message");
const movesElement=document.getElementById("moves");
const minimumElement=document.getElementById("minimum");
const timerElement=document.getElementById("timer");
const progressElement=document.getElementById("progress");
const discCount=document.getElementById("discCount");
const hintBtn=document.getElementById("hintBtn");
const undoBtn=document.getElementById("undoBtn");
const resetBtn=document.getElementById("resetBtn");
const autoBtn=document.getElementById("autoBtn");
const pauseBtn=document.getElementById("pauseBtn");
const newGameBtn=document.getElementById("newGameBtn");
const winModal=document.getElementById("winModal");
const winMoves=document.getElementById("winMoves");
const winMinimum=document.getElementById("winMinimum");
const winTime=document.getElementById("winTime");
const playAgainBtn=document.getElementById("playAgainBtn");

document.addEventListener("DOMContentLoaded",loadGame);

async function loadGame(){
    try{
        const response=await fetch("/api/state");
        const data=await response.json();
        gameState=data.state;
        discCount.value=gameState.n;
        render();
        startTimer();
    }catch(error){showMessage("Backend connection failed.",true);}
}

function render(){
    if(!gameState)return;

    for(let towerIndex=0;towerIndex<3;towerIndex++){
        const container=towerElements[towerIndex];
        container.innerHTML="";
        const stack=gameState.towers[towerIndex];
        const discHeight=window.innerWidth<600?28:34;
        const gap=3;

        stack.forEach((disc,index)=>{
            const element=document.createElement("div");
            element.className=`disc disc-${disc}`;
            element.textContent=disc;
            element.dataset.disc=disc;
            element.dataset.tower=towerIndex;
            element.draggable=true;

            element.style.width=`${calculateDiscWidth(disc,gameState.n)}px`;
            element.style.height=`${discHeight}px`;
            element.style.bottom=`${index*(discHeight+gap)}px`;

            const isTop=index===stack.length-1;

            if(!isTop){
                element.style.cursor="not-allowed";
                element.draggable=false;
            }

            if(selectedSource===towerIndex&&isTop)element.classList.add("selected");

            element.addEventListener("click",()=>handleDiscClick(towerIndex,disc,isTop));

            element.addEventListener("dragstart",event=>{
                if(!isTop){event.preventDefault();return;}
                selectedSource=towerIndex;
                element.classList.add("dragging");
                event.dataTransfer.setData("text/plain",String(towerIndex));
            });

            element.addEventListener("dragend",()=>element.classList.remove("dragging"));
            container.appendChild(element);
        });
    }

    updateStats();
    updateButtons();
}

function calculateDiscWidth(disc,totalDiscs){
    const maxWidth=window.innerWidth<600?105:210;
    const minWidth=window.innerWidth<600?45:70;
    return minWidth+(maxWidth-minWidth)*(disc/totalDiscs);
}

function handleDiscClick(towerIndex,disc,isTop){
    if(isAnimating||isAutoSolving)return;

    if(!isTop){
        showMessage("Only the top disc can be moved.",true);
        return;
    }

    if(selectedSource===null){
        selectedSource=towerIndex;
        moveText.textContent=`Disc ${disc} selected. Choose destination tower.`;
        render();
        return;
    }

    if(selectedSource===towerIndex){
        selectedSource=null;
        moveText.textContent="Selection cancelled.";
        render();
        return;
    }

    performMove(selectedSource,towerIndex);
}

towerWrappers.forEach(wrapper=>{
    const towerIndex=Number(wrapper.dataset.tower);

    wrapper.addEventListener("click",event=>{
        if(event.target.classList.contains("disc"))return;
        if(selectedSource!==null&&selectedSource!==towerIndex)performMove(selectedSource,towerIndex);
    });

    wrapper.addEventListener("dragover",event=>event.preventDefault());

    wrapper.addEventListener("drop",event=>{
        event.preventDefault();
        if(isAnimating||isAutoSolving)return;
        const source=Number(event.dataTransfer.getData("text/plain"));
        if(Number.isInteger(source))performMove(source,towerIndex);
    });
});

async function performMove(source,destination,options={}){
    if(isAnimating)return false;
    if(isAutoSolving===false&&options.fromAuto)return false;
    if(source===destination)return false;

    const oldState=JSON.parse(JSON.stringify(gameState));
    const sourceStack=oldState.towers[source];

    if(!sourceStack.length){
        showMessage("Source tower is empty.",true);
        selectedSource=null;
        return false;
    }

    const disc=sourceStack[sourceStack.length-1];
    const destinationLength=oldState.towers[destination].length;

    isAnimating=true;
    selectedSource=null;
    updateButtons();

    try{
        const response=await fetch("/api/move",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({source,destination})
        });

        const data=await response.json();

        if(!data.success){
            showMessage(data.message,true);
            return false;
        }

        showArrow(source,destination);
        moveText.textContent=`Moving disc ${disc}: ${towerName(source)} → ${towerName(destination)}`;

        await animateMove(source,destination,disc,destinationLength);

        gameState=data.state;
        hideArrow();
        render();

        if(gameState.won){
            stopTimer();
            showWinModal();
        }

        return true;
    }catch(error){
        showMessage("Server error.",true);
        return false;
    }finally{
        isAnimating=false;
        updateButtons();
    }
}

function animateMove(source,destination,disc,destinationLength){
    return new Promise(resolve=>{
        const sourceElement=towerElements[source].querySelector(`[data-disc="${disc}"]`);
        if(!sourceElement){resolve();return;}

        const startRect=sourceElement.getBoundingClientRect();
        const targetTower=towerWrappers[destination].querySelector(".tower");
        const targetRect=targetTower.getBoundingClientRect();
        const clone=sourceElement.cloneNode(true);

        Object.assign(clone.style,{
            position:"fixed",
            left:`${startRect.left}px`,
            top:`${startRect.top}px`,
            width:`${startRect.width}px`,
            height:`${startRect.height}px`,
            margin:"0",
            zIndex:"1000",
            pointerEvents:"none",
            transition:"none"
        });

        document.body.appendChild(clone);
        sourceElement.style.visibility="hidden";

        const h=startRect.height,gap=3;
        const targetLeft=targetRect.left+targetRect.width/2-startRect.width/2;
        const targetTop=targetRect.bottom-13-(destinationLength*(h+gap))-h;
        const liftTop=Math.max(45,Math.min(startRect.top-80,targetRect.top-90));

        requestAnimationFrame(()=>{
            clone.style.transition="top .35s ease-out";
            clone.style.top=`${liftTop}px`;
        });

        setTimeout(()=>{
            clone.style.transition="left .55s ease-in-out";
            clone.style.left=`${targetLeft}px`;
        },380);

        setTimeout(()=>{
            clone.style.transition="top .35s ease-in";
            clone.style.top=`${targetTop}px`;
        },950);

        setTimeout(()=>{
            clone.remove();
            resolve();
        },1350);
    });
}

function showArrow(source,destination){
    const sourceTower=towerWrappers[source].querySelector(".tower");
    const destinationTower=towerWrappers[destination].querySelector(".tower");
    const boardRect=board.getBoundingClientRect();
    const sourceRect=sourceTower.getBoundingClientRect();
    const destinationRect=destinationTower.getBoundingClientRect();

    const x1=sourceRect.left-boardRect.left+sourceRect.width/2;
    const x2=destinationRect.left-boardRect.left+destinationRect.width/2;
    const y=60;

    arrowSvg.setAttribute("viewBox",`0 0 ${boardRect.width} ${boardRect.height}`);
    arrowLine.setAttribute("x1",x1);
    arrowLine.setAttribute("y1",y);
    arrowLine.setAttribute("x2",x2);
    arrowLine.setAttribute("y2",y);
    arrowLine.classList.add("active");
}

function hideArrow(){arrowLine.classList.remove("active");}

hintBtn.addEventListener("click",async()=>{
    if(isAnimating||isAutoSolving)return;
    try{
        const response=await fetch("/api/hint",{method:"POST"});
        const data=await response.json();

        if(!data.success){showMessage(data.message,true);return;}
        if(!data.hint){showMessage(data.message);return;}

        selectedSource=data.hint.source;
        moveText.textContent=`💡 ${data.message}`;
        showArrow(data.hint.source,data.hint.destination);
        render();
        setTimeout(hideArrow,2500);
    }catch(error){showMessage("Could not get hint.",true);}
});

undoBtn.addEventListener("click",async()=>{
    if(isAnimating||isAutoSolving)return;

    try{
        const response=await fetch("/api/undo",{method:"POST"});
        const data=await response.json();

        if(!data.success){showMessage(data.message,true);return;}

        gameState=data.state;
        selectedSource=null;
        moveText.textContent="Previous move restored.";
        render();
    }catch(error){showMessage("Undo failed.",true);}
});

resetBtn.addEventListener("click",resetGame);

async function resetGame(){
    if(isAnimating||isAutoSolving)return;

    try{
        const response=await fetch("/api/reset",{method:"POST"});
        const data=await response.json();

        gameState=data.state;
        selectedSource=null;
        timerSeconds=0;
        startTimer();
        winModal.classList.add("hidden");
        moveText.textContent="Select a top disc to begin.";
        hideArrow();
        render();
    }catch(error){showMessage("Reset failed.",true);}
}

newGameBtn.addEventListener("click",createNewGame);
discCount.addEventListener("change",createNewGame);

async function createNewGame(){
    if(isAnimating||isAutoSolving){
        discCount.value=gameState.n;
        return;
    }

    const discs=Number(discCount.value);

    try{
        const response=await fetch("/api/new-game",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({discs})
        });

        const data=await response.json();
        gameState=data.state;
        selectedSource=null;
        timerSeconds=0;
        startTimer();
        winModal.classList.add("hidden");
        moveText.textContent="Select a top disc to begin.";
        hideArrow();
        render();
    }catch(error){showMessage("Could not create new game.",true);}
}

autoBtn.addEventListener("click",autoSolve);

async function autoSolve(){
    if(isAnimating||isAutoSolving)return;

    try{
        const response=await fetch("/api/auto-solve",{method:"POST"});
        const data=await response.json();

        if(!data.success){
            showMessage("Could not solve puzzle.",true);
            return;
        }

        if(data.moves.length===0){
            showMessage(gameState.won?"Puzzle is already solved.":"No moves available.");
            return;
        }

        isAutoSolving=true;
        updateButtons();

        for(const move of data.moves){
            await waitIfPaused();

            const success=await performMove(
                move.source,
                move.destination,
                {fromAuto:true}
            );

            if(!success)break;
            await sleep(120);
        }
    }catch(error){
        showMessage("Auto solve failed.",true);
    }finally{
        isAutoSolving=false;
        updateButtons();
    }
}

pauseBtn.addEventListener("click",()=>{
    paused=!paused;
    pauseBtn.textContent=paused?"▶ Resume":"⏸ Pause";
    moveText.textContent=paused?"Auto Solve paused.":"Auto Solve resumed.";
});

function waitIfPaused(){
    return new Promise(resolve=>{
        function check(){
            if(!paused)resolve();
            else setTimeout(check,100);
        }
        check();
    });
}

function startTimer(){
    stopTimer();

    timerInterval=setInterval(()=>{
        if(gameState&&!gameState.won&&!paused){
            timerSeconds++;
            updateTimer();
        }
    },1000);

    updateTimer();
}

function stopTimer(){
    if(timerInterval){
        clearInterval(timerInterval);
        timerInterval=null;
    }
}

function updateTimer(){
    timerElement.textContent=formatTime(timerSeconds);
}

function updateStats(){
    if(!gameState)return;
    movesElement.textContent=gameState.moves;
    minimumElement.textContent=gameState.minimum;

    const progress=Math.round(
        (gameState.towers[2].length/gameState.n)*100
    );

    progressElement.textContent=`${progress}%`;
}

function updateButtons(){
    const disabled=isAnimating||isAutoSolving;

    hintBtn.disabled=disabled;
    undoBtn.disabled=disabled||!gameState||gameState.moves===0;
    resetBtn.disabled=disabled;
    autoBtn.disabled=disabled;
    newGameBtn.disabled=disabled;
    discCount.disabled=disabled;
}

function showWinModal(){
    winMoves.textContent=gameState.moves;
    winMinimum.textContent=gameState.minimum;
    winTime.textContent=formatTime(timerSeconds);
    winModal.classList.remove("hidden");
    moveText.textContent="🏆 Puzzle solved!";
}

playAgainBtn.addEventListener("click",resetGame);

function showMessage(text,isError=false){
    clearTimeout(messageTimeout);
    message.textContent=text;
    message.classList.toggle("error",isError);
    message.classList.add("show");

    messageTimeout=setTimeout(
        ()=>message.classList.remove("show"),
        2500
    );
}

function towerName(index){return ["A","B","C"][index];}
function formatTime(totalSeconds){
    const minutes=Math.floor(totalSeconds/60);
    const seconds=totalSeconds%60;
    return `${String(minutes).padStart(2,"0")}:${String(seconds).padStart(2,"0")}`;
}
function sleep(ms){return new Promise(resolve=>setTimeout(resolve,ms));}

window.addEventListener("resize",()=>{
    if(!isAnimating)render();
});

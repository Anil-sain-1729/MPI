const patterns = [
{id:1,title:"Two Pointers",color:"--blue",short:"Use two indexes that move through a sorted array.",explain:"Two pointers keep a left and right position. Instead of checking every pair, move one pointer based on the comparison. This often reduces O(n²) pair checking to O(n).",complex:"Time O(n) • Space O(1)",code:`left = 0
right = len(nums) - 1

while left < right:
    total = nums[left] + nums[right]

    if total == target:
        return left, right
    elif total < target:
        left += 1
    else:
        right -= 1`,steps:["Start with L at the first element and R at the last element.","Compare nums[L] + nums[R] with the target.","If the sum is too small, move L right.","If the sum is too large, move R left.","Stop when the target pair is found or L crosses R."]},

{id:2,title:"Sliding Window",color:"--orange",short:"Maintain a moving range over an array/string.",explain:"A sliding window represents a continuous part of the input. Expand the right side when you need more data and move the left side when the window violates a condition.",complex:"Time O(n) • Space O(1)",code:`left = 0

for right in range(len(nums)):
    add(nums[right])

    while window_is_invalid():
        remove(nums[left])
        left += 1

    answer = max(answer, right-left+1)`,steps:["Start with an empty window.","Move R to expand the window.","Add the new element to the window state.","If the condition is invalid, move L and remove elements.","Record the best valid window."]},

{id:3,title:"Binary Search",color:"--green",short:"Repeatedly cut a sorted search space in half.",explain:"Binary search works on a sorted range. Check the middle element. If it is too small, discard the left half; if too large, discard the right half.",complex:"Time O(log n) • Space O(1)",code:`left = 0
right = len(nums) - 1

while left <= right:
    mid = (left + right) // 2

    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        left = mid + 1
    else:
        right = mid - 1`,steps:["Set L to the first index and R to the last.","Calculate MID.","Compare nums[MID] with the target.","Discard the half that cannot contain the target.","Repeat until found or the range is empty."]},

{id:4,title:"Frequency Counting",color:"--purple",short:"Store how often each value appears.",explain:"Use a hash map/object to count occurrences. This is useful for duplicates, anagrams, frequency comparisons and many lookup problems.",complex:"Time O(n) • Space O(k)",code:`freq = {}

for x in nums:
    if x not in freq:
        freq[x] = 0
    freq[x] += 1

return freq`,steps:["Create an empty frequency map.","Read each element one by one.","If the key does not exist, initialize its count.","Increase the count.","Use the map for fast frequency lookup."]},

{id:5,title:"Matrix Traversal",color:"--yellow",short:"Visit a 2D matrix in a controlled order.",explain:"Matrix problems often become easier when you identify the required traversal: row-wise, column-wise, diagonal or spiral. Keep boundaries/indexes explicit.",complex:"Time O(rows × cols) • Space O(1)",code:`top, bottom = 0, rows - 1
left, right = 0, cols - 1

while top <= bottom and left <= right:
    traverse top row
    traverse right column
    traverse bottom row
    traverse left column

    top += 1
    bottom -= 1
    left += 1
    right -= 1`,steps:["Begin at the outer boundary.","Traverse the top row from left to right.","Traverse the right column downward.","Traverse the bottom row backward.","Traverse the left column upward, then shrink the boundary."]},

{id:6,title:"Monotonic Stack",color:"--red",short:"Keep a stack in increasing or decreasing order.",explain:"A monotonic stack removes elements that can no longer be useful. It is common for next greater element, next smaller element, temperatures and histogram problems.",complex:"Time O(n) • Space O(n)",code:`stack = []

for x in nums:
    while stack and stack[-1] < x:
        answer[stack.pop()] = x

    stack.append(x)`,steps:["Create an empty stack.","Read the next value.","Pop values that violate the required monotonic order.","Those popped values have found their answer.","Push the current value/index."]},

{id:7,title:"Prefix Sum",color:"--green",short:"Precompute cumulative totals for fast range queries.",explain:"Prefix sums store the total from the beginning up to each index. A range sum can then be calculated with subtraction instead of looping through the whole range.",complex:"Build O(n) • Query O(1)",code:`prefix = [0]

for x in nums:
    prefix.append(prefix[-1] + x)

# sum from l to r
range_sum = prefix[r+1] - prefix[l]`,steps:["Start prefix with 0.","Add each number to the previous prefix value.","Now each prefix position stores a cumulative total.","For a range, subtract the prefix before the range from the prefix after it."]},

{id:8,title:"Overlapping Intervals",color:"--purple",short:"Sort intervals and merge ranges that overlap.",explain:"After sorting by start time, only the current merged interval needs to be compared with the next interval. If they overlap, extend the end.",complex:"Time O(n log n) • Space O(n)",code:`intervals.sort()

merged = []

for start, end in intervals:
    if not merged or start > merged[-1][1]:
        merged.append([start, end])
    else:
        merged[-1][1] = max(merged[-1][1], end)`,steps:["Sort intervals by their starting point.","Take the first interval as the current range.","Compare the next start with the current end.","If they overlap, extend the current end.","Otherwise save the current range and start a new one."]},

{id:9,title:"Greedy",color:"--yellow",short:"Make the best local choice at every step.",explain:"Greedy algorithms choose an immediately useful option without revisiting earlier choices. They work when the problem has the required greedy property.",complex:"Depends on problem",code:`while work_remains:
    choice = best_available_choice()
    take(choice)
    update_state()`,steps:["Define what a locally best choice means.","Pick the best currently available option.","Commit to that choice.","Update the remaining problem.","Repeat until the goal is reached."]},

{id:10,title:"Top K Elements",color:"--orange",short:"Keep only the K most important values.",explain:"A heap can maintain K elements efficiently. For top K largest values, use a min-heap of size K; the smallest value in the heap is the current cutoff.",complex:"Time O(n log k) • Space O(k)",code:`heap = []

for x in nums:
    push(heap, x)

    if len(heap) > k:
        pop_min(heap)

return heap`,steps:["Create a heap with capacity K.","Insert each candidate.","When the heap grows beyond K, remove the smallest.","The remaining K elements are the top K candidates."]},

{id:11,title:"Backtracking",color:"--green",short:"Explore choices, then undo the choice.",explain:"Backtracking builds a solution incrementally. When a path cannot produce a valid answer, undo the last decision and try another choice.",complex:"Usually exponential • Depends on problem",code:`def backtrack(path):
    if complete(path):
        save(path)
        return

    for choice in choices:
        if valid(choice):
            path.append(choice)
            backtrack(path)
            path.pop()  # undo`,steps:["Choose one possible option.","Add it to the current path.","Recursively explore deeper.","If the path is complete, record it.","Undo the choice and try the next option."]},

{id:12,title:"Binary Tree Traversal",color:"--purple",short:"Visit tree nodes in a defined order.",explain:"Common traversals are preorder (root-left-right), inorder (left-root-right), and postorder (left-right-root). Inorder on a BST gives sorted values.",complex:"Time O(n) • Space O(h)",code:`def inorder(node):
    if not node:
        return

    inorder(node.left)
    visit(node)
    inorder(node.right)`,steps:["Start at the root.","Go to the left subtree.","Visit the current node according to the chosen traversal.","Go to the right subtree.","Continue recursively until all nodes are visited."]},

{id:13,title:"Depth-First Search",color:"--green",short:"Go as deep as possible before backtracking.",explain:"DFS follows one path deeply before returning. It can be implemented with recursion or an explicit stack and is useful for connected components, paths and graph exploration.",complex:"Time O(V+E) • Space O(V)",code:`stack = [start]
visited = set()

while stack:
    node = stack.pop()

    if node in visited:
        continue

    visited.add(node)

    for nxt in graph[node]:
        stack.append(nxt)`,steps:["Put the start node on a stack.","Pop one node.","If already visited, skip it.","Mark it visited and push its neighbors.","Continue until the stack is empty."]},

{id:14,title:"Breadth-First Search",color:"--blue",short:"Explore a graph level by level using a queue.",explain:"BFS visits all nodes at distance 1 before distance 2, then distance 3, and so on. In an unweighted graph, BFS can find the shortest number-of-edges path.",complex:"Time O(V+E) • Space O(V)",code:`queue = [start]
visited = {start}

while queue:
    node = queue.pop(0)

    for nxt in graph[node]:
        if nxt not in visited:
            visited.add(nxt)
            queue.append(nxt)`,steps:["Put the start node in a queue.","Remove the front node.","Visit its unvisited neighbors.","Add those neighbors to the back of the queue.","The queue naturally processes nodes level by level."]},

{id:15,title:"Dynamic Programming",color:"--red",short:"Store answers to overlapping subproblems.",explain:"DP avoids recalculating the same subproblem. Define a state, write its recurrence, set base cases, and compute each state once.",complex:"Depends on states • Often O(n) or O(n×m)",code:`dp = [0] * (n + 1)
dp[0] = base0
dp[1] = base1

for i in range(2, n + 1):
    dp[i] = dp[i-1] + dp[i-2]

return dp[n]`,steps:["Identify the smaller repeated subproblems.","Define what dp[i] represents.","Set the base cases.","Use the recurrence to calculate each new state.","Return the final state."]}
];

const cards = document.getElementById("cards");
const search = document.getElementById("search");
const modal = document.getElementById("modal");
const visual = document.getElementById("visual");
const mTitle = document.getElementById("mTitle");
const mNumber = document.getElementById("mNumber");
const mShort = document.getElementById("mShort");
const complexity = document.getElementById("complexity");
const explanation = document.getElementById("explanation");
const stepExplanation = document.getElementById("stepExplanation");
const code = document.getElementById("code");
const stepText = document.getElementById("stepText");
const progressBar = document.getElementById("progressBar");

let current = null;
let step = 0;
let timer = null;

function colorVar(p){ return getComputedStyle(document.documentElement).getPropertyValue(p.color).trim(); }

function miniVisual(p){
  if([1,2,3,4,7,9,10,15].includes(p.id)){
    return `<div class="array">${[1,3,5,7,9].map((x,i)=>`<div class="cell ${i===2?'active':''}">${x}</div>`).join("")}</div>`;
  }
  if(p.id===5) return `<div class="matrix">${Array.from({length:12},(_,i)=>`<div class="cell ${i===5?'active':''}">${i+1}</div>`).join("")}</div>`;
  if([11,12].includes(p.id)) return `<div class="tree">
    <div class="node" style="left:145px;top:0">4</div>
    <div class="node" style="left:75px;top:55px">2</div>
    <div class="node" style="left:215px;top:55px">6</div>
    <div class="node" style="left:38px;top:100px">1</div>
    <div class="node" style="left:112px;top:100px">3</div>
  </div>`;
  if([13,14].includes(p.id)) return `<div class="graph">
    <div class="gline" style="left:85px;top:55px;width:145px;transform:rotate(-20deg)"></div>
    <div class="gline" style="left:225px;top:55px;width:145px;transform:rotate(20deg)"></div>
    <div class="gnode" style="left:40px;top:35px">A</div>
    <div class="gnode" style="left:185px;top:5px">B</div>
    <div class="gnode" style="left:285px;top:35px">C</div>
    <div class="gnode" style="left:95px;top:85px">D</div>
    <div class="gnode" style="left:235px;top:85px">E</div>
  </div>`;
  if(p.id===6) return `<div class="array">${[1,3,2,4].map(x=>`<div class="cell">${x}</div>`).join("")}</div>`;
  if(p.id===8) return `<div style="width:270px"><div style="height:22px;background:#315b7a;width:100px;margin:8px 0;border-radius:4px"></div><div style="height:22px;background:#7a3b69;width:150px;margin-left:70px;border-radius:4px"></div><div style="height:22px;background:#00a878;width:220px;margin-left:25px;border-radius:4px"></div></div>`;
  return "";
}

function renderCards(filter=""){
  cards.innerHTML="";
  patterns.filter(p=>p.title.toLowerCase().includes(filter.toLowerCase())).forEach(p=>{
    const card=document.createElement("article");
    card.className="card";
    card.innerHTML=`<div class="num" style="color:${colorVar(p)}">0${p.id} · PATTERN</div>
      <h3>${p.title}</h3>
      <p>${p.short}</p>
      <div class="mini">${miniVisual(p)}</div>`;
    card.onclick=()=>openPattern(p);
    cards.appendChild(card);
  });
}

function openPattern(p){
  current=p; step=0;
  mNumber.textContent=`PATTERN ${String(p.id).padStart(2,"0")}`;
  mTitle.textContent=p.title;
  mTitle.style.color=colorVar(p);
  mShort.textContent=p.short;
  complexity.textContent=p.complex;
  explanation.textContent=p.explain;
  code.textContent=p.code;
  modal.classList.remove("hidden");
  renderStep();
}

function renderStep(){
  if(!current)return;
  const total=current.steps.length;
  step=Math.max(0,Math.min(step,total-1));
  stepText.textContent=`Step ${step+1} / ${total}`;
  stepExplanation.textContent=current.steps[step];
  progressBar.style.width=((step+1)/total*100)+"%";
  drawVisual(current,step);
}

function cells(nums, active=[], labels={}){
  return `<div class="array">${nums.map((n,i)=>{
    let cls="cell";
    if(active.includes(i))cls+=" active";
    if(labels[i]==="L")cls+=" left";
    if(labels[i]==="R")cls+=" right";
    if(labels[i]==="M")cls+=" mid";
    return `<div><div class="${cls}">${n}</div>${labels[i]?`<div class="pointer">${labels[i]}</div>`:""}</div>`;
  }).join("")}</div>`;
}

function drawVisual(p,s){
  const nums=[2,1,5,1,3,2];
  if(p.id===1){
    const L=Math.min(s,3),R=Math.max(5-s, L+1);
    visual.innerHTML=cells([1,3,5,7,9,11],[L,R],{[L]:"L",[R]:"R"});
  }else if(p.id===2){
    const L=Math.min(s,3),R=Math.min(L+2,5);
    visual.innerHTML=cells(nums,Array.from({length:R-L+1},(_,i)=>L+i),{[L]:"L",[R]:"R"});
  }else if(p.id===3){
    const ranges=[[0,6],[0,2],[2,2],[3,3],[3,3]];
    const [l,r]=ranges[Math.min(s,ranges.length-1)],m=Math.floor((l+r)/2);
    visual.innerHTML=cells([1,3,5,7,9,11,13], [m], {[l]:"L",[m]:"M",[r]:"R"});
  }else if(p.id===4){
    const arr=["a","b","a","c","b"], counts={};
    for(let i=0;i<=s && i<arr.length;i++) counts[arr[i]]=(counts[arr[i]]||0)+1;
    visual.innerHTML=`<div><div class="array">${arr.map((x,i)=>`<div class="cell ${i===s?'active':''}">${x}</div>`).join("")}</div>
    <pre style="margin-top:25px">Frequency Map\n${Object.entries(counts).map(([k,v])=>`${k} : ${v}`).join("\n")}</pre></div>`;
  }else if(p.id===5){
    const total=16; let active=Math.min(s,total-1);
    visual.innerHTML=`<div class="matrix">${Array.from({length:total},(_,i)=>`<div class="cell ${i===active?'active':''}">${i+1}</div>`).join("")}</div>`;
  }else if(p.id===6){
    const arr=[1,3,2,4]; const active=Math.min(s,3);
    visual.innerHTML=`<div><div class="array">${arr.map((x,i)=>`<div class="cell ${i===active?'active':''}">${x}</div>`).join("")}</div><div style="margin-top:35px;text-align:center;color:#8e9aa8">Stack: ${arr.slice(0,Math.min(s+1,arr.length)).join(" → ")}</div></div>`;
  }else if(p.id===7){
    const arr=[1,2,3,4,5]; const pref=arr.map((_,i)=>arr.slice(0,i+1).reduce((a,b)=>a+b,0));
    visual.innerHTML=`<div><div class="array">${arr.map((x,i)=>`<div class="cell ${i===s?'active':''}">${x}</div>`).join("")}</div><div class="array" style="margin-top:35px">${pref.map((x,i)=>`<div class="cell">${x}</div>`).join("")}</div><div style="text-align:center;color:#8e9aa8;margin-top:15px">Prefix = cumulative total</div></div>`;
  }else if(p.id===8){
    const bars=[
      [30,105],[80,155],[145,210],[215,275]
    ];
    const shown=Math.min(s+1,bars.length);
    visual.innerHTML=`<div>${bars.slice(0,shown).map((b,i)=>`<div style="display:flex;gap:10px;align-items:center;margin:12px"><span style="color:#8e9aa8">I${i+1}</span><div style="height:26px;width:${b[1]-b[0]+80}px;background:${i===shown-1?'#00a878':'#315b7a'};border-radius:5px"></div></div>`).join("")}<div style="color:#00e5a0;text-align:center">Merge overlapping ranges</div></div>`;
  }else if(p.id===9){
    const arr=[25,10,5,1]; const a=Math.min(s,3);
    visual.innerHTML=`<div><div class="array">${arr.map((x,i)=>`<div class="cell ${i===a?'active':''}">${x}</div>`).join("")}</div><div style="text-align:center;margin-top:35px;color:#ffd447">Choose largest value that fits</div></div>`;
  }else if(p.id===10){
    const arr=[9,7,5,3,2]; const shown=Math.min(s+2,5);
    visual.innerHTML=`<div><div class="array">${arr.map((x,i)=>`<div class="cell ${i<shown?'active':''}">${x}</div>`).join("")}</div><div style="text-align:center;margin-top:35px;color:#ffad42">Keep only K best elements</div></div>`;
  }else if(p.id===11||p.id===12){
    visual.innerHTML=`<div class="tree" style="transform:scale(1.7)">
      <div class="node" style="left:145px;top:0;border-color:${s>=0?'#00e5a0':'#27313c'}">4</div>
      <div class="node" style="left:75px;top:55px">2</div><div class="node" style="left:215px;top:55px">6</div>
      <div class="node" style="left:38px;top:110px">1</div><div class="node" style="left:112px;top:110px">3</div>
      <div class="node" style="left:178px;top:110px">5</div><div class="node" style="left:252px;top:110px">7</div>
    </div>`;
  }else if(p.id===13||p.id===14){
    const order=p.id===13?["A","B","C","E","D"]:["A","B","D","C","E"];
    const shown=order.slice(0,s+1);
    visual.innerHTML=`<div><div class="array">${order.map(x=>`<div class="cell ${shown.includes(x)?'active':''}">${x}</div>`).join("")}</div><div style="margin-top:35px;text-align:center;color:${p.id===13?'#00e5a0':'#28a8ff'}">${p.id===13?'DFS':'BFS'} visits: ${shown.join(" → ")}</div></div>`;
  }else if(p.id===15){
    const vals=[1,1,2,3,5,8]; const shown=Math.min(s+1,vals.length);
    visual.innerHTML=`<div><div class="array">${vals.map((x,i)=>`<div class="cell ${i<shown?'active':''}">${x}</div>`).join("")}</div><div style="margin-top:35px;text-align:center;color:#ff5d68">Reuse stored subproblem answers</div></div>`;
  }
}

document.getElementById("next").onclick=()=>{if(current&&step<current.steps.length-1){step++;renderStep()}};
document.getElementById("prev").onclick=()=>{if(current&&step>0){step--;renderStep()}};
document.getElementById("reset").onclick=()=>{step=0;renderStep()};
document.getElementById("play").onclick=()=>{
  if(timer){clearInterval(timer);timer=null;document.getElementById("play").textContent="▶ Play";return}
  document.getElementById("play").textContent="⏸ Pause";
  timer=setInterval(()=>{
    if(step>=current.steps.length-1){clearInterval(timer);timer=null;document.getElementById("play").textContent="▶ Play";return}
    step++;renderStep();
  },1300);
};
document.getElementById("close").onclick=()=>{modal.classList.add("hidden");if(timer){clearInterval(timer);timer=null}};
modal.onclick=e=>{if(e.target===modal)document.getElementById("close").click()};
search.oninput=e=>renderCards(e.target.value);
renderCards();

const cells = document.querySelectorAll(".cell");
const statusText = document.getElementById("status");
const resetBtn = document.getElementById("resetBtn");

let board = ["", "", "", "", "", "", "", "", ""];
let currentPlayer = "X";
let gameActive = true;

const winningPatterns = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
];

cells.forEach(cell => {
    cell.addEventListener("click", () => {
        const index = cell.getAttribute("data-index");

        if (board[index] !== "" || !gameActive) return;

        board[index] = currentPlayer;
        cell.textContent = currentPlayer;
        cell.classList.add(currentPlayer.toLowerCase());

        checkWinner();
    });
});

function checkWinner() {
    let winner = null;

    for (const pattern of winningPatterns) {
        const [a, b, c] = pattern;

        if (board[a] !== "" && board[a] === board[b] && board[b] === board[c]) {
            winner = board[a];
            break;
        }
    }

    if (winner) {
        statusText.textContent = `Player ${winner} Wins!`;
        gameActive = false;
        return;
    }

    if (!board.includes("")) {
        statusText.textContent = "Game Draw!";
        gameActive = false;
        return;
    }

    currentPlayer = currentPlayer === "X" ? "O" : "X";
    statusText.textContent = `Player ${currentPlayer}'s Turn`;
}

resetBtn.addEventListener("click", resetGame);

function resetGame() {
    board = ["", "", "", "", "", "", "", "", ""];
    currentPlayer = "X";
    gameActive = true;
    statusText.textContent = "Player X's Turn";

    cells.forEach(cell => {
        cell.textContent = "";
        cell.classList.remove("x", "o");
    });
}

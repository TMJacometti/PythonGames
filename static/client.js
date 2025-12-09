// static/client.js
const boardDiv = document.getElementById("board");
const statusDiv = document.getElementById("status");

let socket = null;
let you = null;          // "red" ou "black"
let currentTurn = null;  // "red" ou "black"
let board = [];          // matriz 8x8
let selectedCell = null; // {row, col}

function connect() {
    // Uma sala fixa "default". Se quiser múltiplas, muda aqui.
    socket = new WebSocket(`ws://${window.location.host}/ws/default`);

    socket.onopen = () => {
        statusDiv.textContent = "Conectado. Aguardando outro jogador...";
    };

    socket.onmessage = (event) => {
        const msg = JSON.parse(event.data);

        if (msg.type === "joined") {
            you = msg.you;
            statusDiv.textContent = `Você é: ${you === "red" ? "Vermelho (começa)" : "Preto"}`;
        }

        if (msg.type === "state") {
            you = msg.you;
            board = msg.board;
            currentTurn = msg.current_turn;
            renderBoard();
            updateStatus();
        }

        if (msg.type === "error") {
            alert(`Erro: ${msg.message}`);
        }
    };

    socket.onclose = () => {
        statusDiv.textContent = "Conexão fechada. Recarregue a página para tentar novamente.";
    };
}

function updateStatus() {
    if (!you || !currentTurn) return;
    const meuTurno = (you === currentTurn);
    statusDiv.textContent = `Você é: ${you}. Turno de: ${currentTurn}` +
        (meuTurno ? " (SEU TURNO)" : " (aguarde)");
}

function renderBoard() {
    boardDiv.innerHTML = "";
    for (let r = 0; r < 8; r++) {
        for (let c = 0; c < 8; c++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");

            if ((r + c) % 2 === 0) {
                cell.classList.add("light");
            } else {
                cell.classList.add("dark");
            }

            cell.dataset.row = r;
            cell.dataset.col = c;

            const value = board[r][c];
            if (value !== 0) {
                const pieceDiv = document.createElement("div");
                pieceDiv.classList.add("piece");
                if (value > 0) {
                    pieceDiv.classList.add("red");
                } else {
                    pieceDiv.classList.add("black");
                }

                // Se for dama, mostra "D"
                if (Math.abs(value) === 2) {
                    pieceDiv.textContent = "D";
                }

                cell.appendChild(pieceDiv);
            }

            if (selectedCell && selectedCell.row === r && selectedCell.col === c) {
                cell.classList.add("selected");
            }

            cell.addEventListener("click", () => onCellClick(r, c));
            boardDiv.appendChild(cell);
        }
    }
}

function onCellClick(r, c) {
    if (!you || !currentTurn) return;
    const isMyTurn = (you === currentTurn);
    if (!isMyTurn) return; // só joga no seu turno

    const value = board[r][c];

    // Se nada selecionado ainda
    if (!selectedCell) {
        // Só pode selecionar peça sua
        if ((you === "red" && value > 0) || (you === "black" && value < 0)) {
            selectedCell = { row: r, col: c };
            renderBoard();
        }
        return;
    } else {
        // Já tinha origem, então clica no destino
        const from = selectedCell;
        const to = { row: r, col: c };

        // Se clicou de novo na mesma célula, desmarca
        if (from.row === to.row && from.col === to.col) {
            selectedCell = null;
            renderBoard();
            return;
        }

        // Envia jogada ao servidor
        socket.send(JSON.stringify({
            type: "move",
            from: [from.row, from.col],
            to: [to.row, to.col],
        }));

        selectedCell = null;
        // O servidor vai validar e mandar o novo estado
    }
}

connect();

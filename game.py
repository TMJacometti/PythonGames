# game.py
from typing import List, Tuple, Optional

EMPTY = 0

P1_MAN = 1
P1_KING = 2
P2_MAN = -1
P2_KING = -2


class InvalidMove(Exception):
    pass


class CheckersGame:
    def __init__(self):
        self.board = self._initial_board()
        # "red" = jogador 1, "black" = jogador 2
        self.current_turn = "red"

    def _initial_board(self) -> List[List[int]]:
        board = [[EMPTY for _ in range(8)] for _ in range(8)]

        # Jogador 1 (red) em cima
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = P1_MAN

        # Jogador 2 (black) em baixo
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = P2_MAN

        return board

    def get_board_state(self) -> List[List[int]]:
        return self.board

    def _piece_owner(self, value: int) -> Optional[str]:
        if value in (P1_MAN, P1_KING):
            return "red"
        if value in (P2_MAN, P2_KING):
            return "black"
        return None

    def _is_king(self, value: int) -> bool:
        return value in (P1_KING, P2_KING)

    def _direction_for_player(self, player: str) -> int:
        # red começa em cima indo para baixo (linha cresce)
        # black começa em baixo indo para cima (linha diminui)
        return 1 if player == "red" else -1

    def move(self, player: str, from_pos: Tuple[int, int], to_pos: Tuple[int, int]):
        fr, fc = from_pos
        tr, tc = to_pos

        # Valida coordenadas
        if not (0 <= fr < 8 and 0 <= fc < 8 and 0 <= tr < 8 and 0 <= tc < 8):
            raise InvalidMove("Posição fora do tabuleiro.")

        piece = self.board[fr][fc]
        if piece == EMPTY:
            raise InvalidMove("Não há peça na posição de origem.")

        owner = self._piece_owner(piece)
        if owner != player:
            raise InvalidMove("A peça não pertence a você.")

        if self.current_turn != player:
            raise InvalidMove("Não é seu turno.")

        if self.board[tr][tc] != EMPTY:
            raise InvalidMove("A posição de destino não está vazia.")

        dr = tr - fr
        dc = tc - fc

        if abs(dc) != abs(dr):
            raise InvalidMove("Movimento precisa ser na diagonal.")

        step = abs(dr)

        is_king = self._is_king(piece)
        direction = self._direction_for_player(player)

        # Movimento simples (sem captura)
        if step == 1:
            if not is_king and (dr != direction):
                raise InvalidMove("Peça normal só anda para frente.")
            # Ok, movimento simples
            self.board[tr][tc] = piece
            self.board[fr][fc] = EMPTY

        # Movimento de captura
        elif step == 2:
            mid_r = (fr + tr) // 2
            mid_c = (fc + tc) // 2
            mid_piece = self.board[mid_r][mid_c]
            mid_owner = self._piece_owner(mid_piece)

            if mid_piece == EMPTY or mid_owner == player:
                raise InvalidMove("Não há peça adversária para capturar.")

            if not is_king and (dr != 2 * direction):
                raise InvalidMove("Peça normal só captura para frente.")

            # Captura válida
            self.board[tr][tc] = piece
            self.board[fr][fc] = EMPTY
            self.board[mid_r][mid_c] = EMPTY

        else:
            raise InvalidMove("Só é permitido andar 1 casa ou capturar pulando 2 casas.")

        # Promoção
        if player == "red" and tr == 7 and piece == P1_MAN:
            self.board[tr][tc] = P1_KING
        elif player == "black" and tr == 0 and piece == P2_MAN:
            self.board[tr][tc] = P2_KING

        # Troca turno
        self.current_turn = "black" if self.current_turn == "red" else "red"

    def serialize(self):
        return {
            "board": self.board,
            "current_turn": self.current_turn,
        }

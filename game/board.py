from game.constants import DIRECTIONS, Color, Status
from game.exceptions import EmptyCellException, InvalidPositionException, OccupiedCellException

from game.piece import Piece
from game.player import Player


class Cell:
    def __init__(self):
        self.__piece = None

    def place_piece(self, piece: Piece) -> None:
        if self.__piece is not None:
            raise OccupiedCellException()
        self.__piece = piece

    def remove_piece(self) -> Piece:
        if self.__piece is None:
            raise EmptyCellException()
        piece = self.__piece
        self.__piece = None
        return piece

    def is_occupied(self) -> bool:
        return self.__piece is not None

    def is_empty(self) -> bool:
        return self.__piece is None

    def get_piece(self) -> Piece:
        return self.__piece


class Board:
    def __init__(self):
        self.__cells: list[list[Cell]]
        self.__players: list[Player]
        self.__status = Status.NO_MATCH
        self.start()

    def click(self, position: tuple[int, int]) -> None:
        if self.__status == Status.NO_MATCH:
            self.start()
        elif self.__status == Status.IN_PROGRESS:
            self.place_piece(position)
        elif self.__status == Status.FINISHED:
            self.start()

    def start(self) -> None:
        self.__cells = [[Cell() for _ in range(6)] for _ in range(6)]
        self.__players = [Player(Color.RED), Player(Color.BLUE)]
        self.__status = Status.IN_PROGRESS

    def current_player(self) -> Player:
        return self.__players[0]

    def flip_players(self) -> None:
        self.__players.reverse()

    def get_player(self, color: Color) -> Player:
        for player in self.__players:
            if player.get_color() == color:
                return player

    def get_cell(self, position: tuple[int, int]) -> Cell:
        if self.position_valid(position):
            return self.__cells[position[0]][position[1]]
        raise InvalidPositionException()

    def position_valid(self, position: tuple[int, int]) -> bool:
        return 0 <= position[0] < 6 and 0 <= position[1] < 6

    def move_piece(self, source: Cell, destination: Cell) -> None:
        if destination.is_empty():
            piece = source.remove_piece()
            destination.place_piece(piece)

    def remove_piece(self, cell: Cell) -> None:
        piece = cell.remove_piece()
        owner = next(p for p in self.__players if p.get_color() == piece.get_color())
        owner.take_piece(piece)

    def place_piece(self, position: tuple[int, int]) -> None:
        if self.position_valid(position):
            cell = self.get_cell(position)
            if cell.is_occupied():
                return
        else:
            return

        player = self.current_player()
        piece = player.place_piece()
        cell.place_piece(piece)

        self.push_neighbors(position)
        self.flip_players()

    def push_neighbors(self, position: tuple[int, int]) -> None:
        for direction in DIRECTIONS:
            neighbor_position = (position[0] + direction[0], position[1] + direction[1])
            if self.position_valid(neighbor_position):
                neighbor = self.get_cell(neighbor_position)
                if neighbor.is_empty():
                    continue
            else:
                continue

            push_position = (neighbor_position[0] + direction[0], neighbor_position[1] + direction[1])
            if self.position_valid(push_position):
                push = self.get_cell(push_position)
                self.move_piece(neighbor, push)
            else:
                self.remove_piece(neighbor)

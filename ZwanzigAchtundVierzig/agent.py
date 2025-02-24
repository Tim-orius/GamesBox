import numpy as np
from game_grid import GameGrid
from game_ui import GameUI


class State:
    def __init__(self, grid:GameGrid, state_move:int=None, parent=None):
        """

        :param grid: GameGrid instance.
        :param state_move: the move performed to reach this state (from the parent state).
        :param parent: parent (previous) state before the move has been applied.
        """
        self.score = 0

        self.grid = grid
        self.parent = parent
        self.performed_moves = parent.performed_moves.copy() if parent else []

        if state_move is not None: self.performed_moves.append(state_move)

    def move(self, direction):
        success = self.grid.move(direction)
        self.update_score(success)

        return success

    def update_score(self, move_success:bool):
        base_score = self.grid.score
        if not move_success:
            base_score -= 100

        self.score = base_score

    def copy(self, state_move:int):
        new_grid = GameGrid(self.grid.frame_size, self.grid.base_number, self.grid.percent_double_base_on_spawn)
        new_grid.field = self.grid.copy()
        new_grid.score = self.grid.score
        return State(new_grid, state_move=state_move, parent=self)


class Agent:
    def __init__(self, grid:GameGrid=None, ui:GameUI=None):
        """AI Agent for the Game 2048.

        :param grid: GameGrid instance for the game. Will be ignored when a game ui is supplied.
        :param ui: Game UI instance for the game. Will be preferred over game_grid.
        """
        if grid is None and ui is None:
            raise ValueError("Either a GameGrid or a GameUI have to be supplied.")

        self.grid = grid
        self.ui = ui

        self.states = []

    def step(self, grid:GameGrid, depth:int):
        """Perform one step of search for the best move

        :param grid: GameGrid instance
        :param depth: depth for search
        :return: best state and best move to reach the best state
        """
        best_state = self.depth_search(state=State(grid), depth=depth)

        if best_state.performed_moves:
            return best_state, best_state.performed_moves[0]
        else:
            return best_state, -1

    def depth_search(self, state:State, depth):
        """Perform search for best move in a set number of steps ahead.

        :param state: current state of the game
        :param depth: depth for search
        :return: best state in *depth* moves
        """
        self.states = []

        self.lookup(state=state, depth=depth)

        if not self.states:
            return state

        # Identify the best state based on the score
        best_state = max(self.states, key=lambda s: s.score)

        return best_state

    def lookup(self, state:State, depth:int):
        if depth == 0:
            self.states.append(state)
            return

        for ii in range(4):
            new_state = state.copy(state_move=ii)
            success = new_state.move(direction=ii)

            if success:
                self.lookup(new_state, depth-1)

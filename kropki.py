
import sys
from typing import List, Tuple

class KropkiSudoku:
    def __init__(self, initial_board: List[List[int]], 
                 horizontal_dots: List[List[int]], 
                 vertical_dots: List[List[int]]):
        # Initialize the Kropki Sudoku board and dot constraints
        self.board = [row[:] for row in initial_board]
        self.horizontal_dots = horizontal_dots
        self.vertical_dots = vertical_dots

    def is_valid_assignment(self, row: int, col: int, num: int) -> bool:
        # Check if assigning 'num' to cell (row, col) is valid

        # Check row constraint
        if num in self.board[row]:
            return False
        
        # Check column constraint
        if num in [self.board[i][col] for i in range(9)]:
            return False
        
        # Check 3x3 block constraint
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.board[r][c] == num:
                    return False
        
        # Check Kropki dot constraints
        # Horizontal checks
        if col < 8 and self.horizontal_dots[row][col] != 0:
            right_val = self.board[row][col+1]
            dot_val = self.horizontal_dots[row][col]
            if right_val != 0:
                # White dot check (difference of 1)
                if dot_val == 1 and abs(num - right_val) != 1:
                    return False
                # Black dot check (one value is double the other)
                if dot_val == 2 and (num != 2*right_val and right_val != 2*num):
                    return False
        
        if col > 0 and self.horizontal_dots[row][col-1] != 0:
            left_val = self.board[row][col-1]
            dot_val = self.horizontal_dots[row][col-1]
            if left_val != 0:
                # White dot check (difference of 1)
                if dot_val == 1 and abs(num - left_val) != 1:
                    return False
                # Black dot check (one value is double the other)
                if dot_val == 2 and (num != 2*left_val and left_val != 2*num):
                    return False
        
        # Vertical checks
        if row < 8 and self.vertical_dots[row][col] != 0:
            down_val = self.board[row+1][col]
            dot_val = self.vertical_dots[row][col]
            if down_val != 0:
                # White dot check (difference of 1)
                if dot_val == 1 and abs(num - down_val) != 1:
                    return False
                # Black dot check (one value is double the other)
                if dot_val == 2 and (num != 2*down_val and down_val != 2*num):
                    return False
        
        if row > 0 and self.vertical_dots[row-1][col] != 0:
            up_val = self.board[row-1][col]
            dot_val = self.vertical_dots[row-1][col]
            if up_val != 0:
                # White dot check (difference of 1)
                if dot_val == 1 and abs(num - up_val) != 1:
                    return False
                # Black dot check (one value is double the other)
                if dot_val == 2 and (num != 2*up_val and up_val != 2*num):
                    return False
        
        return True

    def select_unassigned_variable(self) -> Tuple[int, int]:
        # Select unassigned variable using Minimum Remaining Values (MRV)
        # and Degree heuristic as a tie-breaker
        min_remaining_values = 10
        max_degree = -1
        selected_var = None

        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    remaining_values = sum(1 for num in range(1, 10) 
                                           if self.is_valid_assignment(row, col, num))
                    degree = self.count_constraints(row, col)
                    
                    if (remaining_values < min_remaining_values or 
                        (remaining_values == min_remaining_values and degree > max_degree)):
                        min_remaining_values = remaining_values
                        max_degree = degree
                        selected_var = (row, col)
        
        return selected_var

    def count_constraints(self, row: int, col: int) -> int:
        # Count the number of constraints (filled cells) in the same row, column, and 3x3 block
        constraints = 0
        for r in range(9):
            for c in range(9):
                if (r == row or c == col or (r//3 == row//3 and c//3 == col//3)) and self.board[r][c] != 0:
                    constraints += 1
        return constraints

    def solve(self) -> bool:
        # Backtracking algorithm to solve the Kropki Sudoku
        var = self.select_unassigned_variable()
        if var is None:
            return True
        
        row, col = var
        for num in range(1, 10):
            if self.is_valid_assignment(row, col, num):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0
        
        return False

    def print_solution(self) -> List[List[int]]:
        # Print the solution to console and return as 2D list
        for row in self.board:
            print(' '.join(map(str, row)))
        return self.board

def read_input_file(filename: str) -> Tuple[List[List[int]], List[List[int]], List[List[int]]]:
    # Read input file and parse Sudoku board and dot constraints
    with open(filename, 'r') as f:
        initial_board = [list(map(int, f.readline().split())) for _ in range(9)]
        f.readline()  # Skip blank line
        horizontal_dots = [list(map(int, f.readline().split())) for _ in range(9)]
        f.readline()  # Skip blank line
        vertical_dots = [list(map(int, f.readline().split())) for _ in range(8)]
    return initial_board, horizontal_dots, vertical_dots

def write_output_file(filename: str, solution: List[List[int]]):
    # Write solution to output file
    with open(filename, 'w') as f:
        for row in solution:
            f.write(' '.join(map(str, row)) + '\n')

def main():
    # Main function to solve Kropki Sudoku from input file
    if len(sys.argv) != 3:
        print("Usage: python kropki_solver.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Read input
    initial_board, horizontal_dots, vertical_dots = read_input_file(input_file)
    sudoku = KropkiSudoku(initial_board, horizontal_dots, vertical_dots)
    
    # Solve and handle result
    if sudoku.solve():
        solution = sudoku.print_solution()
        write_output_file(output_file, solution)
        print(f"Solution written to {output_file}")
    else:
        print("No solution exists.")

if __name__ == "__main__":
    main()

import sys
from typing import List, Tuple, Set

class KropkiSudoku:
    def __init__(self, initial_board: List[List[int]], 
                 horizontal_dots: List[List[int]], 
                 vertical_dots: List[List[int]]):
        """
        Initialize the Kropki Sudoku solver
        
        Args:
        - initial_board: 9x9 grid of initial values (0 for empty cells)
        - horizontal_dots: Dot constraints between horizontally adjacent cells
        - vertical_dots: Dot constraints between vertically adjacent cells
        """
        self.board = [row[:] for row in initial_board]
        self.horizontal_dots = horizontal_dots
        self.vertical_dots = vertical_dots
    
    def is_valid_assignment(self, row: int, col: int, num: int) -> bool:
        """
        Check if assigning 'num' to cell (row, col) is valid
        
        Checks:
        1. Row constraint
        2. Column constraint
        3. 3x3 block constraint
        4. Kropki dot constraints
        """
        # Check row constraint
        for c in range(9):
            if c != col and self.board[row][c] == num:
                return False
        
        # Check column constraint
        for r in range(9):
            if r != row and self.board[r][col] == num:
                return False
        
        # Check 3x3 block constraint
        block_row, block_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(block_row, block_row + 3):
            for c in range(block_col, block_col + 3):
                if (r, c) != (row, col) and self.board[r][c] == num:
                    return False
        
        # Check Kropki dot constraints for adjacent cells
        # Horizontal checks
        if col > 0 and len(self.horizontal_dots) > row and len(self.horizontal_dots[row]) > col-1:
            left_val = self.board[row][col-1]
            dot_val = self.horizontal_dots[row][col-1]
            if left_val != 0 and dot_val != 0:
                # White dot (difference of 1)
                if dot_val == 1:
                    if not ((left_val + 1 == num) or (num + 1 == left_val)):
                        return False
                # Black dot (one is double the other)
                elif dot_val == 2:
                    if not ((left_val * 2 == num) or (num * 2 == left_val)):
                        return False
        
        # Vertical checks
        if row > 0 and len(self.vertical_dots) > row-1 and len(self.vertical_dots[row-1]) > col:
            up_val = self.board[row-1][col]
            dot_val = self.vertical_dots[row-1][col]
            if up_val != 0 and dot_val != 0:
                # White dot (difference of 1)
                if dot_val == 1:
                    if not ((up_val + 1 == num) or (num + 1 == up_val)):
                        return False
                # Black dot (one is double the other)
                elif dot_val == 2:
                    if not ((up_val * 2 == num) or (num * 2 == up_val)):
                        return False
        
        return True
    
    def select_unassigned_variable(self) -> Tuple[int, int]:
        """
        Select unassigned variable using Minimum Remaining Values (MRV)
        and Degree heuristic as a tie-breaker
        """
        min_domain_size = 10
        selected_var = None
        max_constraints = -1
        
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    # Count possible values
                    domain_size = sum(1 for num in range(1, 10) 
                                      if self.is_valid_assignment(row, col, num))
                    
                    # Count constraints (neighboring filled cells)
                    constraint_count = self.count_constraints(row, col)
                    
                    # MRV with degree heuristic as tie-breaker
                    if (domain_size < min_domain_size or 
                        (domain_size == min_domain_size and constraint_count > max_constraints)):
                        min_domain_size = domain_size
                        selected_var = (row, col)
                        max_constraints = constraint_count
        
        return selected_var
    
    def count_constraints(self, row: int, col: int) -> int:
        """
        Count the number of constraints (neighboring filled cells)
        """
        constraints = 0
        
        # Check row
        for c in range(9):
            if c != col and self.board[row][c] != 0:
                constraints += 1
        
        # Check column
        for r in range(9):
            if r != row and self.board[r][col] != 0:
                constraints += 1
        
        return constraints
    
    def solve(self) -> bool:
        """
        Backtracking algorithm to solve the Kropki Sudoku
        """
        # Find unassigned variable
        var = self.select_unassigned_variable()
        
        # If no unassigned variables, puzzle is solved
        if var is None:
            return True
        
        row, col = var
        
        # Try values 1-9 in increasing order
        for num in range(1, 10):
            if self.is_valid_assignment(row, col, num):
                # Make assignment
                self.board[row][col] = num
                
                # Recursive call
                if self.solve():
                    return True
                
                # Backtrack
                self.board[row][col] = 0
        
        return False
    
    def print_solution(self):
        """
        Print the solution to console and return as 2D list
        """
        for row in self.board:
            print(' '.join(map(str, row)))
        return self.board

def read_input_file(filename: str) -> Tuple[List[List[int]], List[List[int]], List[List[int]]]:
    """
    Read input file and parse Sudoku board and dot constraints
    """
    with open(filename, 'r') as f:
        # Read initial board
        initial_board = []
        for _ in range(9):
            row = list(map(int, f.readline().split()))
            initial_board.append(row)
        
        # Skip blank line
        f.readline()
        
        # Read horizontal dots
        horizontal_dots = []
        for _ in range(9):
            row = list(map(int, f.readline().split()))
            horizontal_dots.append(row)
        
        # Skip blank line
        f.readline()
        
        # Read vertical dots
        vertical_dots = []
        for _ in range(8):
            row = list(map(int, f.readline().split()))
            vertical_dots.append(row)
        
    return initial_board, horizontal_dots, vertical_dots

def write_output_file(filename: str, solution: List[List[int]]):
    """
    Write solution to output file
    """
    with open(filename, 'w') as f:
        for row in solution:
            f.write(' '.join(map(str, row)) + '\n')

def main():
    """
    Main function to solve Kropki Sudoku from input file
    """
    if len(sys.argv) != 3:
        print("Usage: python kropki_solver.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Read input
    initial_board, horizontal_dots, vertical_dots = read_input_file(input_file)
    
    # Create and solve Sudoku
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
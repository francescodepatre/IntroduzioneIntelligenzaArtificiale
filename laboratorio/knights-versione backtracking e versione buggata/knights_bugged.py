moves = [(0, 0), (-1, -2), (1, -2), (2, -1), (2, 1), (-1, 2), (1, 2), (-2, -1), (-2, 1)]

def utility(board, n, x, y) -> int:
    count = 0
    for dx, dy in moves:
        x1, y1 = x + dx, y + dy
        if 0 <= x1 < n and 0 <= y1 < n and board[y1 * n + x1] == 0:
            count += 1
    return count
            
def place_knight(board, n, x, y):
    for dx, dy in moves:
        x1, y1 = x + dx, y + dy
        if 0 <= x1 < n and 0 <= y1 < n:
            board[y1 * n + x1] += 1
    board[y * n + x] += 10

def remove_knight(board, n, x, y):
    for dx, dy in moves:
        x1, y1 = x + dx, y + dy
        if 0 <= x1 < n and 0 <= y1 < n:
            board[y1 * n + x1] -= 1    
    board[y * n + x] -= 10

def solve(board, n, k):
    best = board[:]
    best_val = board.count(0), sum(1 for v in board if v >= 10)
    if all(board):
        return best
    if k == 0:
        return best

    options = []
    i = board.index(0)
    x0, y0 = i % n, i // n
    for dx, dy in moves:
        x1, y1 = x0 + dx, y0 + dy
        if 0 <= x1 < n and 0 <= y1 < n:
            v = utility(board, n, x1, y1)
            options.append((-v, x1, y1))
    options.sort()
    for v, x, y in options:        
        place_knight(board, n, x, y)
        board = solve(board, n, k-1)
        val = board.count(0), sum(1 for v in board if v >= 10)
        if val < best_val:
            best = board[:]
        remove_knight(board, n, x, y)
    return best

ks = [(0,0),(1,1),(2,4),(3,4),(4,4),(5,5),(6,8),(7,10),(8,12),(9,14),(10,16),(11,21),
          (12,24),(13,28),(14,32),(15,36),(16,40),(17,46),(18,52),(19,57),(20,62),(21,68)]


n, k = 6, 8

board = [0] * (n * n)
board = solve(board, n, k)

for y in range(n):
    for x in range(n):
        print(board[y * n + x], end="\t")
    print()

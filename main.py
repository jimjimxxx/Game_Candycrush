import random
import copy

# 印出棋盤
def create_board(row, col, candytype):
    board = [[random.randint(1, candytype) for _ in range(col)] for _ in range(row)]
    return board


def print_board(board):
    print("+---" * len(board[0]) + "+")
    for i, row in enumerate(board):
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print(f" {i}")
        print("+" + "---+" * len(row))
    print(" ", end="")
    for col in range(len(board[0])):
        print(f" {col:^2} ", end="")
    print("\n")
    return board


# 檢查輸入是否合法(正整數)
def check_input(row, col, candytype):
    row = int(row) if row.isdigit() else None
    col = int(col) if col.isdigit() else None
    candytype = int(candytype) if candytype.isdigit() else None

    while not all([row is not None, col is not None, candytype is not None]):
        print("輸入不合法，請重新輸入：")

        if row is None:
            row = input("row需為正整數，請再輸入一次row：")
            row = int(row) if row.isdigit() else None

        if col is None or col <= 0:
            col = input("col需為正整數，請再輸入一次col：")
            col = int(col) if col.isdigit() else None

        if candytype is None or candytype <= 0:
            candytype = input("candytype需為正整數,請在輸入一次candytype：")
            candytype = int(candytype) if candytype.isdigit() else None

    return row, col, candytype


# 如果當前棋盤沒有可以透過一步移動就消除的糖果，則重新印出一張棋盤，糖果重新隨機分布(需要引用其他函式)
def has_one_step_match(board):
    rows = len(board)
    cols = len(board[0])

    for row in range(rows):
        for col in range(cols):
            # 嘗試上下左右四個方向進行交換
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row = row + dr
                new_col = col + dc

                # 檢查新的位置是否在合法的範圍內
                if new_row >= 0 and new_row < rows and new_col >= 0 and new_col < cols:
                    # 交換兩個單元格的值
                    board[row][col], board[new_row][new_col] = board[new_row][new_col], board[row][col]

                    # 檢查交換後的棋盤是否有可消除的糖果
                    matched_candies = check_matched_candies(board)

                    # 恢復原始的單元格值
                    board[row][col], board[new_row][new_col] = board[new_row][new_col], board[row][col]

                    # 如果有可消除的糖果，返回 True
                    if len(matched_candies) > 0:
                        return True

    # 如果遍歷完整個棋盤都沒有找到可消除的糖果，返回 False
    return False


# 檢查是否有可消除的連續糖果(消除哪些)
def check_matched_candies(board):
    rows = len(board)
    cols = len(board[0])
    matched_candies = []

    # 檢查橫向連線
    for row in range(rows):
        for col in range(cols - 2):
            if board[row][col] == board[row][col + 1] == board[row][col + 2]:
                matched_candies.append((row, col))
                matched_candies.append((row, col + 1))
                matched_candies.append((row, col + 2))
                if col + 3 < cols:
                    for k in range(cols + 3, cols):
                        if board[row][k] == board[row][k - 1]:
                            matched_candies.append(row, k)
                        else:
                            break

    # 檢查縱向連線
    for col in range(cols):
        for row in range(rows - 2):
            if board[row][col] == board[row + 1][col] == board[row + 2][col]:
                matched_candies.append((row, col))
                matched_candies.append((row + 1, col))
                matched_candies.append((row + 2, col))
                if row + 3 < rows:
                    for k in range(row + 3, rows):
                        if board[k][col] == board[k - 1][col]:
                            matched_candies.append((k, col))
                        else:
                            break
    matched_candies = set(matched_candies)  # 要被消除的糖果

    return matched_candies  # 返回可消除糖果的列表


# 檢查交換位置是否有效
def is_valid_swap(board, row1, col1, row2, col2):
    rows = len(board)
    cols = len(board[0])

    # 檢查是否超過範圍
    if (
        row1 < 0
        or row1 >= rows
        or col1 < 0
        or col1 >= cols
        or row2 < 0
        or row2 >= rows
        or col2 < 0
        or col2 >= cols
    ):
        print("Opps，有糖果的座標超出範圍了喔，請再輸入一次範圍內的糖果")
        return False
    # 檢查交換位置是否相鄰
    if (abs(row1 - row2) + abs(col1 - col2)) != 1:
        print("這兩個糖果的位置不相鄰，請重新挑選相鄰的糖果")
        return False

    copy_board = copy.deepcopy(board)

    temp = copy_board[row1][col1]
    copy_board[row1][col1] = copy_board[row2][col2]
    copy_board[row2][col2] = temp
    matched_candies = check_matched_candies(copy_board)

    if len(matched_candies) > 0:  ## 先拿複製的棋盤丟進函式內確認能不能消除
        # 可以消除的話就對主棋盤處理
        board[row1][col1] = board[row2][col2]
        board[row2][col2] = temp
        return True
    else:
        print("這兩個糖果不能交換，請重新選擇想交換的糖果")
        return False


# 將可以消除的糖果消除，上面的糖果要向下遞補空格，最頂端隨機生成糖果
def fill_board(board, candytype, matched_candies):
    rows = len(board)
    cols = len(board[0])

    for row, col in matched_candies:  # 將可以消除的糖果消除，暫時視為0
        board[row][col] = 0

    for col in range(cols):  # 執行糖果的遞補
        empty_cells = 0
        for row in range(rows - 1, -1, -1):
            if board[row][col] == 0:
                empty_cells += 1
            elif empty_cells > 0:
                board[row + empty_cells][col] = board[row][col]
                board[row][col] = 0

    # 在頂端隨機生成糖果
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0:
                board[row][col] = random.randint(1, candytype)
    return board


# 計分機制(消除3~6顆>倍率1，消除7~12顆>倍率2，消除12顆以上>倍率5)
def score_(score, matched_candies):
    point = len(matched_candies)
    multiplier = 1
    if 3 <= point <= 6:
        multiplier = 1
    elif 7 <= point <= 12:
        multiplier = 2
    elif point > 12:
        multiplier = 5
    else:
        return score  # 分數沒有改變的情形

    score += point * multiplier

    return score


# 重複檢查棋盤，直到棋盤上的糖果沒有可以不透過移動就消除，和棋盤上有透過移動一步就消除的情況
def important_check(score, board, row, col, candytype):
    TT=True
    while TT:  # 檢查有沒有可以不透過移動就消除的糖

        matched_candies = check_matched_candies(board)
        if len(matched_candies) == 0 and not has_one_step_match(board):  # 沒辦法消除，要重新生成棋盤
            print("棋盤沒有可移動消除的糖果，重新隨機印出棋盤")
            print()
            board = create_board(row, col, candytype)
            print_board(board)
            matched_candies = check_matched_candies(board)
            score = score_(score, matched_candies)
            if len(matched_candies) == 0 and has_one_step_match(board):
                TT=False
        elif len(matched_candies) != 0:  # 可以消除
            fill_board(board, candytype, matched_candies)
            score = score_(score, matched_candies)
        elif len(matched_candies) == 0 and has_one_step_match(board):
            TT=False

    return score


# 主遊戲
def play_game():
    row = input("輸入棋盤的列數:")
    col = input("輸入棋盤的行數:")
    candytype = input("輸入糖果的種類:")
    row, col, candytype = check_input(row, col, candytype)

    board = create_board(row, col, candytype)
    print_board(board)
    score = 0
    eliminate_numbers = 15  # 交換糖果15次後結束(有成功交換和沒有成功交換都要算進步數)

    while eliminate_numbers > 1:## 有剩餘步數時才可以移動
        score = important_check(score, board, row, col, candytype)
        print()
        print("當前分數為",score,"(此為包含天降後消除的分數)")
        print()
        print("剩餘移動步數為:", eliminate_numbers)

        # 當有可以消除的糖果時才可以輸入
        if has_one_step_match(board):
            print_board(board)
            row1 = int(input("請輸入第一個要交換的單元格的列數："))
            col1 = int(input("請輸入第一個要交換的單元格的行數："))
            row2 = int(input("請輸入第二個要交換的單元格的列數："))
            col2 = int(input("請輸入第二個要交換的單元格的行數："))
            if is_valid_swap(board, row1, col1, row2, col2):  # 檢查兩個糖果座標是否可以交換，若不能交換，則讓使用者再輸入一次
                score = important_check(score, board, row, col, candytype)

                eliminate_numbers -= 1
                if eliminate_numbers == 0:
                    break

            elif not is_valid_swap(board, row1, col1, row2, col2):
                eliminate_numbers -= 1
                if eliminate_numbers == 0:
                    break
                continue
    print("遊戲結束，最終得分為", score)


play_game()

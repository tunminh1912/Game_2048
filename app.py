from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

VAL_CHOICE = [2, 4]
souc = 0  # Điểm số
ds = []  # Bàn cờ

def init_matrix():
    global ds
    ds = [[0 for _ in range(4)] for _ in range(4)]
    for _ in range(2):
        add_block()
    return ds

def add_block():
    while True:
        i = random.randint(0, 3)
        j = random.randint(0, 3)
        if ds[i][j] == 0:
            ds[i][j] = random.choice(VAL_CHOICE)
            break

def move_left():
    global souc
    moved = False
    for i in range(4):
        new_row = [x for x in ds[i] if x != 0]
        combined_row = []
        j = 0
        while j < len(new_row):
            if j + 1 < len(new_row) and new_row[j] == new_row[j + 1]:
                combined_row.append(new_row[j] * 2)
                souc += new_row[j] * 2
                j += 2
            else:
                combined_row.append(new_row[j])
                j += 1
        combined_row += [0] * (4 - len(combined_row))
        if combined_row != ds[i]:
            moved = True
        ds[i] = combined_row
    return moved

def move_right():
    global souc
    moved = False
    for i in range(4):
        # Combine tiles and move right
        new_row = [x for x in ds[i] if x != 0][::-1]
        combined_row = []
        j = 0
        while j < len(new_row):
            if j + 1 < len(new_row) and new_row[j] == new_row[j + 1]:
                combined_row.append(new_row[j] * 2)
                souc += new_row[j] * 2
                j += 2  # Skip the next tile
            else:
                combined_row.append(new_row[j])
                j += 1
        combined_row += [0] * (4 - len(combined_row))  # Fill the rest with zeros
        combined_row.reverse()  # Reverse to original order
        if combined_row != ds[i]:
            moved = True
        ds[i] = combined_row
    return moved

def move_up():
    global souc
    moved = False
    for j in range(4):
        # Combine tiles and move up
        new_column = [ds[i][j] for i in range(4) if ds[i][j] != 0]
        combined_column = []
        k = 0
        while k < len(new_column):
            if k + 1 < len(new_column) and new_column[k] == new_column[k + 1]:
                combined_column.append(new_column[k] * 2)
                souc += new_column[k] * 2
                k += 2  # Skip the next tile
            else:
                combined_column.append(new_column[k])
                k += 1
        combined_column += [0] * (4 - len(combined_column))  # Fill the rest with zeros
        for i in range(4):
            if i < len(combined_column):
                if combined_column[i] != ds[i][j]:
                    moved = True
                ds[i][j] = combined_column[i]
            else:
                ds[i][j] = 0
    return moved

def move_down():
    global souc
    moved = False
    for j in range(4):
        # Combine tiles and move down
        new_column = [ds[i][j] for i in range(4) if ds[i][j] != 0][::-1]
        combined_column = []
        k = 0
        while k < len(new_column):
            if k + 1 < len(new_column) and new_column[k] == new_column[k + 1]:
                combined_column.append(new_column[k] * 2)
                souc += new_column[k] * 2
                k += 2  # Skip the next tile
            else:
                combined_column.append(new_column[k])
                k += 1
        combined_column += [0] * (4 - len(combined_column))  # Fill the rest with zeros
        combined_column.reverse()  # Reverse to original order
        for i in range(4):
            if i < len(combined_column):
                if combined_column[i] != ds[i][j]:
                    moved = True
                ds[i][j] = combined_column[i]
            else:
                ds[i][j] = 0
    return moved
def check_win():
    for row in ds:
        if 2048 in row:
            return True
    return False

def check_loss():
    for i in range(4):
        for j in range(4):
            if ds[i][j] == 0:
                return False
            if i < 3 and ds[i][j] == ds[i + 1][j]:
                return False
            if j < 3 and ds[i][j] == ds[i][j + 1]:
                return False
    return True

def updateBXH(score):
    try:
        with open('BXH.txt', 'r') as file:
            ranks = [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        ranks = []

    if len(ranks) < 10 or score > ranks[-1]:
        ranks.append(score)
        ranks = sorted(ranks, reverse=True)[:10]
        with open('BXH.txt', 'w') as file:
            file.writelines([f"{s}\n" for s in ranks])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game')
def new_game():
    global ds, souc
    ds = init_matrix()
    souc = 0
    return jsonify({'matrix': ds, 'score': souc, 'status': 'ongoing'})

@app.route('/move/<direction>')
def move(direction):
    global ds, souc
    moved = False
    if direction == 'left':
        moved = move_left()
    elif direction == 'right':
        moved = move_right()
    elif direction == 'up':
        moved = move_up()
    elif direction == 'down':
        moved = move_down()

    if moved:
        add_block()

    if check_win():
        updateBXH(souc)
        return jsonify({'matrix': ds, 'score': souc, 'status': 'winner'})

    if check_loss():
        updateBXH(souc)
        return jsonify({'matrix': ds, 'score': souc, 'status': 'game_over'})

    return jsonify({'matrix': ds, 'score': souc, 'status': 'ongoing'})

@app.route('/rank')
def rank():
    try:
        with open('BXH.txt', 'r') as file:
            ranks = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        ranks = []

    return render_template('rank.html', ranks=ranks)

if __name__ == '__main__':
    app.run(debug=True)

import random

faces = ['U', 'D', 'L', 'R', 'F', 'B']
modifiers = ['', "'", '2']

# Group faces by axis
axes = {
    'U': 'UD', 'D': 'UD',
    'L': 'LR', 'R': 'LR',
    'F': 'FB', 'B': 'FB'
}

def generate_scramble(length=20):
    scramble = []
    prev_face = None
    prev_axis = None

    for _ in range(length):
        while True:
            face = random.choice(faces)
            axis = axes[face]

            # Rule 1: no same face twice in a row
            if face == prev_face:
                continue

            # Rule 2: no same axis three times in a row
            # (prevents sequences like R L R)
            if axis == prev_axis:
                continue

            move = face + random.choice(modifiers)
            scramble.append(move)

            prev_face = face
            prev_axis = axis
            break

    return ' '.join(scramble)

def generate_scramble_vis(scramble: str):
    left = [["o","o","o"],
            ["o","o","o"],
            ["o","o","o"]]
    front = [["g","g","g"],
            ["g","g","g"],
            ["g","g","g"]]
    right = [["r","r","r"],
            ["r","r","r"],
            ["r","r","r"]]
    back = [["b","b","b"],
            ["b","b","b"],
            ["b","b","b"]]
    top = [["w","w","w"],
            ["w","w","w"],
            ["w","w","w"]]
    bottom = [["y","y","y"],
            ["y","y","y"],
            ["y","y","y"]]

    def rotate90(mat):
        n = len(mat)

        for i in range(n // 2):

            for j in range(i, n - i - 1):

                temp = mat[i][j]
                mat[i][j] = mat[n - 1 - j][i]                # Move P4 to P1
                mat[n - 1 - j][i] = mat[n - 1 - i][n - 1 - j]  # Move P3 to P4
                mat[n - 1 - i][n - 1 - j] = mat[j][n - 1 - i]  # Move P2 to P3
                mat[j][n - 1 - i] = temp                      # Move P1 to P2

    def move_U():
        rotate90(top)
        temp = left[0].copy()
        left[0] = front[0]
        front[0] = right[0]
        right[0] = back[0]
        back[0] = temp

    def move_D():
        rotate90(bottom)
        temp = left[2].copy()
        left[2] = back[2]
        back[2] = right[2]
        right[2] = front[2]
        front[2] = temp

    def move_R():
        rotate90(right)
        temp = [top[0][2],top[1][2],top[2][2]]
        top[0][2],top[1][2],top[2][2] = front[0][2],front[1][2],front[2][2]
        front[0][2],front[1][2],front[2][2] = bottom[0][2],bottom[1][2],bottom[2][2]
        bottom[2][2],bottom[1][2],bottom[0][2] = back[0][0],back[1][0],back[2][0]
        back[0][0],back[1][0],back[2][0] = temp[2],temp[1],temp[0]

    def move_L():
        rotate90(left)
        temp = [top[0][0],top[1][0],top[2][0]]
        top[0][0],top[1][0],top[2][0] = back[2][2],back[1][2],back[0][2]
        back[0][2],back[1][2],back[2][2] = bottom[2][0],bottom[1][0],bottom[0][0]
        bottom[2][0],bottom[1][0],bottom[0][0] = front[2][0],front[1][0],front[0][0]
        front[0][0],front[1][0],front[2][0] = temp[0],temp[1],temp[2]


    def move_F():
        rotate90(front)
        temp = top[2].copy()
        top[2] = [left[2][2],left[1][2],left[0][2]]
        left[0][2], left[1][2], left[2][2] = bottom[0]
        bottom[0] = [right[2][0], right[1][0], right[0][0]]
        right[0][0], right[1][0], right[2][0] = temp

    def move_B():
        rotate90(back)
        temp = top[0].copy()
        top[0] = [right[0][2],right[1][2],right[2][2]]
        right[2][2], right[1][2], right[0][2] = bottom[2]
        bottom[2] = [left[0][0], left[1][0], left[2][0]]
        left[2][0], left[1][0], left[0][0] = temp
    
    scramble_steps = scramble.split(" ")
    step_to_func = {"U": move_U,
                    "D": move_D,
                    "L": move_L,
                    "R": move_R,
                    "F": move_F,
                    "B": move_B}

    for step in scramble_steps:
        if len(step) > 1:
            if step[1] == "'":
                for _ in range(0,3):
                    step_to_func[step[0]]()
            elif step[1] == "2":
                for _ in range(0,2):
                    step_to_func[step[0]]()
        else:
            step_to_func[step[0]]()
    
    def print_2d():
        filler = [' ',' ',' ']
        string = f"""
        {filler} {top[0]} {filler} {filler}
        {filler} {top[1]} {filler} {filler}
        {filler} {top[2]} {filler} {filler}

        {left[0]} {front[0]} {right[0]} {back[0]}
        {left[1]} {front[1]} {right[1]} {back[1]}
        {left[2]} {front[2]} {right[2]} {back[2]}
        
        {filler} {bottom[0]} {filler} {filler}
        {filler} {bottom[1]} {filler} {filler}
        {filler} {bottom[2]} {filler} {filler}
        """
        print(string)

    return {"top": top, "bottom": bottom, "front": front, "back": back, "left": left, "right": right}

if __name__ == "__main__":
    scramble = generate_scramble()
    print(f"Scramble: {scramble}")
    generate_scramble_vis(scramble)

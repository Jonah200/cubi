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

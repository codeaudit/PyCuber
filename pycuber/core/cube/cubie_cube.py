import numpy as np
from colorama import Back
from .cube_array import CubeArray
from .cube_abc import CubeABC
from .constants import X, Y, Z, U, L, F, R, B, D
from ..formula import Move


rotation_parameters = {
    Move("L"): (X, 0, -1),
    Move("M"): (X, 1, -1),
    Move("R"): (X, 2, 1),

    Move("D"): (Y, 0, -1),
    Move("E"): (Y, 1, -1),
    Move("U"): (Y, 2, 1),

    Move("F"): (Z, 0, -1),
    Move("S"): (Z, 1, -1),
    Move("B"): (Z, 2, 1),
}

for step in list(rotation_parameters.keys()):
    axis, layer, k = rotation_parameters[step]
    rotation_parameters[step.inverse()] = (axis, layer, k * -1)
    rotation_parameters[step * 2] = (axis, layer, k * 2)

combinations = {
    Move("l"): [Move("L"), Move("M")],
    Move("r"): [Move("M'"), Move("R")],
    Move("x"): [Move("L'"), Move("M'"), Move("R")],

    Move("d"): [Move("D"), Move("E")],
    Move("u"): [Move("E'"), Move("U")],
    Move("y"): [Move("D'"), Move("E'"), Move("U")],

    Move("f"): [Move("F"), Move("S")],
    Move("b"): [Move("S'"), Move("B")],
    Move("z"): [Move("F"), Move("S"), Move("B'")],
}

for step, comb in list(combinations.items()):
    combinations[step.inverse()] = [s.inverse() for s in comb]
    combinations[step * 2] = [s * 2 for s in comb]


default_colours = {
    U: Back.YELLOW,
    L: Back.RED,
    F: Back.GREEN,
    R: Back.MAGENTA,
    B: Back.BLUE,
    D: Back.WHITE,
}


class CubieCube(object):

    def __init__(self):
        super().__init__()
        self.__data = CubeArray()

    def _do_step(self, step):
        if step.face.isupper():
            self.__data.twist(*rotation_parameters[step])
        else:
            for s in combinations[step]:
                self.__data.twist(*rotation_parameters[s])
        return self

    def _do_formula(self, formula):
        for step in formula:
            self.do_step(step)
        return self

    def _get_face(self, face):
        return self.__data.get_face(face)

    def _get_drawing(self, **colours):
        colours = {**default_colours, **colours}
        faces = {face: self.get_face(face) for face in [U, L, F, R, B, D]}
        s = ""
        for row in faces[U]:
            s += "      " + "".join("%s  " % colours[p] for p in row)
            s += Back.RESET + "\n"
        for zipped_rows in zip(faces[L], faces[F], faces[R], faces[B]):
            for row in zipped_rows:
                s += "".join("%s  " % colours[p] for p in row)
            s += Back.RESET + "\n"
        for row in faces[D]:
            s += "      " + "".join("%s  " % colours[p] for p in row)
            s += Back.RESET + "\n"
        return s

    def _get_cubie(self, face_indexed_position):
        selector = [1, 1, 1]
        for face in face_indexed_position:
            if face in (L, R):
                selector[X] = [L, None, R].index(face)
            elif face in (D, U):
                selector[Y] = [D, None, U].index(face)
            elif face in (F, B):
                selector[Z] = [F, None, B].index(face)
        return self.__data[tuple(selector)].view(np.ndarray)


CubeABC.register(CubieCube)
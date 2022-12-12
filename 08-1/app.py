from enum import Enum, auto
from typing import List


class Direction(Enum):
    TOP = auto()
    BOTTOM = auto()
    LEFT = auto()
    RIGHT = auto()


def count_visible_trees(tree_matrix: List[List[int]]) -> int:
    def view_from_direction(viewing_matrix: List[List[int]], local_x: int, local_y: int, direction: Direction) -> List[int]:
        section: List[int] = []
        if direction == Direction.TOP:
            section = [viewing_matrix[i][local_x] for i in range(0, local_y + 1)]
        elif direction == Direction.BOTTOM:
            section = [viewing_matrix[i][local_x] for i in range(len(viewing_matrix) - 1, local_y - 1, -1)]
        elif direction == Direction.LEFT:
            section = [viewing_matrix[local_y][i] for i in range(0, local_x + 1)]
        elif direction == Direction.RIGHT:
            section = [viewing_matrix[local_y][i] for i in range(len(viewing_matrix[local_y]) - 1, local_x - 1, -1)]

        return section

    # Count all trees visible from the edges of the matrix
    count: int = (2 * len(tree_matrix)) + (2 * len(tree_matrix[0])) - 4

    max_scenic_score: int = 0
    for y in range(1, len(tree_matrix) - 1):
        for x in range(1, len(tree_matrix[0]) - 1):
            tree_visible: bool = False
            scenic_score: int = 1
            for d in [Direction.TOP, Direction.BOTTOM, Direction.LEFT, Direction.RIGHT]:
                view: List[int] = view_from_direction(tree_matrix, x, y, d)

                if view[-1] > max(view[:-1]):
                    tree_visible = True

                # Change perspective to the tree itself
                view.reverse()
                scenic_view: int = next((i + 1 for i, v in enumerate(view[1:]) if v >= view[0]), len(view) - 1)
                scenic_score *= scenic_view

            if scenic_score > max_scenic_score:
                max_scenic_score = scenic_score

            if tree_visible:
                count += 1

    print(max_scenic_score)
    return count


with open("input.txt") as file:
    trees: List[List[int]] = []

    for line in file:
        trees.append([int(x) for x in line.strip()])

    print(count_visible_trees(trees))

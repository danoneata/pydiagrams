from dataclasses import dataclass
from typing import Any

from colour import Color

import chalk.transform as tx
from chalk.shapes.path import Path
from chalk.shapes.shape import Shape
from chalk.transform import P2, BoundingBox
from chalk.types import Diagram
from chalk.visitor import C, ShapeVisitor

black = Color("black")


def tri() -> Diagram:
    return (
        Path.from_list_of_tuples(
            [(1.0, 0), (0.0, -1.0), (-1.0, 0), (1.0, 0)], closed=True
        )
        .stroke()
        .rotate_by(-0.25)
        .fill_color(Color("black"))
        .center_xy()
        .align_r()
        .line_width(0)
    )


def dart(cut: float = 0.2) -> Diagram:
    return (
        Path.from_list_of_tuples(
            [
                (0, -cut),
                (1.0, cut),
                (0.0, -1.0 - cut),
                (-1.0, +cut),
                (0, -cut),
            ],
            closed=True,
        )
        .stroke()
        .rotate_by(-0.25)
        .fill_color(Color("black"))
        .center_xy()
        .align_r()
        .line_width(0)
    )


@dataclass
class ArrowHead(Shape):
    """Arrow Head."""

    arrow_shape: Diagram

    def get_bounding_box(self) -> BoundingBox:
        # Arrow head don't have a bounding box since we can't accurately know
        # the size until rendering
        eps = 1e-4
        self.bb = BoundingBox(tx.X.origin, tx.X.origin + P2(eps, eps))
        return self.bb

    def accept(self, visitor: ShapeVisitor[C], **kwargs: Any) -> C:
        return visitor.visit_arrowhead(self, **kwargs)

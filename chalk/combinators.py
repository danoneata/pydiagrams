from typing import Iterable, List, Optional, Tuple

import chalk.transform as tx
from chalk.monoid import associative_reduce
from chalk.path import Path
from chalk.transform import Floating, Scalars, V2_t
from chalk.types import (
    BatchDiagram,
    BroadDiagram,
    Diagram,
    EmptyDiagram,
    ExtraDiagram,
)

# Functions mirroring Diagrams.Combinators and Diagrams.2d.Combinators


def with_envelope(self: Diagram, other: Diagram) -> Diagram:
    """
    Act as if the envelope of `other` is the envelope of `self`.
    """
    self, other = self.broadcast_diagrams(other)
    return self.compose(other)


def pad(self: Diagram, extra: Floating) -> Diagram:
    """Scale outward directed padding for a diagram.

    Be careful using this if your diagram is not centered.
    """
    envelope = self.get_envelope()
    bounding_box = envelope.to_bounding_box()
    rect = bounding_box.scale(extra).to_rect()
    self, rect = self.broadcast_diagrams(rect)
    assert rect.shape == self.shape, f"{rect.shape} {self.shape}"
    return self.with_envelope(rect)


# extrudeEnvelope, intrudeEnvelope


def atop(self: BatchDiagram, other: BatchDiagram) -> BroadDiagram:
    return self.compose(None, other)


# beneath


def above(self: BatchDiagram, other: BatchDiagram) -> BroadDiagram:
    return beside(self, other, tx.unit_y)


# appends


def beside(
    self: BatchDiagram, other: BatchDiagram, direction: V2_t
) -> BroadDiagram:
    return atop(self, juxtapose(self, other, direction))


def place_at(
    diagrams: Iterable[Diagram], points: List[Tuple[float, float]]
) -> Diagram:
    return concat(d.translate(x, y) for d, (x, y) in zip(diagrams, points))


def place_on_path(diagrams: Iterable[Diagram], path: Path) -> Diagram:
    return concat(d.translate_by(p) for d, p in zip(diagrams, path.points()))


def batch_hcat(
    self: ExtraDiagram, sep: Optional[Floating] = None
) -> BatchDiagram:
    "Hcat a batched diagram along the outermost axis."
    return batch_cat(self, tx.unit_x, sep)


def batch_vcat(
    self: ExtraDiagram, sep: Optional[Floating] = None
) -> BatchDiagram:
    "Vcat a batched diagram along the outermost axis."
    return batch_cat(self, tx.unit_y, sep)


def batch_cat(
    diagram: ExtraDiagram, v: V2_t, sep: Optional[Floating] = None
) -> BatchDiagram:
    """
    Cat a batched diagram along the outermost axis.
    i.e. if it is size (a,b) it will now be (b)
    """
    axes = diagram.size()
    axis = len(axes) - 1
    assert diagram.size() != ()
    diagram = diagram._normalize()

    if sep is None:
        sep = 0

    def call_scan(diagram: Diagram) -> Diagram:
        env = diagram.get_envelope()
        right = env(v)
        left = env(-v)
        off = tx.np.roll(right, 1) + left + sep
        off = tx.index_update(off, 0, 0)
        off = tx.np.cumsum(off, axis=0)
        t = v * off[..., None, None]
        return diagram.translate_by(t)
    

    call_scan = tx.multi_vmap(call_scan, axis)  # type: ignore
    return call_scan(diagram).compose_axis()


def cat(
    diagram: Iterable[Diagram], v: V2_t, sep: Optional[Floating] = None
) -> Diagram:
    from chalk.shapes import hstrut

    diagrams = iter(diagram)
    start = next(diagrams, None)
    if sep is None:
        hs = empty()
    else:
        hs = hstrut(sep)
    sep_dia = hs.rotate(tx.angle(v))
    if start is None:
        return empty()

    def fn(a: Diagram, b: Diagram) -> Diagram:
        return a.beside(sep_dia, v).beside(b, v)

    return fn(start, associative_reduce(fn, diagrams, empty()))


def batch_concat(self: ExtraDiagram) -> BatchDiagram:
    size = self.size()
    assert size != ()
    return self.compose_axis()


def concat(diagrams: Iterable[BatchDiagram]) -> BroadDiagram:
    """
    Concat diagrams atop of each other with atop.
    """
    from chalk.core import BaseDiagram

    assert not isinstance(
        diagrams, BaseDiagram
    ), "Use diagram.concat() for batched diagrams"

    return BaseDiagram.concat2(diagrams)  # type: ignore


def empty() -> EmptyDiagram:
    "Create an empty diagram"
    from chalk.core import BaseDiagram

    return BaseDiagram.empty()  # type: ignore


# CompaseAligned.

# 2D


def hcat(
    diagrams: Iterable[BatchDiagram], sep: Optional[Floating] = None
) -> BroadDiagram:
    """
    Stack diagrams next to each other with `besides`.

    Args:
        diagrams (Iterable[Diagram]): Diagrams to stack.
        sep (Optional[float]): Padding between diagrams.

    Returns:
        Diagram: New diagram

    """
    return cat(diagrams, tx.unit_x, sep)


def vcat(
    diagrams: Iterable[BatchDiagram], sep: Optional[Floating] = None
) -> BroadDiagram:
    """
    Stack diagrams above each other with `above`.

    Args:
        diagrams (Iterable[Diagram]): Diagrams to stack.
        sep (Optional[float]): Padding between diagrams.

    Returns:
        Diagrams

    """
    return cat(diagrams, tx.unit_y, sep)


# Extra


def above2(self: BatchDiagram, other: BatchDiagram) -> BroadDiagram:
    """Given two diagrams ``a`` and ``b``, ``a.above2(b)``
    places ``a`` on top of ``b``. This moves ``a`` down to
    touch ``b``.

    💡 ``a.above2(b)`` is equivalent to ``a // b``.

    Args:
        self (Diagram): Diagram object.
        other (Diagram): Another diagram object.

    Returns:
        Diagram: A diagram object.
    """
    return beside(other, self, -tx.unit_y)


def juxtapose_snug(
    self: BatchDiagram, other: BatchDiagram, direction: V2_t
) -> BroadDiagram:
    trace1 = self.get_trace()
    trace2 = other.get_trace()
    d1, m1 = trace1.trace_v(tx.origin, direction)
    d2, m2 = trace2.trace_v(tx.origin, -direction)
    assert m1.all()
    assert m2.all()
    d = d1 - d2
    t = tx.translation(d)
    return other.apply_transform(t)


def beside_snug(
    self: BatchDiagram, other: BatchDiagram, direction: V2_t
) -> BroadDiagram:
    return atop(self, juxtapose_snug(self, other, direction))


def juxtapose(
    self: BatchDiagram, other: BatchDiagram, direction: V2_t
) -> BroadDiagram:
    """Given two diagrams ``a`` and ``b``, ``a.juxtapose(b, v)``
    places ``b`` to touch ``a`` along angle ve .

    Args:
        self (Diagram): Diagram object.
        other (Diagram): Another diagram object.
        direction (V2_T): (Normalized) vector angle to juxtapose

    Returns:
        Repositioned ``b`` diagram
    """
    envelope1 = self.get_envelope()
    envelope2 = other.get_envelope()
    d = envelope1.envelope_v(direction) - envelope2.envelope_v(-direction)
    t = tx.translation(d)
    return other.apply_transform(t)


def at_center(self: BatchDiagram, other: BatchDiagram) -> BroadDiagram:
    """Center two given diagrams.

    💡 `a.at_center(b)` means center of ``a`` is translated
    to the center of ``b``, and ``b`` sits on top of
    ``a`` along the axis out of the plane of the image.

    💡 In other words, ``b`` occludes ``a``.
    """
    envelope1 = self.get_envelope()
    t = tx.translation(envelope1.center)
    return self.compose(None, other.apply_transform(t))

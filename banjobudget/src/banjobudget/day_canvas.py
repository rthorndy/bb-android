"""
DayCanvas: A small Canvas widget for rendering a calendar day cell.

Features:
- 4 equal rows.
  • Row 1: day (right-aligned)
  • Row 2: status dots (income = green, expense = blue) centered
  • Row 3: cash (left-aligned)
  • Row 4: spendable (left-aligned)
- on_press handler stub
"""
from __future__ import annotations
from typing import Optional

import toga
from toga.constants import SANS_SERIF
from toga.style import Pack


class DayCanvas(toga.Canvas):
    """A Canvas widget that draws a day cell with indicators and amounts.

    Parameters
    ----------
    day: str
    has_income: bool
    has_expense: bool
    cash: str
    spendable: str
    style: Optional[toga.style.Pack]
        Optional style for sizing (defaults to width=75, height=60).
    """

    def __init__(
        self,
        day: str,
        has_income: bool,
        has_expense: bool,
        cash: str,
        spendable: str,
        is_today: bool,
        is_month: bool,
        month: int,
        year: int,
        style: Optional[Pack] = None,
    ) -> None:
        self.day: str = day
        self.has_income: bool = has_income
        self.has_expense: bool = has_expense
        self.cash: str = cash
        self.spendable: str = spendable
        self.is_today: bool = is_today
        self.is_month: bool = is_month
        self.month = month
        self.year = year


        # Reasonable default footprint for a calendar cell
        default_style = Pack(width=75, height=60)
        use_style = style if style is not None else default_style

        super().__init__(style=use_style)
        # Wire draw + press handlers
        self.on_press = self._on_press
        self.on_alt_press = self._on_press


    # ---- Event handlers ----
    def _on_press(self, _widget: toga.Canvas) -> None:  # Stub for now
        # You can replace this with real selection/navigation later
        # (left as a no-op per request)
        print(f'Click on {self.day}')
        return None

    # ---- Drawing helpers ----
    def _measure_text(self, context, text: str, fallback_char_w: float = 7.0) -> float:
        """Best-effort text width measurement across platforms.
        Falls back to a rough estimate if measurement API is unavailable.
        """
        width = None
        try:
            # Newer Toga contexts expose measure_text returning (width, height) or a size object
            mt = getattr(context, "measure_text", None)
            if callable(mt):
                size = mt(text)
                # size may be a tuple or an object with width attr
                if isinstance(size, tuple) and len(size) >= 1:
                    width = float(size[0])
                elif hasattr(size, "width"):
                    width = float(size.width)
        except (AttributeError, TypeError):
            width = None
        if width is None:
            width = len(text) * fallback_char_w
        return width

    def draw(self, width) -> None:
        # Determine available drawing area
        context = self.context
        context.clear()
        font = toga.Font(family=SANS_SERIF, size=8)
        w = width
        # h = min(100, max(w, 60))
        h = 60

        # print(f'{self.day} drawn to: {w}x{h}, window is {self.window.size if self.window else None}')

        pad = 6
        row_h = h / 4.0

        # Baselines/centers for each row
        y1 = row_h * 0 + row_h * 0.65 + 2
        y2 = row_h * 1 + row_h * 0.5
        y3 = row_h * 2 + row_h * 0.65
        y4 = row_h * 3 + row_h * 0.65

        # Background
        context.rect(0, 0, w, h)
        context.fill("lightyellow" if self.is_today else ("white" if self.is_month else "lightgray"))

        # Border
        with context.Stroke(0, 0, color = "black") as stroke:
            stroke.rect(0, 0, w-1, h-1)

        # Row 1: Day (right aligned)
        day_text = str(self.day)
        day_w = self._measure_text(context, day_text)
        day_x = max(pad, w - pad - day_w)
        with self.Fill("#000000") as text_filler:
            text_filler.write_text(day_text, day_x, y1, font)

        # Row 2: Dots (centered)
        dots = []
        if self.has_income:
            dots.append(("#2e7d32",))
        if self.has_expense:
            dots.append(("#1565c0",))

        r = min(6, row_h * 0.35)
        spacing = 2 * r
        total_w = 0 if not dots else (len(dots) * (2 * r) + (len(dots) - 1) * spacing)
        start_x = (w - total_w) / 2.0
        cx = start_x + r
        for (color,) in dots:
            context.begin_path()
            context.ellipse(cx - r, y2 - r, 2 * r, 2 * r)
            context.fill(color)
            cx += 2 * r + spacing

        # Row 3: Cash (left aligned)
        cash_text = str(self.cash)
        with self.Fill("#000000") as text_filler:
            text_filler.write_text(cash_text, pad, y3, font)

        # Row 4: Spendable (left aligned)
        spend_text = str(self.spendable)
        with self.Fill("#000000") as text_filler:
            text_filler.write_text(spend_text, pad, y4, font)



__all__ = ["DayCanvas"]

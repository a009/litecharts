"""Chart class and factory function."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import TYPE_CHECKING, overload

from .pane import Pane
from .series import (
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
)

if TYPE_CHECKING:
    from .series import BaseSeries
    from .types import (
        AreaSeriesOptions,
        BarSeriesOptions,
        BaselineSeriesOptions,
        CandlestickSeriesOptions,
        ChartOptions,
        HistogramSeriesOptions,
        LineSeriesOptions,
        OhlcInput,
        PaneOptions,
        SingleValueInput,
    )


def _in_jupyter() -> bool:
    """Check if running in a Jupyter environment."""
    try:
        from IPython import get_ipython  # type: ignore[attr-defined]

        ip = get_ipython()  # type: ignore[no-untyped-call]
        if ip is None:
            return False
        return "IPKernelApp" in ip.config
    except (ImportError, AttributeError):
        return False


class Chart:
    """Main chart class."""

    def __init__(self, options: ChartOptions | None = None) -> None:
        """Initialize the chart.

        Args:
            options: Chart options.
        """
        self._id = f"chart_{uuid.uuid4().hex[:8]}"
        self._options: ChartOptions = options.copy() if options else {}
        self._panes: list[Pane] = []
        self._default_pane: Pane | None = None

    @property
    def id(self) -> str:
        """Return the chart ID."""
        return self._id

    @property
    def options(self) -> ChartOptions:
        """Return the chart options."""
        return self._options

    @property
    def panes(self) -> list[Pane]:
        """Return all panes in the chart."""
        return self._panes

    @property
    def width(self) -> int:
        """Return the chart width."""
        result = self._options.get("width", 800)
        if isinstance(result, int):
            return result
        return 800

    @property
    def height(self) -> int:
        """Return the chart height."""
        result = self._options.get("height", 600)
        if isinstance(result, int):
            return result
        return 600

    def _get_default_pane(self) -> Pane:
        """Get or create the default pane."""
        if self._default_pane is None:
            self._default_pane = Pane()
            self._panes.append(self._default_pane)
        return self._default_pane

    def add_pane(self, options: PaneOptions | None = None) -> Pane:
        """Add a new pane to the chart.

        Args:
            options: Pane options including height_ratio.

        Returns:
            The created Pane.
        """
        pane = Pane(options)
        self._panes.append(pane)
        return pane

    @overload
    def add_series(
        self,
        series_type: type[CandlestickSeries],
        options: CandlestickSeriesOptions | None = None,
        pane_index: int | None = None,
    ) -> CandlestickSeries: ...

    @overload
    def add_series(
        self,
        series_type: type[LineSeries],
        options: LineSeriesOptions | None = None,
        pane_index: int | None = None,
    ) -> LineSeries: ...

    @overload
    def add_series(
        self,
        series_type: type[AreaSeries],
        options: AreaSeriesOptions | None = None,
        pane_index: int | None = None,
    ) -> AreaSeries: ...

    @overload
    def add_series(
        self,
        series_type: type[BarSeries],
        options: BarSeriesOptions | None = None,
        pane_index: int | None = None,
    ) -> BarSeries: ...

    @overload
    def add_series(
        self,
        series_type: type[HistogramSeries],
        options: HistogramSeriesOptions | None = None,
        pane_index: int | None = None,
    ) -> HistogramSeries: ...

    @overload
    def add_series(
        self,
        series_type: type[BaselineSeries],
        options: BaselineSeriesOptions | None = None,
        pane_index: int | None = None,
    ) -> BaselineSeries: ...

    def add_series(
        self,
        series_type: type[
            CandlestickSeries
            | LineSeries
            | AreaSeries
            | BarSeries
            | HistogramSeries
            | BaselineSeries
        ],
        options: CandlestickSeriesOptions
        | LineSeriesOptions
        | AreaSeriesOptions
        | BarSeriesOptions
        | HistogramSeriesOptions
        | BaselineSeriesOptions
        | None = None,
        pane_index: int | None = None,
    ) -> BaseSeries[SingleValueInput] | BaseSeries[OhlcInput]:
        """Add a series to a pane.

        Args:
            series_type: The series class (e.g., CandlestickSeries, LineSeries).
            options: Series options specific to the series type.
            pane_index: Index of the pane to add the series to. If None, uses
                the default pane (creating it if necessary).

        Returns:
            The created series instance.

        Raises:
            IndexError: If pane_index is out of range.
        """
        if pane_index is not None:
            if pane_index < 0 or pane_index >= len(self._panes):
                raise IndexError(f"Pane index {pane_index} out of range")
            pane = self._panes[pane_index]
        else:
            pane = self._get_default_pane()

        return pane.add_series(series_type, options)  # type: ignore[arg-type]

    def to_html(self) -> str:
        """Generate self-contained HTML for the chart.

        Returns:
            HTML string.
        """
        from .render import render_chart

        return render_chart(self)

    def show(self) -> None:
        """Display the chart.

        Auto-detects environment: uses Jupyter inline display if in a notebook,
        otherwise opens in a browser.
        """
        if _in_jupyter():
            self.show_notebook()
        else:
            self.show_browser()

    def show_notebook(self) -> None:
        """Display the chart inline in a Jupyter notebook."""
        from IPython.display import HTML, display

        display(HTML(self.to_html()))  # type: ignore[no-untyped-call]

    def show_browser(self) -> None:
        """Open the chart in the default web browser."""
        import tempfile
        import webbrowser

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False, encoding="utf-8"
        ) as f:
            f.write(self.to_html())
            temp_path = f.name

        webbrowser.open(f"file://{temp_path}")

    def save(self, path: str | Path) -> None:
        """Save the chart to an HTML file.

        Args:
            path: File path to save to.
        """
        path = Path(path)
        path.write_text(self.to_html(), encoding="utf-8")


def create_chart(options: ChartOptions | None = None) -> Chart:
    """Create a new chart.

    Args:
        options: Chart options.

    Returns:
        A new Chart instance.
    """
    return Chart(options)

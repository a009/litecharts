"""Tests for pane.py module."""

from __future__ import annotations

from litecharts.pane import Pane
from litecharts.series import (
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
)


class TestPane:
    """Tests for Pane class."""

    def test_id_generated(self) -> None:
        """Pane ID is generated."""
        pane = Pane()
        assert pane.id.startswith("pane_")

    def test_default_options(self) -> None:
        """Default options is empty dict."""
        pane = Pane()
        assert pane.options == {}

    def test_custom_options(self) -> None:
        """Custom options are stored."""
        pane = Pane({"height_ratio": 2.0})
        assert pane.options["height_ratio"] == 2.0

    def test_default_height_ratio(self) -> None:
        """Default height ratio is 1.0."""
        pane = Pane()
        assert pane.height_ratio == 1.0

    def test_custom_height_ratio(self) -> None:
        """Custom height ratio is returned."""
        pane = Pane({"height_ratio": 0.5})
        assert pane.height_ratio == 0.5

    def test_series_initially_empty(self) -> None:
        """Series list is initially empty."""
        pane = Pane()
        assert pane.series == []


class TestPaneAddSeries:
    """Tests for Pane add_series method."""

    def test_add_candlestick_series(self) -> None:
        """add_series creates and adds CandlestickSeries."""
        pane = Pane()
        series = pane.add_series(CandlestickSeries)
        assert isinstance(series, CandlestickSeries)
        assert len(pane.series) == 1
        assert pane.series[0] is series

    def test_add_candlestick_series_with_options(self) -> None:
        """add_series passes options to CandlestickSeries."""
        pane = Pane()
        series = pane.add_series(CandlestickSeries, {"up_color": "#00ff00"})
        assert series.options.get("up_color") == "#00ff00"

    def test_add_line_series(self) -> None:
        """add_series creates and adds LineSeries."""
        pane = Pane()
        series = pane.add_series(LineSeries)
        assert isinstance(series, LineSeries)
        assert len(pane.series) == 1

    def test_add_area_series(self) -> None:
        """add_series creates and adds AreaSeries."""
        pane = Pane()
        series = pane.add_series(AreaSeries)
        assert isinstance(series, AreaSeries)
        assert len(pane.series) == 1

    def test_add_bar_series(self) -> None:
        """add_series creates and adds BarSeries."""
        pane = Pane()
        series = pane.add_series(BarSeries)
        assert isinstance(series, BarSeries)
        assert len(pane.series) == 1

    def test_add_histogram_series(self) -> None:
        """add_series creates and adds HistogramSeries."""
        pane = Pane()
        series = pane.add_series(HistogramSeries)
        assert isinstance(series, HistogramSeries)
        assert len(pane.series) == 1

    def test_add_baseline_series(self) -> None:
        """add_series creates and adds BaselineSeries."""
        pane = Pane()
        series = pane.add_series(BaselineSeries)
        assert isinstance(series, BaselineSeries)
        assert len(pane.series) == 1

    def test_add_multiple_series(self) -> None:
        """Multiple series can be added to a pane."""
        pane = Pane()
        pane.add_series(CandlestickSeries)
        pane.add_series(LineSeries)
        pane.add_series(HistogramSeries)
        assert len(pane.series) == 3

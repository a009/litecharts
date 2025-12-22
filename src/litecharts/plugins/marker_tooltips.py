"""Marker tooltips plugin for litecharts.

This plugin adds hover tooltips to markers. When a marker has an 'id' and 'tooltip'
field, hovering over it displays custom metadata.

This is a custom enhancement - LWC doesn't have built-in marker tooltips.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..pane import Pane


def extract_marker_tooltips(pane: Pane) -> dict[str, dict[str, object]]:
    """Extract tooltip data from markers that have 'id' and 'tooltip' fields.

    Args:
        pane: The pane to extract tooltips from.

    Returns:
        Dict mapping marker IDs to tooltip data.
    """
    tooltips: dict[str, dict[str, object]] = {}
    for series in pane.series:
        for marker in series.markers:
            marker_id = marker.get("id")
            tooltip = marker.get("tooltip")
            if marker_id and tooltip:
                tooltips[marker_id] = dict(tooltip)
    return tooltips


def render_tooltip_js(
    chart_var: str, container_id: str, tooltips: dict[str, dict[str, object]]
) -> str:
    """Generate JS code for tooltip DOM and crosshairMove subscription.

    Args:
        chart_var: The JS variable name of the chart.
        container_id: The HTML container ID for the pane.
        tooltips: Dict mapping marker IDs to tooltip data.

    Returns:
        JavaScript code string.
    """
    tooltip_var = f"tooltip_{chart_var}"
    tooltips_data_var = f"markerTooltips_{chart_var}"

    tooltips_json = json.dumps(tooltips)

    return f"""// Marker tooltips
    const {tooltips_data_var} = {tooltips_json};
    const {tooltip_var} = document.createElement('div');
    {tooltip_var}.style.cssText = 'position:absolute;display:none;padding:8px 12px;' +
        'background:rgba(0,0,0,0.85);color:white;border-radius:4px;' +
        'font-size:12px;pointer-events:none;z-index:1000;max-width:250px;';
    document.getElementById('{container_id}').style.position = 'relative';
    document.getElementById('{container_id}').appendChild({tooltip_var});
    {chart_var}.subscribeCrosshairMove(function(param) {{
        if (param.hoveredObjectId && {tooltips_data_var}[param.hoveredObjectId]) {{
            const data = {tooltips_data_var}[param.hoveredObjectId];
            let html = data.title ? '<strong>' + data.title + '</strong><br>' : '';
            if (data.fields) {{
                for (const [key, val] of Object.entries(data.fields)) {{
                    html += '<span style="color:#aaa">' + key + ':</span> ';
                    html += val + '<br>';
                }}
            }}
            {tooltip_var}.innerHTML = html;
            {tooltip_var}.style.display = 'block';
            if (param.point) {{
                {tooltip_var}.style.left = (param.point.x + 15) + 'px';
                {tooltip_var}.style.top = (param.point.y - 15) + 'px';
            }}
        }} else {{
            {tooltip_var}.style.display = 'none';
        }}
    }});"""

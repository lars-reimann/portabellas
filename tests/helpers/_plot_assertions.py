from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from portabellas.plotting import Plot


def assert_plot_has_traces(
    plot: Plot,
    *,
    expected_trace_count: int,
    expected_trace_types: list[str] | None = None,
) -> None:
    fig_dict = plot._figure.to_dict()
    data = fig_dict.get("data", [])
    assert len(data) == expected_trace_count, f"Expected {expected_trace_count} traces, but got {len(data)}."
    if expected_trace_types is not None:
        actual_types = [trace.get("type", "unknown") for trace in data]
        assert actual_types == expected_trace_types, (
            f"Expected trace types {expected_trace_types}, but got {actual_types}."
        )


def assert_plot_has_title(plot: Plot, expected_title: str) -> None:
    fig_dict = plot._figure.to_dict()
    layout = fig_dict.get("layout", {})
    actual_title = layout.get("title", {}).get("text", None)
    assert actual_title == expected_title, f"Expected title '{expected_title}', but got '{actual_title}'."


def assert_plot_has_no_title(plot: Plot) -> None:
    fig_dict = plot._figure.to_dict()
    layout = fig_dict.get("layout", {})
    title = layout.get("title", {})
    text = title.get("text", None) if isinstance(title, dict) else title
    assert text is None, f"Expected no title, but got '{text}'."


def assert_plot_has_theme(plot: Plot, expected_template: str) -> None:
    fig_dict = plot._figure.to_dict()
    layout = fig_dict.get("layout", {})
    template = layout.get("template", {})
    actual_template = template.get("data", {}).get("layout_attributes", {}).get("name", None)
    assert actual_template == expected_template, (
        f"Expected template '{expected_template}', but got '{actual_template}'."
    )

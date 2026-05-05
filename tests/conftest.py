import importlib.util

import pytest


def _kaleido_is_available() -> bool:
    if importlib.util.find_spec("kaleido") is None:
        return False
    try:
        import kaleido  # type: ignore[import-untyped]  # noqa: PLC0415

        kaleido.Kaleido()
    except (ImportError, RuntimeError):
        return False
    return True


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "requires_kaleido: requires kaleido with Chrome")


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    if _kaleido_is_available():
        return
    skip = pytest.mark.skip(reason="requires kaleido with Chrome")
    for item in items:
        if "requires_kaleido" in item.keywords:
            item.add_marker(skip)

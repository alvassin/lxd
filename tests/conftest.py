from pathlib import Path

import pytest


@pytest.fixture
def assets_path() -> Path:
    path = Path(__file__).parent / 'assets'
    return path.resolve()

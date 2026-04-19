from ._collections import compute_duplicates
from ._lazy import safely_collect_lazy_frame, safely_collect_lazy_frame_schema
from ._string import get_similar_strings

__all__ = [
    "compute_duplicates",
    "get_similar_strings",
    "safely_collect_lazy_frame",
    "safely_collect_lazy_frame_schema",
]

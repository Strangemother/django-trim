from pathlib import Path


def without_leaf(full_path, partial_path):
    """
    base = Path('/django-trim/django-trim/doc_site/extern/templates/')
    partial = 'extern/generic_indices.md'
    full = base / partial

    res = without_leaf(full, partial)
    assert res == base
    """
    rev_root = tuple(reversed(Path(full_path).parts))

    for i, part in enumerate(reversed(Path(partial_path).parts)):
        if part == rev_root[i]:
            continue

    return Path(*tuple(reversed(rev_root[i+1:])))

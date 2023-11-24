"""Common util/helper functions for Jenkins"""


def validate_max_retry(max_retry: int):
    """Validates max retry parameter"""
    if max_retry < 1 or max_retry > 100_000:
        raise ValueError('Max retry value invalid')

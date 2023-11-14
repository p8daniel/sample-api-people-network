import re
from re import Pattern
from typing import AnyStr, Dict, List, Union


def order_json(obj: Union[Dict, List, str]) -> Union[str, List, Dict]:
    """Order list present in a json so that assertion comparison don't fail due to order."""
    if isinstance(obj, dict):
        return dict(sorted((k, order_json(v)) for k, v in obj.items()))
    if isinstance(obj, list):
        return sorted([order_json(x) for x in obj], key=lambda x: str(order_json(x)))
    return obj


class MatchRegex:
    """Assert that a given string match with a regex"""

    def __init__(self, pattern: Pattern, flags: int = 0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual: str) -> bool:  # type: ignore
        return bool(self._regex.match(actual))

    def __repr__(self) -> AnyStr:
        pattern: AnyStr = self._regex.pattern
        return pattern


UUID_REGEX = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"

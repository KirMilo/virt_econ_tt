import hashlib
from typing import Callable, Any, Optional, Tuple, Dict

from starlette.requests import Request
from starlette.responses import Response


def custom_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *,
    request: Optional[Request] = None,  # noqa
    response: Optional[Response] = None,  # noqa
    args: Tuple[Any, ...],  # noqa
    kwargs: Dict[str, Any],  # noqa
) -> str:
    return ":".join([
        namespace,
        request.method.lower(),
        request.url.path
    ])

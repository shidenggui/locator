# coding:utf-8
import requests
from typing import List, Tuple, Optional

from locator.locator import Locator

__all__ = ("find", "find_first")


def find(
    *, html: str = None, url: str = None, target: str, fuzzy: bool = True
) -> List[Tuple[str, Optional[int]]]:
    """
    Finding shortest css selector path for target in given html

    :param html:
        html content.
    :param url:
        url to provide html content, if url is provided, html options will be ignored.
    :param target:
        target text to search in html
    :param fuzzy:
        should match target text exactly
    :return:
        css selector, if css selector cant pinpoint the target,
        use index to spot exactly
    """
    if not html and not url:
        raise ValueError("must apply options for html or url")
    if url:
        response = requests.get(url=url)
        html = response.text

    return Locator(html).find(target, fuzzy=fuzzy)


def find_first(
    *, html: str = None, url: str = None, target: str, fuzzy: bool = True
) -> Optional[Tuple[str, Optional[int]]]:
    """
    like find, but just return first path or None
    """
    if not html and not url:
        raise ValueError("must apply options for html or url")
    if url:
        response = requests.get(url=url)
        html = response.text

    return Locator(html).find_first(target, fuzzy=fuzzy)

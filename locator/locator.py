# coding: utf8
import operator
from itertools import combinations
from typing import Optional, List, Tuple

import lxml.html
from lxml.etree import Element


class Node:
    """Representing a path fragment for select target element"""

    def __init__(
        self, type_: str, text: str, position: int = 0, show_position: bool = False
    ):
        self.type_ = type_
        self.text = text
        self.position = position
        self.show_position = show_position

    def __hash__(self):
        return id(self)


class ClassNode(Node):
    """Representing a html class like <div class="test"></div>"""

    def __repr__(self):
        return f".{self.text}"


class IdNode(Node):
    """Representing a html id like <div id="id"></div>"""

    def __repr__(self):
        return f"#{self.text}"


class TagNode(Node):
    """Representing a html tag like <div></div>"""

    def __repr__(self):
        if self.show_position and self.position > 0:
            return f"{self.text}:nth-child({self.position})"
        else:
            return f"{self.text}"


class Locator:
    """Finding shortest match css select path for text in given html"""

    def __init__(self, html: str):
        self._ast: Element = lxml.html.fromstring(html)

    def find(self, text: str, *, fuzzy: bool = True) -> List[Tuple[str, Optional[int]]]:
        targets = self._find_targets(text, fuzzy)
        for target in targets:
            selector, index = self._build_path(target)
            yield selector.lstrip("html body "), index

    def find_first(
        self, text: str, *, fuzzy: bool = True
    ) -> Optional[Tuple[str, Optional[int]]]:
        try:
            return next(self.find(text, fuzzy=fuzzy))
        except StopIteration:
            return None

    def _find_targets(self, text: str, fuzzy: bool) -> List[Element]:
        match = operator.contains if fuzzy else operator.eq
        elements = []
        for child in self._ast.iter():
            if child.text and match(child.text, text):
                elements.append(child)
        return elements

    def _build_path(self, target: Element) -> Tuple[str, Optional[int]]:
        path = self._build_basic_path(target)
        return self._minimize_path(path, target)

    def _build_basic_path(self, target: Element) -> List[Node]:
        path = []
        self._construct_path(target, path)
        path.reverse()
        return path

    def _minimize_path(self, path: List[Element], target: Element):
        selector = self._build_selector(path)
        if self._is_unique(selector):
            return selector, None

        tags: List[TagNode] = list(filter(lambda x: isinstance(x, TagNode), path))
        for i in range(1, len(tags) + 1):
            for tag_nodes in combinations(tags, i):
                for tag_node in tag_nodes:
                    tag_node.show_position = True
                selector = self._build_selector(path)
                if self._is_unique(selector):
                    return selector, None

                for tag_node in tag_nodes:
                    tag_node.show_position = False
        # if can't find unique targets by path, try match by position
        selector = self._build_selector(path)
        for i, ele in enumerate(self._ast.cssselect(selector)):
            if ele == target:
                return selector, i
        assert True, "Bug appears, shouldn't reach there"

    @staticmethod
    def _build_selector(elements) -> str:
        build_query = " ".join([str(e) for e in elements])
        return build_query

    def _is_unique(self, query: str) -> bool:
        return len(self._ast.cssselect(query)) == 1

    def find_first(self, *args, **kwargs) -> Optional[Tuple[str, int]]:
        try:
            return next(self.find(*args, **kwargs))
        except StopIteration:
            return None

    def _construct_path(self, ele: Element, path: list):
        if ele is None:
            return

        if "id" in ele.attrib:
            path.append(IdNode("id", ele.attrib["id"]))
            return

        reserved = []
        if "class" in ele.attrib:
            for class_name in ele.attrib["class"].split():
                if self._is_unique_class(self._ast, class_name):
                    path.append(ClassNode("class", class_name))
                    return

                reserved.append((ele, class_name))

        if reserved:
            jump = []
            for ele, class_name in reserved:
                distance, parent = self._find_longest_jump(ele, class_name)
                jump.append((distance, parent, ele, class_name))

            max_jump = max(jump)
            if max_jump[0] >= 0:
                path.append(ClassNode("class", max_jump[3]))
                self._construct_path(max_jump[1], path)
                return

        path.append(TagNode("tag", ele.tag, self._get_position(ele)))
        self._construct_path(ele.getparent(), path)

    @staticmethod
    def _is_unique_class(tree: Element, class_name: str):
        if len(tree.cssselect(f".{class_name}")) == 1:
            return True
        return False

    @staticmethod
    def _get_position(ele: Element) -> int:
        """0 represent unique"""
        before = len(list(ele.itersiblings(tag=ele.tag, preceding=True)))
        after = len(list(ele.itersiblings(tag=ele.tag, preceding=False)))
        if before + after == 0:
            return 0
        return before + 1

    def _find_longest_jump(self, node, class_name: str) -> Tuple[int, Element]:
        prev = node
        distance = -1

        while node is not None:
            if not self._is_unique_class(node, class_name):
                break
            distance += 1
            prev = node
            node = node.getparent()
        return distance, prev.getparent() if distance == 0 else prev

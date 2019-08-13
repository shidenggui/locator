from locator import __version__
import unittest

from locator.locator import Locator


def test_version():
    assert __version__ == "0.1.0"


class Test(unittest.TestCase):
    def test_id(self):
        finder = Locator(html=html)
        path = list(finder.find("test1"))
        self.assertListEqual([("#test_id", None)], path)

    def test_class(self):
        finder = Locator(html=html)
        path = list(finder.find("test2"))
        self.assertListEqual([(".class1 .test_class p", None)], path)

    def test_multi_tags(self):
        finder = Locator(html=html)
        path = list(finder.find("test3"))
        self.assertListEqual([(".class2 div:nth-child(2) .class3 p", None)], path)

    def test_conflict_path(self):
        finder = Locator(html=html)
        path = list(finder.find("test4"))
        self.assertListEqual(
            [(".class3 div div .test_class p:nth-child(1)", None)], path
        )

    def test_path_with_index(self):
        finder = Locator(html=html)
        path = list(finder.find("test_info"))
        self.assertListEqual([(".intro .info", 1)], path)


html = """
<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>
</head>
<body>

<h1>This is a Heading</h1>
<div>
    <p id="test_id">test1</p >
</div>
<div class="class1">
    <div class="test_class">
        <p>test2</p >
    </div>

    <div class="test_class test_class2"></div>
</div>
<div class="class2">
    <div>
        <div class="class3">
            <p>test8</p >
        </div>
    </div>
    <div>
        <div class="class3">
            <p>test3</p >
        </div>
    </div>

</div>
<div class="class3">
    <div>
        <div class="test_class3">
            <p>test5</p >
        </div>
    </div>
    <div class="test_class">
        <div class="test_class2">
            <div class="test_class test_class2">
                <p>test4</p >
                <p>test6</p >
            </div>
        </div>
    </div>
</div>
<div class="intro">
    <p class="info">test_</p >
    <p class="info">test_info</p >
</div>

</body>
</html>
"""

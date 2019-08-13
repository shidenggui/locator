# locator

CSS Selector Generator For Python

## Install

pip install locator

## Usage

### Find

```Python
>>> import locator
>>> locator.find(html='test content', target='target_text')
>>> [('.class1 p', None), ('.class2 p', None)]

>>> locator.find_first(html='test content2', target='target_text2')
>>> ('.class1 p', None)
```

### Match target exactly

```Python
>>> import locator
>>> locator.find(html='test content', target='target_text', fuzzy=False)
>>> [('.class1 p', None), ('.class2 p', None)]
```

### Find target from url

```Python
>>> import locator
>>> locator.find_first(url='http://test.com', target='target_text')
>>> ('.class1 p', None)
```

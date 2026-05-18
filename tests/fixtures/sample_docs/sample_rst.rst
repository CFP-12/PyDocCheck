Python RST Example
==================

This is a reStructuredText file.

Simple Example
--------------

.. code-block:: python

    print("Hello from RST!")
    x = 42
    print(x)

List Comprehension
------------------

.. code-block:: python

    squares = [x**2 for x in range(10)]
    print(squares)

Dictionary Operations
---------------------

.. code-block:: python

    person = {"name": "John", "age": 28}
    for key, value in person.items():
        print(f"{key}: {value}")

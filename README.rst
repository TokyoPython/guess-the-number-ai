.. role:: bash(code)
    :language: bash

.. role:: python(code)
    :language: python


===================
Guess the number AI
===================

(disclaimer: it's not AI in the sense of machine/deep learning etc.)

Welcome!

.. contents::
    :backlinks: none


Problem
=======

I give you a number range, for example 1 to 100.

I also pick a number within that range (including the borders), for example 24.
But, I keep that number a secret.

You can try to guess the number, and every time you guess, I will simply say:

*   "higher" when my secret number is larger than your guess,
*   "lower" when my number is smaller than the guess,
*   or "hit" when you guessed it.

Task 1
------

Your task is to guess the number I've picked in the most efficient way possible.
Therefore, you're supposed to design and implement a strategy for finding this number.

For solving the problem, we'll use Python and Jupyter Notebook.

First of all, there is an enumeration ``Hint`` which has 3 values:

.. code:: python

    class Hint(enum.Enum):

        Lower = '-'
        Hit = '!'
        Higher = '+'

Secondly, there is a class ``GuessingGameAi`` which has 3 important methods:

.. code:: python

    class MyAi(GuessingGameAi):

        def __init__(self, game: GuessingGame):
            self.game = game

        def generate_guess(self) -> int:
            ...

        def receive_hint(self, hint: Hint):
            ...

The ``__init__`` method runs only once, and it receives the number range
in a variable ``game.number_range``.

The ``generate_guess`` method runs first, after which ``receive_hint`` runs in which
you can examine if you should go lower or higher next time.

I've prepared a template of solution in which the only places where you'd write
your code are 3 spots where currently we have ``pass`` statements.


.. code:: python

    class MyAi(GuessingGameAi):

        """Implement your solution here."""

        def __init__(self, game):
            """Initialize new instance of MyAi."""
            super().__init__(game)
            # add extra variables below
            pass

        def generate_guess(self) -> int:
            """Generate a number within the range allowed by the game.

            You may use and/or modify variables defined in __init__(), for example self.game.

            Make sure to return an integer number within range defined in the game.
            """
            # write your code below...
            pass

        def receive_hint(self, hint: Hint):
            """Analyse the hint given by the game.

            You may use and/or modify variables defined in __init__(), for example self.game.

            To check what the hint actually is, use the fact that hint is of type Hint. For example,
            you can use "if hint is Hint.Higher: ..." etc.
            """
            # write your code below...
            pass

Really, no need to modify any other part of the code, just the parts marked:

.. code:: python

    # add extra variables below
    pass

.. code:: python

    # write your code below...
    pass

Some examples of (non-optimal) solutions are available in `<guess_the_number_ai_examples.ipynb>`_.
Feel free to study them before writing your own.

Open `<guess_the_number_ai_task.ipynb>`_ in Jupyter Notebook and solve the task there.
That notebook includes a testing routines, so you can see how well your strategy performs against
the non-optimal examples, as well as how it performs against the reference solution.


Reference solution
------------------

A good solution is implemented in `<guess_the_number_ai_solution.ipynb>`_. Please avoid looking
there until you're satisfied with your own solution.


Task 2
------

Solve Task 1 in exactly 1 line of code. Can you do it? It's possible, if you use a certain trick.


Technical side
==============


Requirements
------------

Python 3.5+

Python libraries as specified in `<requirements.txt>`_. You can install them via:

.. code:: bash

    pip3 install -r requirements.txt


Running jupyter notebook
------------------------

.. code:: bash

    python3 -m jupyter notebook

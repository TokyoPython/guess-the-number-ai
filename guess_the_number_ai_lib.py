"""Guessing game AI library.

by Mateusz Bysiek
"""

import collections
import enum
import functools
import math
import operator
import random
import typing

import numpy as np
import pylab


class Hint(enum.Enum):

    """Enumeration of possible hints that GuessingGame can give to GuessingGameAi.

    This class is predefined - do not change it.
    """

    Lower = '-'
    Hit = '!'
    Higher = '+'


class GuessingGame:

    """Guessing game.

    This class is predefined - do not change it.
    """

    def __init__(self, range_min: int, range_max: int, testing: bool = False):
        """Initialize a new guessing game."""
        assert isinstance(range_min, int), 'lower bound of the number range must be an integer'
        assert isinstance(range_max, int), 'upper bound of the number range must be an integer'
        assert range_min < range_max, 'lower bound must be lower than upper bound'
        assert isinstance(testing, bool)

        self._range_min = range_min
        self._range_max = range_max
        self._number = random.randrange(range_min, range_max)
        self._state = None  # type: Hint
        self._testing = testing

    def number_range(self) -> typing.Tuple[int, int]:
        """Return tuple (min, max) that describes range of the number to guess."""
        return (self._range_min, self._range_max)

    def state(self) -> Hint:
        """Return current state of the game, i.e. last given hint."""
        return self._state

    def is_over(self) -> bool:
        """Return True if game is over, False otherwise."""
        return self._state is Hint.Hit

    def change_number(self) -> None:
        """Do nothing... yet."""
        pass

    def guess(self, number: int) -> Hint:
        """Compare given number to internally stored one, and return a hint about its value."""
        if not self._testing:
            print('{}?'.format(number))

        if self._state is Hint.Hit:
            raise RuntimeError('you shoud not keep guessing after you guessed correctly')

        assert isinstance(number, int), 'your guess must be an integer'
        assert number in range(self._range_min, self._range_max), (
            'your guess {} is outside the valid range <{},{})'
            .format(number, self._range_min, self._range_max))

        if self._number == number:
            self._state = Hint.Hit
        elif self._number > number:
            self._state = Hint.Higher
        elif self._number < number:
            self._state = Hint.Lower

        if not self._testing:
            print(self._state)

        return self._state


class GuessingGameAi:

    """AI for the guessing game.

    This class is predefined - do not change it.
    """

    def __init__(self, game: GuessingGame):
        assert isinstance(game, GuessingGame)

        self.game = game

    def generate_guess(self) -> int:
        """Generate a number within the range allowed by the game."""
        pass

    def receive_hint(self, hint: Hint):
        """Analyse the hint given by the game."""
        pass

    def generate_guesses_until_hit(self, max_guesses: int = None) -> typing.Optional[int]:
        """Try to guess unil win, or until maximum number of guesses is performed.

        Return number of guesses performed to win, or None if the number was not guessed
        correctly within maximum number of guesses.

        Default limit of guesses is 10000.
        """
        if max_guesses is None:
            max_guesses = 10000

        assert isinstance(max_guesses, int)
        assert max_guesses > 0

        for guess_no in range(max_guesses):
            guess = self.generate_guess()
            hint = self.game.guess(guess)
            if self.game.is_over():
                return guess_no + 1
            self.receive_hint(hint)
        return None


class StupidAi(GuessingGameAi):

    """StupidAi is a kind of GuessingGameAi.

    Each time it makes guesses randomly without remembering previous guesses.

    It also ignores the hints.
    """

    def __init__(self, game):
        super().__init__(game)

    def generate_guess(self) -> int:
        guess = random.randrange(*self.game.number_range())
        return guess

    def receive_hint(self, hint: Hint):
        pass


class SequencingAi(GuessingGameAi):

    """SequencingAi is also a kind of GuessingGameAi.

    It tries guessing the number from minimum in increasing order.

    It also ignores the hints.
    """

    def __init__(self, game):
        super().__init__(game)
        self.curr_number, _ = game.number_range()

    def generate_guess(self) -> int:
        guess = self.curr_number
        self.curr_number += 1
        return guess

    def receive_hint(self, hint: Hint):
        pass


class SignedSequencingAi(GuessingGameAi):

    """SignedSequencingAi is a kind of GuessingGameAi as well.

    It tries guessing the number from the middle and goes up or down depending on the hint.
    """

    def __init__(self, game):
        super().__init__(game)
        self.curr_number = sum(game.number_range()) // 2
        self.sign = None

    def generate_guess(self) -> int:
        if self.sign == '+':
            self.curr_number += 1
        elif self.sign == '-':
            self.curr_number -= 1
        return self.curr_number

    def receive_hint(self, hint: Hint):
        if hint is Hint.Higher:
            self.sign = '+'
        if hint is Hint.Lower:
            self.sign = '-'


class OptimalAi(GuessingGameAi):

    """This is optimal solution, don't study it unless you already tried on your own."""

    def __init__(self, game):
        """Initialize new instance of OptimalAi."""
        super().__init__(game)
        # add extra variables below
        self.lower, self.upper = game.number_range()
        self.number = None

    def generate_guess(self) -> int:
        """Generate a number within the range allowed by the game.

        You may use and/or modify variables defined in __init__(), for example self.game.

        Make sure to return an integer number within range defined in the game.
        """
        # write your code below...
        self.number = ((self.lower + self.upper) // 2)
        return self.number

    def receive_hint(self, hint: Hint):
        """Analyse the hint given by the game.

        You may use and/or modify variables defined in __init__(), for example self.game.

        To check what the hint actually is, use the fact that hint is of type Hint. For example,
        you can use "if hint is Hint.Higher: ..." etc.
        """
        # write your code below...
        self.lower, self.upper = (self.number + 1, self.upper) if hint is Hint.Higher \
            else (self.lower, self.number - 1)


class GuessingGameAiTester:

    """Tester for guessing game AI systems."""

    trials = 500

    ranges = [
        (3, 5), (10, 16), (0, 10), (-10, 5), (100, 120), (-25, 0), (1000, 1030), (0, 40),
        (-100, -50)]

    colors = ['blue', 'gold', 'black', 'violet']

    def __init__(self, ai_classes: typing.List[type]):  # pylint: disable=invalid-sequence-index
        assert all([issubclass(ai_class, GuessingGameAi) for ai_class in ai_classes])

        self._ai_classes = ai_classes
        self.all_results_mappings = None

    def _run_test(self, ai_class, range_min, range_max):
        results = []  # type: typing.Optional[typing.List[int]]
        for _ in range(self.trials):
            game = GuessingGame(range_min, range_max, testing=True)
            guessing_ai = ai_class(game)
            result = guessing_ai.generate_guesses_until_hit()
            if result is None:
                return None
            results.append(result)
        return results

    def _run_tests(self, ai_class):
        results_mapping = {}  # type: typing.Mapping[int, typing.Optional[typing.List[int]]]
        for range_min, range_max in self.ranges:
            results_mapping[range_max - range_min] = self._run_test(ai_class, range_min, range_max)
        return results_mapping

    def run_tests(self):
        """Run extensive tests for AI classes."""
        self.all_results_mappings = collections.OrderedDict()
        for ai_class in self._ai_classes:
            results_mapping = self._run_tests(ai_class)
            self.all_results_mappings[ai_class] = results_mapping

    def _plot_results(self, ai_class, results_mapping, color):
        assert ai_class in self._ai_classes
        assert color in self.colors

        sorted_mapping = sorted(results_mapping.items())
        x_values, y_values = zip(*sorted_mapping)

        line_style = {
            'color': color
            }
        plot_properties = {
            'boxprops': {**line_style},
            'whiskerprops': {**line_style},
            'capprops': {**line_style},
            'flierprops': {**line_style, 'marker': '+'},
            'medianprops': {**line_style},
            'meanprops': {**line_style}
            }
        pylab.boxplot(y_values, positions=x_values, **plot_properties)

        averages = [
            functools.reduce(operator.add, [n / len(results) for n in results])
            for results in y_values]
        line_style = {
            'linewidth': 0,
            'marker': 'o',
            'color': color
            }
        label = 'average guesses of {}'.format(ai_class.__name__)
        pylab.plot(x_values, averages, label=label, **line_style)

    def _format_plot(self):
        x_values = sorted([b - a for a, b in self.ranges])

        line_style = {
            'linewidth': 2,
            'color': 'green'
            }
        pylab.plot(
            np.arange(1, max(x_values), 0.1),
            [math.log2(n) for n in np.arange(1.0, max(x_values), 0.1)],
            label='log2 of guessing range', **line_style)

        line_style = {
            'linewidth': 2,
            'color': 'red'
            }
        pylab.plot(
            range(max(x_values) + 1), range(max(x_values) + 1),
            label='linear with guessing range', **line_style)

        pylab.legend(loc='upper left', framealpha=0.8)
        pylab.title(
            'Testing guessing quality of: {}'
            .format(', '.join([ai_class.__name__ for ai_class in self._ai_classes])))
        pylab.xlim(xmin=0.0, xmax=1.0 + max(x_values))
        pylab.xlabel('range size')
        pylab.ylim(ymin=0.0, ymax=5.0 + max(x_values))
        pylab.ylabel('number of guesses until success')

    def plot_results(self):
        """Plot results about AIs accuracy."""
        for ai_class, color in zip(self._ai_classes, self.colors):
            self._plot_results(ai_class, self.all_results_mappings[ai_class], color)
        self._format_plot()

    def run_tests_and_plot_results(self):
        """Run extensive tests for AIs and plot results about their accuracy."""
        self.run_tests()
        self.plot_results()

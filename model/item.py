import random
from typing import Dict, List
from enum import Enum


class ReviewLevel(Enum):
    """
    Review levels
    """
    A1 = 2
    A2 = 8
    A3 = 24
    A4 = 48
    G1 = 24*7
    G2 = 24*14
    M1 = 24*30
    E1 = 24*120


class ReviewItem(object):
    """
    Review items
    """

    def __init__(self):
        self._level_stat: Dict[ReviewLevel, int] = dict()
        self._level_stat[ReviewLevel.A1] = 1
        self._current_level_index: int = 0
        self._burned: bool = False

    @property
    def burned(self):
        return self._burned

    @property
    def level_idx(self):
        return self._current_level_index

    def get_stat(self, level: ReviewLevel) -> int:
        return self._level_stat[level]

    def advance(self) -> bool:
        """
        Advance the item in the review
        :return: false if advanced, true if the item is burned
        """
        self._current_level_index += 1
        if self._current_level_index == len(ReviewLevel):
            self._burned = True
        else:
            level = list(ReviewLevel)[self._current_level_index]
            if level not in self._level_stat:
                self._level_stat[level] = 1
            else:
                self._level_stat[level] += 1
        return self._burned

    def fail(self):
        """
        The item review failed
        :return:
        """
        if self._current_level_index > 1:
            self._current_level_index -= 2
        else:
            self._current_level_index = 0
        self._level_stat[list(ReviewLevel)[self._current_level_index]] += 1


class ReviewEngine(object):
    """
    This class takes an Item and make it work until it burns
    """

    def __init__(self, prob_array: List):
        self._prob_array = prob_array

    def process(self, item: ReviewItem) -> ReviewItem:
        """
        Process the item until it burns
        :param item: the item to process
        :return: the item once burned
        """
        while not item.burned:
            probability = self._prob_array[item.level_idx]
            advance = probability > random.random()
            if advance:
                item.advance()
            else:
                item.fail()
        return item


class ReviewStats(object):
    """
    Class handling statistics
    """

    _a_levels = [ReviewLevel.A1, ReviewLevel.A2, ReviewLevel.A3, ReviewLevel.A4]
    _g_levels = [ReviewLevel.G1, ReviewLevel.G2]
    _m_levels = [ReviewLevel.M1]
    _e_levels = [ReviewLevel.E1]

    def __init__(self, items: List[ReviewItem]):
        self._items = items
        self._mean_a = None
        self._mean_g = None
        self._mean_m = None
        self._mean_e = None

    @property
    def mean_a(self) -> float:
        if self._mean_a is None:
            a_total_time = 0
            for item in self._items:
                a_total_time += item.get_stat(ReviewLevel.A1) * ReviewLevel.A1.value
                a_total_time += item.get_stat(ReviewLevel.A2) * ReviewLevel.A2.value
                a_total_time += item.get_stat(ReviewLevel.A3) * ReviewLevel.A3.value
                a_total_time += item.get_stat(ReviewLevel.A4) * ReviewLevel.A4.value
            self._mean_a = a_total_time / 24 / len(self._items)
        return self._mean_a

    @property
    def mean_g(self) -> float:
        if self._mean_g is None:
            g_total_time = 0
            for item in self._items:
                g_total_time += item.get_stat(ReviewLevel.G1) * ReviewLevel.G1.value
                g_total_time += item.get_stat(ReviewLevel.G2) * ReviewLevel.G2.value
            self._mean_g = g_total_time / 24 / len(self._items)
        return self._mean_g

    @property
    def mean_m(self) -> float:
        if self._mean_m is None:
            m_total_time = 0
            for item in self._items:
                m_total_time += item.get_stat(ReviewLevel.M1) * ReviewLevel.M1.value
            self._mean_m = m_total_time / 24 / len(self._items)
        return self._mean_m

    @property
    def mean_e(self) -> float:
        if self._mean_e is None:
            e_total_time = 0
            for item in self._items:
                e_total_time += item.get_stat(ReviewLevel.E1) * ReviewLevel.E1.value
            self._mean_e = e_total_time / 24 / len(self._items)
        return self._mean_e

    def mean(self):
        return (self.mean_a + self.mean_g + self.mean_m + self.mean_e) / 4

    @staticmethod
    def optimal(levels: List[ReviewLevel]) -> int:
        opt_a = 0
        for level in levels:
            opt_a += level.value
        return opt_a

    def corr_a(self):
        return ReviewStats.optimal(ReviewStats._a_levels) / self.mean_a / 24

    def corr_g(self):
        return ReviewStats.optimal(ReviewStats._g_levels) / self.mean_g / 24

    def corr_m(self):
        return ReviewStats.optimal(ReviewStats._m_levels) / self.mean_m / 24

    def corr_e(self):
        return ReviewStats.optimal(ReviewStats._e_levels) / self.mean_e / 24

"""
Module providing classes as data structure.
"""

from typing import List


class Record(object):
    """ 
    """
    def __init__(self, *args: List) -> None:
        self.start_time = args[0]
        self.end_time = args[1]
        self.verification = int(args[2])
        self.validity = int(args[3])
        self.value = float(args[-1])


class Observation(object):
    """ Air pollution recorded by a sample point
    ref : https://www.data.gouv.fr/fr/datasets/donnees-temps-reel-de-mesure-des-concentrations-de-polluants-atmospheriques-reglementes-1/ 
    """
    def __init__(self, polluant: str, sample_point:str) -> None:
        self.polluant = polluant
        self.sample_point = f"https://mg-services.herokuapp.com/api/open-data/pollution/air/sample-point/{sample_point}"
        self.records = []

    def add(self, record: Record):
        self.records.append(record)

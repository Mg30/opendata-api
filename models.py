from typing import List


class Record(object):
    def __init__(self, *args: List) -> None:
        self.start_time = args[0]
        self.end_time = args[1]
        self.verification = int(args[2])
        self.validity = int(args[3])
        self.value = float(args[-1])


class Observation(object):
    def __init__(self, polluant: str, sample_point:str) -> None:
        self.polluant = polluant
        self.sample_point = sample_point
        self.records = []

    def add(self, record: Record):
        self.records.append(record)

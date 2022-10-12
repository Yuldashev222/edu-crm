from enum import Enum


class StudentStatus(Enum):
    in_open_class = 'in_open_class'
    in_trial_lesson = 'in_trial_lesson'
    real = 'real'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)


class StudentDegrees(Enum):
    beginner = 'beginner'
    middle = 'middle'
    prof = 'prof'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)
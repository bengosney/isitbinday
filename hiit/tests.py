from django.test import TestCase

from model_bakery import baker

from .models import Exercise, Workout

class WorkoutTestModel(TestCase):
    def setUp(self):
        self.workout = baker.make(Workout, make_m2m=True)
        print(self.workout.exercises.count())
        
    def testWorkout(self):
        workout = baker.make(Workout)
        
        self.assertEqual(1, 2)
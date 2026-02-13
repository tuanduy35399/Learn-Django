from django.test import TestCase
from .models import TodoModel
# Create your tests here

class TestModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.todo=TodoModel.objects.create(
            title= "1st Todo",
            body="Body of Todo"
        )

    def test_model_content(self):
        self.assertEqual(self.todo.title, "1st Todo")
        self.assertEqual(self.todo.body, "Body of Todo")
        self.assertEqual(str(self.todo), "1st Todo")

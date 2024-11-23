from django.db import models

# Animal model
class Animal(models.Model):
    name = models.CharField(max_length=255)  # Name of the animal.
    picture = models.ImageField(upload_to='images/', null=True, blank=True)  # Animal's picture.

    def __str__(self):
        return self.name


# Answer model
class Answer(models.Model):
    answer = models.TextField()  # The actual answer text.
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='answers'
    )  # Answer is tied to a specific question.
    animal = models.ForeignKey(
        'Animal',
        on_delete=models.CASCADE,
        related_name='answers',  # Use a meaningful related_name for reverse querying.
        null=True,  # Allows NULL in the database.
        blank=True  # Allows form validation to accept an empty field.
    )

    def __str__(self):
        return self.answer


# Question model
class Question(models.Model):
    order_in_test = models.IntegerField()  # The order of the question in the test.
    question = models.CharField(max_length=255)  # The actual question text.

    def __str__(self):
        return self.question

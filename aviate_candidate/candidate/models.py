from django.db import models

class Candidate(models.Model):
    """
    Assuming email as unique identifer and also assuming all fields are required.
    Not connecting to User for authentication. 
    Creating candidate table with name and using it to search, for the test.
    Also keeping name as one, instead of splitting into first name, middle name and last name , to keep it simple for test.
    """
    email = models.EmailField(unique=True) 
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=2, choices=(("M", "Male"),("F", "Female"),("O", "others")))
    phone_number = models.CharField(max_length=12) #keeping it simple for the test
    created_at = models.DateTimeField(auto_now_add=True) #habit
    updated_at = models.DateTimeField(auto_now=True) #habit

    def __str__(self):
        return f"Candidate : name - {self.name} : email - {self.email} "


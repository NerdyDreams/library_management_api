from django.db import models

# Create your models here.


class Book(models.Model):
    AVAILABILITY_STATUS = (
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost'),
        ('damaged', 'Damaged'),
    )
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    publication_date = models.DateField()
    edition = models.CharField(max_length=50)
    summary = models.TextField()
    status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
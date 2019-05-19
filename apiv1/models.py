from django.db import models
from users.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class BookState(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    category = models.ManyToManyField(Category)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    book_state = models.ForeignKey(BookState, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    author = models.CharField(max_length=100)
    translator = models.CharField(max_length=100)
    publisher = models.CharField(max_length=1000)
    chap = models.CharField(max_length=30)
    date_published = models.IntegerField()
    pages = models.IntegerField()
    description = models.TextField()


class Images(models.Model):
    book = models.ForeignKey(Book, default=None, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(default=None)


class Sell(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    @property
    def is_available(self):
        r = self.request.filter(status="sold")
        if not r:
            return True
        return False


class Request(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="buy_request")
    sell = models.ForeignKey(Sell, on_delete=models.CASCADE, related_name='request')
    status = models.CharField(choices=(('sold', 'sold'), ('waiting', 'waiting'), ('declined', 'declined')),
                              max_length=20, default='waiting')



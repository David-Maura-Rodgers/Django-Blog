# pip3 install 'django<4'
# pip3 install dj-database-url psycopg2
# pip3 install dj3-cloudinary-storage
# pip3 install 'django<4' gunicorn
# pip3 install django-allauth
# pip3 install django-summernote
# pip3 install django-crispy-forms
# pip3 freeze -- local > requirements.txt

# ls ../.pip-modules/lib
# cp -r ../.pip-modules/lib/python3.8/site-packages/allauth/templates/* ./templates  # noqa

# python3 manage.py makemigrations --dry-run
# python3 manage.py makemigrations
# python3 manage.py migrate
# python3 manage.py createsuperuser
# python3 manage.py runserver
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    context = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='blogpost_like', blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"

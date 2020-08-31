from django.db import models

# Create your models here.
class Venue(models.Model):
    name = models.CharField(max_length=64)
    map_image = models.ImageField(upload_to='map_images', null=True)

    def __str__(self):
        return f"{self.name}"

    def getinfo(self):
        ans = {
            "name": self.name,
            "map_image": self.map_image.url
        }

        return ans

class Floor(models.Model):
    name = models.CharField(max_length=64)
    level = models.IntegerField()

    def __str__(self):
        return f"{self.name}, Level {self.level}"

    def getinfo(self):
        ans = {
            "name": self.name,
            "level": self.level
        }

        return ans

class Stair(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)
    floors = models.ManyToManyField(Floor)

class Room(models.Model):
    name = models.CharField(max_length=64)
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}"

    def getinfo(self):
        ans = {
            "name": self.name,
            "venue": self.venue.getinfo(),
            "floor": self.floor.getinfo()
        }

        return ans

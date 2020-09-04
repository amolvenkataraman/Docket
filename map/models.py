from django.db import models

# Create your models here.
class Venue(models.Model):
    name = models.CharField(max_length=64)
    main = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.name}"

    def getinfo(self):
        ans = {
            "id": self.id,
            "name": self.name,
            "main": str(self.main),
        }

        return ans

class Floor(models.Model):
    name = models.CharField(max_length=64)
    level = models.IntegerField()
    main = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.name}, Level {self.level}"

    def getinfo(self):
        ans = {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "main": str(self.main),
        }

        return ans

class FloorPlan(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT)
    map_image = models.ImageField(upload_to='map_images', null=True)

    def __str__(self):
        return f"Floor plan for: {self.venue.name}, Floor: {self.floor.name}"

    def getinfo(self):
        ans = {
            "id": self.id,
            "venue": self.venue.getinfo(),
            "floor": self.floor.getinfo(),
            "map_image": self.map_image.url
        }

class FloorTransport(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)
    floors = models.ManyToManyField(Floor)
    bllat = models.FloatField()
    bllng = models.FloatField()
    trlat = models.FloatField()
    trlng = models.FloatField()

    def __str__(self):
        return f""

    def getinfo(self):
        ans = {
            "id": self.id,
            "name": self.venue.getinfo(),
            "floors": [i.getinfo() for i in self.floors],
            "bllat": self.bllat,
            "bllng": self.bllng,
            "trlat": self.trlat,
            "trlng": self.trlng
            
        }

        return ans

class Stair(FloorTransport):
    pass

class Elevator(FloorTransport):
    pass

class RoomType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

    def getinfo(self):
        ans = {
            "id": self.id,
            "name": self.name
        }

        return ans

class Room(models.Model):
    name = models.CharField(max_length=64)
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT)
    Type = models.ForeignKey(RoomType, on_delete=models.PROTECT, null=True)
    info = models.TextField(null=True)
    bllat = models.FloatField()
    bllng = models.FloatField()
    trlat = models.FloatField()
    trlng = models.FloatField()

    def __str__(self):
        return f"{self.name}, Type: {self.Type.name}"

    def getinfo(self):
        ans = {
            "id": self.id,
            "name": self.name,
            "venue": self.venue.getinfo(),
            "floor": self.floor.getinfo(),
            "type": self.Type.getinfo(),
            "info": self.info,
            "bllat": self.bllat,
            "bllng": self.bllng,
            "trlat": self.trlat,
            "trlng": self.trlng
        }

        return ans

class Entrance(models.Model):
    name = models.CharField(max_length=64)
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT)
    entrance = models.BooleanField()
    Exit = models.BooleanField()
    emergency = models.BooleanField()
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return f"{self.name}"

    def getinfo(self):
        ans = {
            "id": self.id,
            "name": self.name,
            "venue": self.venue.getinfo(),
            "floor": self.floor.getinfo(),
            "entrance": str(self.entrance),
            "exit": str(self.Exit),
            "emergency": str(self.emergency),
            "lat": self.lat,
            "lng": self.lng,
        }

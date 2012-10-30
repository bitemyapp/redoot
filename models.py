import peewee

database = peewee.SqliteDatabase("woots.db")

class Post(peewee.Model):
    type = peewee.CharField()
    title = peewee.CharField()
    site = peewee.CharField()
    start_date = peewee.DateField()
    end_date = peewee.DateField()
    def __unicode__(self):
        return self.title

    class Meta:
        database = database

if __name__ == "__main__":
    Post.create_table()

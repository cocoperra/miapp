from django.db import models

class Player(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    equipo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, null=True)
    ano = models.DateField()
    posicion= models.CharField(max_length=100)
    pdfes = models.ManyToManyField('Pdf', blank=True, related_name='players')  # Especificar un nombre de relación inversa
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)

    def __str__(self):
        return self.nombre


class Pdf(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='pdfs')  # Asegúrate de que el nombre de la relación inversa sea único
    file = models.FileField(upload_to='pdfs/')
    
    def __str__(self):
        return self.file.name
from django.db import models
from django.contrib.auth.models import User

class Tesouro(models.Model):
    nome = models.CharField(max_length=45)
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=10,decimal_places=2)
    img_tesouro = models.ImageField(upload_to="imgs", verbose_name='Imagem')

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='recorte', verbose_name='Usuario')

    def __str__(self):
    	return self.nome

    class Meta:
    	verbose_name = "Tesouro"
    	verbose_name_plural = "Tesouros"

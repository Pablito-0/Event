from django.contrib.auth.models import User, AbstractUser
from django.db import models


class BaseDate(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Event(BaseDate):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', null=True)
    date = models.DateField(verbose_name='Дата проведения', null=True)

    organisator = models.ForeignKey('Company',
                                    verbose_name='Организатор',
                                    null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='event')

    sponsor = models.ManyToManyField('Company',
                                     verbose_name='Спонсор',
                                     related_name='+')

    ticket_count = models.PositiveIntegerField(verbose_name='Количество билетов')

    def __str__(self):
        return f'{self.title} | {self.description} | {self.ticket_count}'

    def save(self, * args, **kwargs):
        tickets_amount = Ticket.objects.filter(event=self).count()
        if self.ticket_count < tickets_amount:
            self.ticket_count = tickets_amount
        super().save(*args, **kwargs)


class CustomUser(AbstractUser):
    TIERS = ('G', 'Gold'), \
            ('S', 'Silver'), \
            ('B', 'Bronse')

    tier = models.CharField(max_length=1, verbose_name='Уровень подписки', choices=TIERS, null=True, blank=True)

    def __str__(self):
        return f'{self.tier}'


class Ticket(BaseDate):
    event = models.ForeignKey('Event', verbose_name='Название мероприятия', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(verbose_name='Цена')
    number = models.PositiveIntegerField(verbose_name='Номер билета')
    vip = models.BooleanField(verbose_name='Статус билета "ВИП"', default=False)
    user = models.ForeignKey(CustomUser, verbose_name='Посетитель', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.event} | {self.user}'


class Company(BaseDate):
    title = models.CharField(max_length=150, verbose_name='Наименование организации')






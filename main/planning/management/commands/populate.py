from django.core.management.base import BaseCommand
from ...models import Nurse


class Command(BaseCommand):
    """ Populate nurses database """

    help = "Does something"

    def handle(self, *args, **options):
        """ Liste des infirmières """

        nurse_list = [
            ["Ramata Samake", "0652226124", "samakeramata@hotmail.fr", "12 Chemin des Pipeaux, 95800 Cergy"],
            ["Amaria Ghernoug", "0646523475", "amaria48@hotmail.fr", "Adresse inconnue"],
            ["Béatrice Wabel", "0603792129", "wablebeatrice@yahoo.fr", "Adresse inconnue"],
            ["Sonia Roubehi", "0783451675", "s.roubehi@yahoo.fr", "Adresse inconnue"]
        ]
        try:
            for line in nurse_list:
                Nurse.objects.create(
                    fullname=line[0],
                    mobile=line[1],
                    email=line[2],
                    address=line[3]
                )
            print("Les infirmières ont bien été enregistrées.")
        except:
            print("Une erreur s'est produite.")
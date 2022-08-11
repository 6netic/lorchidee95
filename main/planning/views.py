from django.shortcuts import render, redirect, reverse
from . process import Process
from . prepare import Prepare
from . models import Tour, Nurse
from . check_vars import check_vars, verify_date
from django.http import HttpResponse, JsonResponse
from django_globals import globals
from django.utils.html import escape
from django.contrib.auth.decorators import login_required


def index(request):
    """ Index page accessible only if logged in """

    if request.user.is_authenticated:
        return render(request, "planning/index.html")
    else:
        return redirect(reverse('member:connect'))


@login_required
def display_form(request):
    """ Inserts 2 tours for a specific date  """

    context = {}
    context['nurses'] = Nurse.objects.all()
    return render(request, 'planning/display_form.html', context=context)


@login_required
def check_variables(request):
    """ Checks whether all variables are correct """

    eval_obj = check_vars(request)
    if isinstance(eval_obj, list):
        return render(request, "planning/display_detailed_form.html", context={'bad_var': eval_obj})
    else:
        globals.tours = Prepare(
            eval_obj['date_tour'], eval_obj['tour_name1'], eval_obj['tour_name2'],
            eval_obj['nurse1'], eval_obj['nurse2'])
        globals.tours.createFolders()
        globals.tours.saveOnLocal([eval_obj['pdf_file1'], eval_obj['pdf_file2']])
        globals.tours.converPdf2Jpg(eval_obj['pdf_file1'].name, "planning/documents/prefecture/")
        globals.tours.converPdf2Jpg(eval_obj['pdf_file2'].name, "planning/documents/village/")
        globals.tours.del_pdf_files()
        message = ["Fichiers pdf convertis en image jpg.", "Extraction du contenu en cours..."]
        return render(request, "planning/display_detailed_form.html", context={'converted': message})


@login_required
def extract_lines(request):
    """ Extract lines from jpg files """

    date_list, lines_list = [], []
    for img_dir in ["planning/documents/prefecture/", "planning/documents/village/"]:
        one_date, part_lines = Process().extractLines(img_dir)
        date_list.append(one_date)
        lines_list.append(part_lines)
    globals.date = date_list
    globals.lines = lines_list
    message = ["Contenu extrait.", "Vérification de la validité des dates..."]
    return render(request, "planning/display_detailed_form.html", context={'extracted': message})


@login_required
def check_date_and_is_registered(request):
    """ Checks date and if tour is already in the database """

    date_list = Process().convertDate(globals.date)
    check_date = verify_date(globals.tours.date_tour, date_list)
    if isinstance(check_date, list):
        return render(request, "planning/display_detailed_form.html", context={'error_in_date': check_date})
    # Checking if date is already in the database
    saved_tour_pref = Tour.objects.filter(jour=globals.tours.date_tour).filter(nomTournee="Préfecture")
    saved_tour_vill = Tour.objects.filter(jour=globals.tours.date_tour).filter(nomTournee="Le Village")
    if saved_tour_pref and saved_tour_vill:
        message = "A cette date, les 2 tournées ont déjà été enregistrées !"
        return render(request, "planning/display_detailed_form.html", context={'already_in': message})
    else:
        message = "Enregistrement en base de données..."
        return render(request, "planning/display_detailed_form.html", context={'recording_status': message})


@login_required
def insert_tour(request):
    """ Inserts datas in the database """

    nurses_list = [globals.tours.nurse1, globals.tours.nurse2]
    tours_list = [globals.tours.tour_name1, globals.tours.tour_name2]
    for i in range(2):
        for line in globals.lines[i]:
            new_entry = Tour.objects.create(
                nurse=Nurse.objects.get(id=int(nurses_list[i])),
                jour=globals.tours.date_tour,
                heure=line[0],
                patient=line[1],
                addrTel=line[2],
                cotation=line[3],
                assure=line[4],
                honoraire=line[5],
                finTraitement=line[6],
                commentaires=" ",
                nomTournee=tours_list[i]
            )
    return HttpResponse("<span style='color:green;'>Enregistrement de la tournée effectué avec succès !</span>")


@login_required
def display_tour(request):
    """ Displays a tour for a selected date """

    if request.method == 'POST':
        context = {}
        if not request.POST.get("date_search"):
            context['no_date'] = True
            return render(request, "planning/display_detailed_tour.html", context=context)
        if not request.POST.get("nom_tournee"):
            tour_name = "Préfecture"
        else:
            tour_name = escape(request.POST.get("nom_tournee"))
        context['tour_name'] = tour_name
        date = escape(request.POST.get("date_search"))
        context['date'] = date
        tour_day = Tour.objects.filter(jour=date).filter(nomTournee=tour_name).order_by('id')
        if tour_day:
            context['tour_day'] = tour_day
            return render(request, "planning/display_detailed_tour.html", context=context)
        else:
            context['no_tour'] = True
            return render(request, "planning/display_detailed_tour.html", context=context)
    # GET method
    return render(request, "planning/display_tour.html", context={'calendar': True})


@login_required
def save_comment(request):
    """ Saves a comment for a specific line """

    if request.method == 'POST':
        try:
            this_id = int(request.POST.get("this_id"))
            comment = escape(request.POST.get("comment_content"))
            entry = Tour.objects.get(pk=this_id)
            entry.commentaires = comment
            entry.save()
            return JsonResponse(status=200, data={'message': "Ok"})
        except:
            return JsonResponse(status=230, data={'message': "Not Ok"})


@login_required
def validate_line(request):
    """ Validates selected line """

    if request.method == 'POST':
        try:
            this_id = int(request.POST.get("this_id"))
            entry = Tour.objects.get(pk=this_id)
            entry.traite = True
            entry.save()
            return JsonResponse(status=200, data={'message': "Ok"})
        except:
            return JsonResponse(status=230, data={'message': "Not OK"})


from django.utils.html import escape


def check_vars(request):
    """ Checks submitted values from the form """

    error_msg = []
    variables = {}
    if not request.POST.get("date_tour"):
        error_msg.append("Une date valide doit être sélectionnée.")
    if not request.FILES.get("pdf_file1"):
        error_msg.append("Le fichier PDF contenant la tournée de la Préfecture doit être sélectionné.")
    if not request.FILES.get("pdf_file2"):
        error_msg.append("Le fichier PDF contenant la tournée du Village doit être sélectionné.")
    if request.FILES.get("pdf_file1"):
        if request.FILES.get("pdf_file1").content_type != 'application/pdf':
            error_msg.append("Le fichier pour la tournée de la Préfecture doit être au format PDF.")
    if request.FILES.get("pdf_file2"):
        if request.FILES.get("pdf_file2").content_type != 'application/pdf':
            error_msg.append("Le fichier pour la tournée du Village doit être au format PDF.")
    if len(error_msg) == 0:
        variables['date_tour'] = escape(request.POST.get("date_tour"))
        variables['tour_name1'] = escape(request.POST.get("tour_name1"))
        variables['tour_name2'] = escape(request.POST.get("tour_name2"))
        variables['nurse1'] = escape(request.POST.get("nurse1"))
        variables['nurse2'] = escape(request.POST.get("nurse2"))
        variables['pdf_file1'] = request.FILES.get("pdf_file1")
        variables['pdf_file2'] = request.FILES.get("pdf_file2")
        return variables
    else:
        return error_msg


def verify_date(date_form, date_in_file):
    """ Checks date in the form and in the files"""

    error_msg = []
    if date_in_file[0] != date_in_file[1]:
        error_msg.append("Les dates dans les 2 plannings ne correspondent pas au même jour.")
    if date_form != date_in_file[0]:
        error_msg.append("La date dans le formulaire et celle du planning 'Préfecture' sont différentes.")
    if date_form != date_in_file[1]:
        error_msg.append("La date dans le formulaire et celle du planning 'Le Village' sont différentes.")
        return error_msg
    else:
        return date_form

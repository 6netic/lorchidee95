from os import path, mkdir, listdir, remove
import fitz


class Prepare:
    """ Operates on folders and files to be processed """

    def __init__(self, date_tour, tour_name1, tour_name2, nurse1, nurse2):
        """ Initializing variables """

        self.base_path = path.dirname(path.abspath(__file__))
        self.documents_dir = path.join(self.base_path, "documents")
        self.pref_dir = path.join(self.documents_dir, "prefecture")
        self.vill_dir = path.join(self.documents_dir, "village")
        self.date_tour = date_tour
        self.tour_name1 = tour_name1
        self.tour_name2 = tour_name2
        self.nurse1 = nurse1
        self.nurse2 = nurse2
        self.resolution = 200


    def createFolders(self):
        """ Creates empty directories or delete all files within pdf/ and jpg/ """

        try:
            mkdir(self.documents_dir)
            mkdir(self.pref_dir)
            mkdir(self.vill_dir)

        except FileExistsError:
            pass
            # for directory in [self.pref_dir, self.vill_dir]:
            #     for file in listdir(directory):
            #         file = path.join(directory, file)
            #         remove(file)


    def saveOnLocal(self, files_list):
        """ Saves PDF file(s) to PDF folder """

        for pos, directory in enumerate([self.pref_dir, self.vill_dir]):
            with open(path.join(directory, files_list[pos].name), 'wb+') as destination:
                for chunk in files_list[pos].chunks():
                    destination.write(chunk)


    def converPdf2Jpg(self, file, location):
        """ Converts pdf file to jpg file(s) for each foler"""

        file = fitz.open(location + file)
        for page in file:
            image = page.get_pixmap(dpi=self.resolution)
            image.save(file.name.rsplit('.', 1)[0].lower() + "_%i.jpg" % page.number)


    def del_pdf_files(self):
        """ Moves jpg files """

        for directory in [self.pref_dir, self.vill_dir]:
            for file in listdir(directory):
                if file.endswith('.pdf'):
                    file = path.join(directory, file)
                    remove(file)
















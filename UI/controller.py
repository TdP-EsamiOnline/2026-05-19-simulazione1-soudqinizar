import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):

        genre = self._model.getAllGenre()
        genreDD = list(map(lambda x: ft.dropdown.Option(x), genre))
        self._view._ddGenre.options = genreDD
        self._view.update_page()


    def handleCreaGrafo(self, e):
        self._view._txtResult.controls.clear()

        # Ora questo conterrà direttamente una stringa come "Rock"
        genere_selezionato = self._view._ddGenre.value

        if genere_selezionato is None:
            self._view._txtResult.controls.append(ft.Text("Errore: Seleziona un genere dal menù a tendina.", color="red"))
            self._view.update_page()
            return

        try:
            # Passiamo direttamente la stringa al modello
            self._model.creaGrafo(genere_selezionato)

            # Statistiche base
            n_v, n_a = self._model.getInfoGrafo()
            self._view._txtResult.controls.append(ft.Text(f"Grafo creato correttamente per il genere {genere_selezionato}!"))
            self._view._txtResult.controls.append(ft.Text(f"Numero di vertici: {n_v}"))
            self._view._txtResult.controls.append(ft.Text(f"Numero di archi: {n_a}"))


            # Artista con maggiore influenza
            nome_top, infl = self._model.getArtistaMaggioreInfluenza()
            if nome_top:
                self._view._txtResult.controls.append(
                    ft.Text(f"\nArtista con maggiore influenza: {nome_top} (Influenza: {int(infl)})",
                            weight=ft.FontWeight.BOLD))

            # Top 5 archi
            top5 = self._model.getTop5Archi()
            if top5:
                self._view._txtResult.controls.append(ft.Text("\nI 5 archi con peso maggiore:"))
                for arco_str in top5:
                    self._view._txtResult.controls.append(ft.Text(arco_str))
            else:
                self._view._txtResult.controls.append(ft.Text("\nNessun arco presente nel grafo."))

            self._view.update_page()

        except Exception as ex:
            self._view._txtResult.controls.clear()
            self._view._txtResult.controls.append(ft.Text(f"Si è verificato un errore: {str(ex)}", color="red"))
            self._view.update_page()

    def handleCammino(self, e):
        pass


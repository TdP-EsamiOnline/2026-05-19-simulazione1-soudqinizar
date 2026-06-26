import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._ddGenreValue = None

    def fillDDGenre(self):
        self._view._ddGenre.options.clear()
        self._view._ddGenre.value = None
        self._view._ddGenreValue = None

        for c in self._model.getAllGenre():
            self._view._ddGenre.options.append(ft.dropdown.Option(
                key=c.Name,
                data=c,
                on_click=self._choiceDDGenre
            ))
        self._view.update_page()

    def _choiceDDGenre(self, e):
        # salvare la variabile nella classe controller
        self._ddGenreValue = e.control.data
        self.fillDDArtist()

    def fillDDArtist(self):
        self._view._ddArtist.options.clear()
        self._view._ddArtist.value = None
        self._view._ddArtistValue = None
        genreId = self._ddGenreValue
        if genreId is None:
            return
        nodi = self._model.getNodes(genreId.GenreId)
        for c in nodi:
            self._view._ddArtist.options.append(ft.dropdown.Option(
                key=c.Name,
                data=c,
                on_click=self._choiceDDArtist
            ))
        self._view.update_page()

    def _choiceDDArtist(self, e):
        # salvare la variabile nella classe controller
        self._ddArtistValue = e.control.data

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        genreId = self._ddGenreValue
        if self._ddGenreValue is None:
            self._view.txt_result.controls.append(ft.Text("No genre selected!", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(genreId.GenreId)
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato", color="green"))

        self._view.txt_result.controls.append(ft.Text(f"Num nodi: {self._model.getNumNodes()}"))
        self._view.txt_result.controls.append(ft.Text(f"Num archi: {self._model.getNumEdges()}"))
        bestScore, bestArtista = self._model.getInfluente()
        self._view.txt_result.controls.append(ft.Text(f"L'artista più influente è : {bestArtista}, con score {bestScore}"))
        self._view.txt_result.controls.append(ft.Text(f"Top 5 ", color="green"))

        top5 = self._model.get5()
        for a1, a2, peso in top5:
            self._view.txt_result.controls.append(
                ft.Text(f"{a1} -> {a2}, peso {peso}"))

        self._view.update_page()

    def handleCammino(self, e):
        bestPath = self._model.bestPath(self._ddArtistValue)
        self._view.txt_result.controls.append(ft.Text(f"Cammino massimo trovato ({len(bestPath)} nodi):"))

        for a in bestPath:
            self._view.txt_result.controls.append(ft.Text(a.Name))

        self._view.update_page()
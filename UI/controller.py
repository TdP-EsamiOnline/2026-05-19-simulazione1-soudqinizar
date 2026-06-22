import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        self._genreMap = {}
        generi = self._model.fillGenre()
        for g in generi:
            self._genreMap[str(g.GenreId)] = g
            self._view._ddGenre.options.append(
                ft.dropdown.Option(key=g.GenreId, text=g.Name)
            )
        self._view.update_page()

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        genre = self._view._ddGenre.value
        self._model.buildGraph(genre)
        print("NODI:", self._model.getNumNodes(), "ARCHI:", self._model.getNumEdges())
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Num nodi: {self._model.getNumNodes()}"))
        self._view.txt_result.controls.append(ft.Text(f"Num Archi: {self._model.getNumEdges()}"))
        artista,influenza = self._model.getInfluenza()
        self._view.txt_result.controls.append(ft.Text(f"L'artista più influente : {artista}, con influenza: {influenza}", color="green"))
        artist = self._model.fillArtist(genre)

        for a in artist:
            self._view._ddArtist.options.append(
                ft.dropdown.Option(key=a.ArtistId, text=a.Name)
            )


        self._view.update_page()

    def handleCammino(self, e):
        self._view.txt_result.controls.clear()
        artista = self._view._ddArtist.value
        soluzione = self._model.bestPath(artista)

        self._view.txt_result.controls.append(
            ft.Text(f"Il percorso trovato percorre {len(soluzione) - 1} archi:", color="green")
        )

        for i in range(len(soluzione) - 1):
            u = soluzione[i]
            v = soluzione[i + 1]
            peso = self._model.getPesoArco(u, v)
            self._view.txt_result.controls.append(
                ft.Text(f"{u.Name} -> {v.Name}: costo {peso}")
            )

        self._view.update_page()



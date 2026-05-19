import networkx as nx

from database.DAO import DAO


class Model:


    def __init__(self):
        self._grafo = nx.DiGraph()
        self._id_to_artist = {}
        self._id_to_genre = {}

    def getAllGenre(self):
        return DAO.getAllGenre()


    def creaGrafo(self, genre_name):

        # Ripristina il grafo ad ogni click
        self._grafo.clear()
        self._id_to_artist.clear()
        self._id_to_genre = {}

        generi = DAO.getAllGenre()
        for g in generi:
            self._id_to_genre[g["Name"]] = g["GenreId"]

        # 1. Recupera i vertici filtrati per NOME del genere (stringa)
        artisti_genere = DAO.getVerticiPerGenere(self._id_to_genre[g["Name"]])
        if not artisti_genere:
            return

        for a in artisti_genere:
            self._grafo.add_node(a["ArtistId"])
            self._id_to_artist[a["ArtistId"]] = a["Name"]

        # 2. Popolarità e acquisti dei clienti (rimangono invariati)
        popolarita_map = DAO.getPopolaritaArtisti()
        clienti_mappa = DAO.getArtistiPerCliente()

        # 3. Costruzione degli archi (rimane identica a prima)
        nodi_validi = set(self._grafo.nodes)
        coppie_controllate = set()

        for artisti_cliente in clienti_mappa.values():
            filtrati = list(artisti_cliente.intersection(nodi_validi))

            for i in range(len(filtrati)):
                for j in range(i + 1, len(filtrati)):
                    a_id = filtrati[i]
                    b_id = filtrati[j]

                    coppia = (min(a_id, b_id), max(a_id, b_id))
                    if coppia not in coppie_controllate:
                        coppie_controllate.add(coppia)

                        pop_a = popolarita_map.get(a_id, 0)
                        pop_b = popolarita_map.get(b_id, 0)
                        peso = float(pop_a + pop_b)

                        if pop_a > pop_b:
                            self._grafo.add_edge(a_id, b_id, weight=peso)
                        elif pop_b > pop_a:
                            self._grafo.add_edge(b_id, a_id, weight=peso)
                        else:
                            self._grafo.add_edge(a_id, b_id, weight=peso)
                            self._grafo.add_edge(b_id, a_id, weight=peso)

    def getInfoGrafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getArtistaMaggioreInfluenza(self):
        if len(self._grafo.nodes) == 0:
            return None, 0

        max_influenza = -float('inf')
        top_artista_id = None

        for n in self._grafo.nodes:
            # Peso archi uscenti
            peso_out = sum(d['weight'] for u, v, d in self._grafo.out_edges(n, data=True))
            # Peso archi entranti
            peso_in = sum(d['weight'] for u, v, d in self._grafo.in_edges(n, data=True))

            influenza = peso_out - peso_in
            if influenza > max_influenza:
                max_influenza = influenza
                top_artista_id = n

            if top_artista_id is not None:
                return self._id_to_artist[top_artista_id], max_influenza
            return None, 0

    def getTop5Archi(self):
        archi_pesati = []

        for u, v, d in self._grafo.edges(data=True):
            archi_pesati.append((u, v, d['weight']))

        # Ordina per peso decrescente
        archi_pesati.sort(key=lambda x: x[2], reverse=True)

        risultato = []
        for u, v, w in archi_pesati[:5]:
            nome_u = self._id_to_artist[u]
            nome_v = self._id_to_artist[v]
            risultato.append(f"{nome_u} -> {nome_v} (Peso: {int(w)})")
        return risultato








































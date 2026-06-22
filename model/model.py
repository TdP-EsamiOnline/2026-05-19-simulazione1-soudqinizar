import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}
        self._bestPath = []
        self._bestScore = None

    def bestPath(self, primo):
        self._bestPath = []
        parziale = [self._idMap[int(primo)]]
        self.ricorsione(parziale, 0)
        return self._bestPath

    def ricorsione(self, parziale, pesoPrecedente):
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        ultimo = parziale[-1]
        for vicino in self._graph.successors(ultimo):
            if vicino not in parziale:
                pesoCorrente = self._graph[ultimo][vicino]["weight"]
                if pesoCorrente > pesoPrecedente:
                    parziale.append(vicino)
                    self.ricorsione(parziale, pesoCorrente)
                    parziale.pop()

    def getPesoArco(self, u, v):
        return self._graph[u][v]["weight"]


    def fillArtist(self, genere):
        return DAO.getFillArtist(genere)


    def buildGraph(self, genre):
        self._graph.clear()

        nodi = DAO.getAllNodes(genre)
        self._graph.add_nodes_from(nodi)

        for artist in nodi:
            self._idMap[artist.ArtistId] = artist

        edges = DAO.getEdges(genre)
        for edge in edges:
            if edge[2] > edge[3]:
                self._graph.add_edge(self._idMap[edge[0]], self._idMap[edge[1]], weight=edge[4])
            elif edge[2] < edge[3]:
                self._graph.add_edge(self._idMap[edge[1]], self._idMap[edge[0]], weight=edge[4])
            else:
                self._graph.add_edge(self._idMap[edge[0]], self._idMap[edge[1]], weight=edge[4])
                self._graph.add_edge(self._idMap[edge[1]], self._idMap[edge[0]], weight=edge[4])

    def getInfluenza(self):
        influenza = 0
        lista = []
        for n in self._graph.nodes():
            pesoUscenti = 0
            for u,v,data in self._graph.out_edges(n, data=True):
                pesoUscenti += data['weight']
            pesoEntranti = 0
            for u,v,data in self._graph.in_edges(n,data=True):
                pesoEntranti += data["weight"]

            influenza = pesoUscenti - pesoEntranti
            lista.append((n,influenza))
        lista.sort(key=lambda x: x[1], reverse=True)
        return lista[0]









    def fillGenre(self):
        generi = DAO.getAllGenre()
        return generi


    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)
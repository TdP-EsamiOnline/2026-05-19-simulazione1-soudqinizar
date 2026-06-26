import copy
import itertools
from collections import defaultdict

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}
        self._bestPath = []

    def bestPath(self, source):
        print(f"Source: {source.Name}")
        print(f"Nodi nel grafo: {[n.Name for n in self._graph.nodes()][:5]}")
        print(f"Source in grafo: {source in self._graph.nodes()}")
        print(f"Out edges: {list(self._graph.out_edges(source, data=True))}")

        self._bestPath = []
        partial = [source]
        self._ricorsione(partial, float('-inf'))
        return self._bestPath

    def _ricorsione(self, partial, lastWeight):
        # update best solution
        if len(partial) > len(self._bestPath):
            self._bestPath = copy.deepcopy(partial)

        current = partial[-1]

        for _, successor, data in self._graph.out_edges(current, data=True):
            weight = data["weight"]

            # strictly increasing weights
            if weight > lastWeight:
                # simple path
                if successor not in partial:
                    partial.append(successor)
                    self._ricorsione(partial, weight)
                    partial.pop()

    def buildGraph(self, genreId):
        self._graph.clear()
        self._idMap = {}
        nodi = DAO.getNodes(genreId)
        for n in nodi:
            self._idMap[n.ArtistId] = n
        self._graph.add_nodes_from(nodi)

        arc = DAO.getEdges(genreId)

        clienti = defaultdict(dict)
        for cl, artistId, nTracce in arc:
            clienti[cl][artistId] = nTracce

        popolarita = defaultdict(int)
        for cliente, artista in clienti.items():
            for artistId, nTracce in artista.items():
                popolarita[artistId] += nTracce


        coppieViste = set()
        for cliente, artista in clienti.items():
            for a, b in itertools.combinations(artista.keys(), 2):
                if (a, b) in coppieViste or (b, a) in coppieViste:
                    continue
                coppieViste.add((a, b))

                pop1 = popolarita[a]
                pop2 = popolarita[b]
                peso = pop1 + pop2

                if a not in self._idMap or b not in self._idMap:
                    continue

                if pop1 > pop2:
                    self._graph.add_edge(self._idMap[a], self._idMap[b], weight=peso)
                elif pop1 < pop2:
                    self._graph.add_edge(self._idMap[b], self._idMap[a], weight=peso)
                else:
                    self._graph.add_edge(self._idMap[a], self._idMap[b], weight=peso)
                    self._graph.add_edge(self._idMap[b], self._idMap[a], weight=peso)


    def getInfluente(self):
        bestScore = 0
        bestArtista = None

        for n in self._graph.nodes():
            uscenti = 0
            entranti = 0
            for _,_,d in self._graph.out_edges(n, data=True):
                uscenti += (d["weight"])
            for _,_,d in self._graph.in_edges(n, data=True):
                entranti += (d["weight"])
            influenza = uscenti - entranti


            if influenza > bestScore:
                bestScore = influenza
                bestArtista = n
        return bestScore, bestArtista

    def get5(self):

        lista = []

        for a1,a2,peso in self._graph.edges(data=True):
            lista.append((a1,a2,peso["weight"]))

        lista.sort(key=lambda x: x[2], reverse=True)
        return lista[:5]











    def getAllGenre(self):
        return DAO.getAllGenre()
    def getNodes(self, genreId):
        return DAO.getNodes(genreId)

    def getNumNodes(self):
        return len(self._graph.nodes())

    def getNumEdges(self):
        return len(self._graph.edges())
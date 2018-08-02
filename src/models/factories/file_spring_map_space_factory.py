# -*- coding: utf-8 -*-

from typing import Dict
from typing import List
from typing import Tuple

import networkx as nx

from models import MapEdge
from models import MapNode
from models.factories import MapSpaceFactoryType


class FileSpringMapSpaceFactory(MapSpaceFactoryType):
    def __init__(self, json_map: Dict, spring_iterations: int) -> None:
        self._json_map = json_map
        self._spring_iterations = spring_iterations

        self._nodes_by_name: Dict[str, MapNode] = {}
        self._edges_by_pair: Dict[Tuple[MapNode, MapNode], MapEdge] = {}

    def generate_nodes(self) -> List[MapNode]:
        graph = nx.Graph()

        for node_name, peers in self._json_map.items():
            for peer_cost_pair in peers:
                peer_name, _ = list(peer_cost_pair.items())[0]
                graph.add_edge(node_name, peer_name)

        positions = nx.spring_layout(graph, iterations=self._spring_iterations)

        for node_position_pair in positions.items():
            node, position = node_position_pair

            pos_x = float((0.45 + position[0] * 0.45))
            pos_y = float((0.45 + position[1] * 0.45))

            self._nodes_by_name[node] = MapNode(node, (pos_x, pos_y))

        return list(self._nodes_by_name.values())

    def generate_edges(self) -> List[MapEdge]:
        for node_name, peers in self._json_map.items():
            for peer_cost_pair in peers:
                peer_name, cost = list(peer_cost_pair.items())[0]

                _1 = self._nodes_by_name[node_name]
                _2 = self._nodes_by_name[peer_name]

                if (_2, _1) in self._edges_by_pair.keys():
                    continue  # Skip duplicates

                self._edges_by_pair[(_1, _2)] = MapEdge((_1, _2), cost)

        return list(self._edges_by_pair.values())

    def generate_defaults(self) -> Tuple[MapNode, MapNode]:
        from_node = self._nodes_by_name["Arad"]
        to_node = self._nodes_by_name["Bucharest"]

        return from_node, to_node

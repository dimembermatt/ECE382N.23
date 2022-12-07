import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import time
import os
from PIL import Image

GIF_FRAMES_PER_SECOND = 1


class Node:
    def __init__(self, node_id, connected_nodes_list) -> None:
        self.node_id = node_id
        self.connections = connected_nodes_list

    def __str__(self) -> str:
        return f"Node {self.node_id} connected to {self.connections}"


class Grapher:
    def __init__(self, node_list) -> None:
        self.node_list = node_list
        self.graph = nx.DiGraph()

        # assign numerical id to each node
        self.node_ids = np.arange(0, len(self.node_list)).tolist()
        self.reverse_id_lookup = dict()

        # create reverse lookup and add table names
        self.labels = dict()
        for i in range(len(self.node_list)):
            id = self.node_ids[i]
            self.reverse_id_lookup[self.node_list[id].node_id] = id
            self.labels[i] = self.node_list[id].node_id

        self.graph.add_nodes_from(self.node_ids)

        # create edges list
        self.edge_list = []
        for i in range(len(self.node_list)):
            node_id = self.node_list[i].node_id
            node_id_num = self.reverse_id_lookup[node_id]
            node_connections = self.node_list[i].connections

            for connection in node_connections:
                connection_num = self.reverse_id_lookup[connection]
                self.edge_list.append((node_id_num, connection_num))
        self.graph.add_edges_from(self.edge_list)

        self.pos = nx.spring_layout(self.graph)

        # add node colors and sizes
        self.node_colors = []
        self.node_sizes = []
        for i in range(0, len(self.node_list)):
            self.node_colors.append("white")
            self.node_sizes.append(1200)

        # add edge colors
        self.edge_colors = []
        for i in range(0, len(self.edge_list)):
            self.edge_colors.append("black")

        # TODO get auto generated positions
        # print("Auto-generated positions: " + str(self.pos))

        self.screenshot_count = 0
        self.screenshot_list = []

    def set_edge_color(self, node_id_1, node_id_2, color):
        edge_1 = (self.reverse_id_lookup[node_id_1], self.reverse_id_lookup[node_id_2])
        edge_2 = (self.reverse_id_lookup[node_id_2], self.reverse_id_lookup[node_id_1])

        for i in range(len(self.edge_list)):
            if edge_1 == self.edge_list[i] or edge_2 == self.edge_list[i]:
                self.edge_colors[i] = color

    def set_node_color(self, node_id, color):
        node_id_num = self.reverse_id_lookup[node_id]
        self.node_colors[node_id_num] = color

    def set_image_time(self, time):
        if time >= 0:
            plt.title("t = " + str(time))
        else:
            plt.title("Initial")

    def draw_network(self):
        nx.draw_networkx(
            self.graph,
            pos=self.pos,
            labels=self.labels,
            arrows=True,
            node_shape="s",
            node_size=self.node_sizes,
            node_color=self.node_colors,
            edge_color=self.edge_colors,  # color of the edges
            edgecolors="gray",
        )  # edges of the box of node
        nx.draw_networkx_edge_labels(
            self.graph, pos=self.pos, edge_labels={}, font_color="black"
        )

    def show(self):
        self.draw_network()
        plt.show()

    def save_graph_as_image(self, folder_path):
        self.draw_network()
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        image_name = "capture-" + str(self.screenshot_count) + ".png"
        image_path = os.path.join(folder_path, image_name)
        self.screenshot_list.append(image_path)
        # print("Saving image " + str(self.screenshot_count) + " to: " + str(image_path))

        plt.savefig(image_path, bbox_inches="tight")
        plt.clf()

        self.screenshot_count += 1

    def generate_gif(self, screenshot_list, gif_path):
        # create folder for gif
        folder_path = os.path.dirname(gif_path)
        if len(folder_path) > 0 and not os.path.exists(folder_path):
            os.makedirs(folder_path)

        print("Generating and saving gif to: " + str(gif_path))
        frames = []
        for i in screenshot_list:
            new_frame = Image.open(i)
            frames.append(new_frame)
        frames[0].save(
            gif_path,
            format="GIF",
            append_images=frames[1:],
            save_all=True,
            duration=1000 / GIF_FRAMES_PER_SECOND,
            loop=0,
        )

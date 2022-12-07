from grapher import Grapher, Node

IMAGE_CACHE = "image-cache"

node_list = []
node_list.append(Node("A", ["B", "C"]))
node_list.append(Node("B", ["A", "E"]))
node_list.append(Node("C", ["E", "A"]))
node_list.append(Node("D", ["E", "F"]))
node_list.append(Node("E", ["B", "C", "D", "F"]))
node_list.append(Node("F", ["D", "E"]))

grapher = Grapher(node_list)
grapher.set_image_time(1)
grapher.show()
grapher.save_graph_as_image(IMAGE_CACHE)
grapher.set_edge_color("A", "B", "red")
grapher.save_graph_as_image(IMAGE_CACHE)
grapher.set_node_color("C", "skyblue")
grapher.save_graph_as_image(IMAGE_CACHE)
# grapher.show()

screenshot_list = grapher.screenshot_list
grapher.generate_gif(screenshot_list, "output.gif")

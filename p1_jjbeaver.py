import argparse
import snap
import os, sys

parser = argparse.ArgumentParser(description='Print Graph Statistics.')
parser.add_argument('net_dir_path', action="store", help="path to directory containing graph files")
parser.add_argument('out_file_path', action="store", help="output filepath (creates file)")
args = parser.parse_args()
graphs_dir = args.net_dir_path
output_file = args.out_file_path

class Node:
  def __init__(self, id, degree):
    self.id = id
    self.degree = degree

# Get list of all alter nodes in ego network
# based on .feat file. Returns list of alter node IDs
def get_alter_node_ids(fp):
  with open(fp) as f:
    for line in f.readlines():
      yield int(line.partition(' ')[0])

# Print degrees of each node in an ego-network
def print_node_degrees(graph, ego_id):
  global out_file
  out_file.write("%d:\n" % ego_id)
  nodes = []

  # Had to create own nodes because of some odd proxy/Swig object, C-level issues
  for node in graph.Nodes():
    nodes.append(Node(node.GetId(), node.GetDeg()))

  for node in sorted(nodes, key=lambda node: node.id):
    out_file.write("%d %d\n" % ( node.id, node.degree))

# Return graph using graphs_dir/<ego>.edges and graphs_dir/<ego>.feat
def get_graph(graphs_dir, ego_id):
  graph = snap.LoadEdgeList(snap.PNGraph, os.path.join(graphs_dir, "%d.edges" % ego_id), 0, 1)
  graph.AddNode(ego_id)

  for node_id in get_alter_node_ids(os.path.join(graphs_dir, "%d.feat" % ego_id)):
    # Try to add node before inserting corresponding ego-alter edge. 
    # If a RuntimeError occurs, node already exists in graph - pass
    try:
      graph.AddNode(node_id)
    except RuntimeError:
      pass
    graph.AddEdge(ego_id, node_id)
    graph.AddEdge(node_id, ego_id)
  return graph

# Return list of circles (a circle is an arrays of node IDs) using graphs_dir/<ego>.circles,
# where index is equal to circle number
def get_circles(graphs_dir, ego_id, ego_in_circle):
  circles = []
  with open(os.path.join(graphs_dir, "%d.circles" % ego_id)) as f:
    for line in f.readlines():
      circle_nodes = line.split()
      # delete "circle<n>:" from nodes list
      del(circle_nodes[0])
      # Convert strings to ints
      circle_nodes = map(int, circle_nodes)
      if ego_in_circle:
        circle_nodes.append(ego_id)
      circles.append(circle_nodes)
  return circles

# Returns number of common attributes among given circle, based on 
# feature matrices. Assumes non-empty feat_matrices
def get_num_common_attributes(feat_matrices, circle):
  num_ca = 0
  combined_matrix = [1] * len(feat_matrices.values()[0])
  #calculate common attrs based on matrices
  for node_id in circle:
    for idx in range(len(combined_matrix)):
      combined_matrix[idx] = combined_matrix[idx] & feat_matrices[node_id][idx]
  return sum(combined_matrix)

def get_feat_matrices(feat_fp, egofeat_fp, ego_id):
  feat_matrices = {}
  with open(feat_fp) as f:
    for line in f.readlines():
      feats = map(int, line.split())
      node_id = feats.pop(0)
      feat_matrices[node_id] = feats
  with open(egofeat_fp) as f:
    for line in f.readlines():
      feats = map(int, line.split())
      feat_matrices[ego_id] = feats
  return feat_matrices

def print_circle_size_common_attr_count(circles, feat_matrices, ego_id):
  global out_file
  out_file.write("%d:\n" % ego_id)
  #calculate #attributes in common across each circle
  for idx, circle in enumerate(circles):
    out_file.write("c%d: %d %d\n" % (idx, len(circle),
                    get_num_common_attributes(feat_matrices, circle)))


out_file = open(output_file, "w")

### Hypothesis 1 (amadan2-1) - Common Attributes ###

ego_ids = [0, 1684]

# Print circles, size, and # common attributes with ego (1) not included
# and (2) included in circle.
for ego_in_circle in [False, True]:
  for ego_id in ego_ids:
    circles = get_circles(graphs_dir, ego_id, ego_in_circle)
    feat_fp = os.path.join(graphs_dir, "%d.feat" % ego_id)
    egofeat_fp = os.path.join(graphs_dir, "%d.egofeat" % ego_id)
    feat_matrices = get_feat_matrices(feat_fp, egofeat_fp, ego_id)
    print_circle_size_common_attr_count(circles, feat_matrices, ego_id)
    out_file.write("\n")

### Hypothesis 2 (mmashay2)- Degrees ###

ego_ids = [1912, 3980]

# Print node degrees
for ego_id in ego_ids:
  graph = get_graph(graphs_dir, ego_id)
  print_node_degrees(graph, ego_id)
  if ego_ids.index(ego_id) < len(ego_ids)-1:
    out_file.write("\n")

out_file.close()

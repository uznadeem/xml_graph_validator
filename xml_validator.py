import xml.etree.ElementTree as ET

def validate_xml(xml_data):
    try:
        root = ET.fromstring(xml_data)
        node_ids = set()

        validate_root_tag(root)
        validate_graph_tags(root)
        validate_node_structure(root, node_ids)
        validate_edge_structure(root, node_ids)

        return 'XML is Valid'

    except ET.ParseError as e:
        raise ValueError("Invalid XML structure: " + str(e))

def validate_root_tag(root):
    if root.tag != 'graph':
        raise ValueError("Root element must be 'graph'")
    elif root.find('id') is None or root.find('name') is None:
        raise ValueError("Graph must have an id and a name")

def validate_graph_tags(root):
    if not (root.find('id') is not None and root.find('name') is not None):
        raise ValueError("Missing required <id> or <name> tag in <graph>.")

def validate_node_structure(root, node_ids):
    nodes = root.find('nodes')
    if nodes is None:
        raise ValueError("<nodes> groups must be present")

    if len(list(nodes)) == 0:
        raise ValueError("There must be at least one <node> in the <nodes> group")

    for node in nodes:
        node_id = node.find('id')
        if node_id is None:
            raise ValueError("All nodes must have <id> tags")
        node_id_text = node_id.text
        if node_id_text in node_ids:
            raise ValueError(f"All nodes must have unique <id> tags, but '{node_id_text}' is repeated")
        node_ids.add(node_id_text)

def validate_edge_structure(root, node_ids):
    edges = root.find('edges')
    edge_ids = set()

    if edges is None:
        raise ValueError("<edges> groups must be present")

    for edge in edges:
        if edge.find('from') is None or edge.find('to') is None or edge.find('id'):
            raise ValueError("Each <edge> must have a <id>, <from> and a <to> tag")

        if edge.find('id').text in edge_ids:
            raise ValueError(f"All nodes must have unique <id> tags, but '{edge.find('id').text}' is repeated")
        edge_ids.add(edge.find('id').text)

        if edge.find('from').text not in node_ids or edge.find('to').text not in node_ids:
            raise ValueError(
                f"Each <edge>'s <from> and <to> tags must correspond to defined nodes, "
                f"but '{edge.find('from').text}' or '{edge.find('to').text}' is undefined."
            )

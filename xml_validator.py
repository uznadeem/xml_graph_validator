import xml.etree.ElementTree as ET

def validate_xml(xml_data):
    try:
        root = ET.fromstring(xml_data)
        node_ids = set()

        validate_root_tag(root)
        validate_graph_tags(root)
        validate_node_structure(root, node_ids)
        validate_edge_structure(root, node_ids)

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

    if edges is None:
        raise ValueError("<edges> groups must be present")

    for edge in edges:
        from_node = edge.find('from')
        to_node = edge.find('to')
        if from_node is None or to_node is None:
            raise ValueError("Each <edge> must have a <from> and a <to> tag")

        from_node_text = from_node.text
        to_node_text = to_node.text
        if from_node_text not in node_ids or to_node_text not in node_ids:
            raise ValueError(
                f"Each <edge>'s <from> and <to> tags must correspond to defined nodes, "
                f"but '{from_node_text}' or '{to_node_text}' is undefined."
            )

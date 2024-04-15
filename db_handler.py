import json
import psycopg2
import heapq
import xml.etree.ElementTree as ET

def connect_to_db():
    return psycopg2.connect(
        dbname="directed-graph",
        user="postgres",
        password="1234",
        host="localhost"
    )

def clean_data():
    query = """
        DELETE FROM graph;
        DELETE FROM nodes;
        DELETE FROM edges;
    """

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

def create_tables():
    create_graph_table = """
        CREATE TABLE IF NOT EXISTS graph (
            id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
    """

    create_nodes_table = """
        CREATE TABLE IF NOT EXISTS nodes (
            id VARCHAR(50),
            graph_id VARCHAR(50),
            name VARCHAR(255) NOT NULL,
            PRIMARY KEY (id, graph_id),
            FOREIGN KEY (graph_id) REFERENCES graph(id) ON DELETE CASCADE
        );
    """

    create_edges_table = """
        CREATE TABLE IF NOT EXISTS edges (
            id VARCHAR(50),
            graph_id VARCHAR(50),
            from_node_id VARCHAR(50),
            to_node_id VARCHAR(50),
            cost NUMERIC(10, 2) DEFAULT 0.0,
            PRIMARY KEY (id, graph_id),
            FOREIGN KEY (graph_id) REFERENCES graph(id) ON DELETE CASCADE,
            FOREIGN KEY (from_node_id, graph_id) REFERENCES nodes(id, graph_id),
            FOREIGN KEY (to_node_id, graph_id) REFERENCES nodes(id, graph_id)
        );
    """

    conn = connect_to_db()

    cur = conn.cursor()
    cur.execute(create_graph_table)
    cur.execute(create_nodes_table)
    cur.execute(create_edges_table)

    conn.commit()
    conn.close()

def construct_graph_from_db(cursor, graph_id):
    graph = {}
    query = """
        SELECT n1.id, n2.id, e.cost
        FROM edges e
        JOIN nodes n1 ON e.from_node_id = n1.id
        JOIN nodes n2 ON e.to_node_id = n2.id
        WHERE e.graph_id = %s
    """
    cursor.execute(query, (graph_id,))
    for from_node, to_node, cost in cursor.fetchall():
        if from_node in graph:
            graph[from_node][to_node] = cost
        else:
            graph[from_node] = {to_node: cost}
    return graph

def find_cycles_in_graph(graph_id):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        query = """
            WITH RECURSIVE cycle_check(id, from_node_id, to_node_id, path, cycle) AS (
                SELECT e.id, e.from_node_id, e.to_node_id, ARRAY[e.from_node_id]::varchar[], FALSE
                FROM edges e
                WHERE e.graph_id = %s
            UNION ALL
                SELECT e.id, e.from_node_id, e.to_node_id, path || e.from_node_id, e.from_node_id = ANY(path)
                FROM edges e, cycle_check c
                WHERE e.from_node_id = c.to_node_id AND NOT cycle
            )
            SELECT * FROM cycle_check
            WHERE cycle;
        """

        cursor.execute(query, (graph_id,))

        cycles = set(tuple(cycle[-2]) for cycle in cursor.fetchall())

        return list(cycles)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def insert_graph(cursor, graph_id, name):
    cursor.execute(
        "INSERT INTO graph (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;",
        (graph_id, name)
    )

def insert_node(cursor, node_id, name, graph_id):
    cursor.execute(
        "INSERT INTO nodes (id, name, graph_id) VALUES (%s, %s, %s) ON CONFLICT (id, graph_id) DO NOTHING;",
        (node_id, name, graph_id)
    )

def insert_edge(cursor, id, start_node, end_node, cost, graph_id):
    cursor.execute(
        "INSERT INTO edges (id, from_node_id, to_node_id, cost, graph_id) VALUES (%s, %s, %s, %s, %s);",
        (id, start_node, end_node, cost, graph_id)
    )

def data_insert(xml_data):
    conn = connect_to_db()
    try:
        cursor = conn.cursor()

        root = ET.fromstring(xml_data)

        graph_id = root.find('id').text
        graph_name = root.find('name').text

        insert_graph(cursor, graph_id, graph_name)

        nodes = root.find('nodes')
        for node in nodes.findall('node'):
            node_id = node.find('id').text
            node_name = node.find('name').text
            insert_node(cursor, node_id, node_name, graph_id)

        edges = root.find('edges')
        for edge in edges.findall('node'):
            id = edge.find('id').text
            from_node = edge.find('from').text
            to_node = edge.find('to').text
            cost = edge.find('cost').text if edge.find('cost') is not None else "0"
            insert_edge(cursor,id, from_node, to_node, cost, graph_id)

        conn.commit()
    except Exception as e:
        print("An error occurred:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

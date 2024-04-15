# xml_graph_validator
## Overview
This project automates the process of downloading, validating, and analyzing graph data encapsulated in XML files. It supports extracting graph information, storing it into a database, identifying cycles, and evaluating queries for paths and shortest paths within the graph. Find the complete requirements in this [document](https://drive.google.com/file/d/1NzVtsrz0i3334a9vo7eip_MI_41-wU0k/view?usp=sharing).

## Features
- Downloading of XML files from a constant path.
- XML validation against a set of predefined rules including node and edge structure.
- Cycle detection in directed graphs to identify potential data inconsistencies.
- Query processing to find all possible paths and the shortest path between two nodes.
- JSON response generation for user queries, facilitating integration with frontend applications.

## Getting Started
To run the project on your machine, follow these instructions:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/uznadeem/xml_graph_validator.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd xml_graph_validator
   ```

3. **Set up the database**:
   - Make sure PostgreSQL is installed and running on your machine.
   - Create a new database and import the provided SQL schema.

4. **Install Python dependencies** (assuming you're using Python for this project):
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

### Try using with default file
No need to pass any xml file, just run the following command. It would run all the steps against `sample.xml` file stored at the root directory.

   ```bash
   python main.py
   ```

### Try using with specific file
Want to run it against some specific file? Just pass the file name as follows.
`Disclaimer:` The file needs to be present at github repo.

   ```bash
   python main.py sample.xml
   ```

### Try using with predefined sample files
We have listed a bunch of valid and invalid sample files in `sample_xml_files` directory. You can try the script against any `valid` or `invalid` xml file. You just need to pass the sample file name along with the `sample_xml_files` path as:

   ```bash
   # Examples
   python main.py sample_xml_files/valid_sample_01.xml
   python main.py sample_xml_files/valid_sample_02.xml
   python main.py sample_xml_files/invalid_sample_01.xml
   python main.py sample_xml_files/invalid_sample_02.xml
   ...
   ```

## Test Coverage
We have tested our script against all sample files. You can run the test coverage for the sample files as follows:

   ```bash
   pytest tests/test_main.py
   ```

## Packages

We have used `xml.etree.ElementTree` package for traversing through the xml file as it is the most commonly used built-in package in python. Further,
- It is a part of the built-in standard library.
- It is easy to use.
- It is performance optimal while traversing xml trees.
- Readability.

There are also other external packages like `lxml` and `defusedxml`.

## DB Schema
The db schema is made efficient to handle multiple graphs without interfering with other graphs. We do have 3 different tables as follows:

**Graph**

        id VARCHAR(50) PRIMARY KEY
        name VARCHAR(255) NOT NULL

**Node**

        id VARCHAR(50)
        graph_id VARCHAR(50)
        name VARCHAR(255) NOT NULL
        PRIMARY KEY (id, graph_id)
        FOREIGN KEY (graph_id) REFERENCES graph(id) ON DELETE CASCADE
We have also defined composite primary keys using `id, graph_id` in order to manage multiple graphs in same DB.

**Edge**

        id VARCHAR(50)
        graph_id VARCHAR(50)
        from_node_id VARCHAR(50)
        to_node_id VARCHAR(50)
        cost NUMERIC(10, 2) DEFAULT 0.0
        PRIMARY KEY (id, graph_id)
        FOREIGN KEY (graph_id) REFERENCES graph(id) ON DELETE CASCADE
        FOREIGN KEY (from_node_id, graph_id) REFERENCES nodes(id, graph_id)
        FOREIGN KEY (to_node_id, graph_id) REFERENCES nodes(id, graph_id)
We have also defined composite primary keys using `id, graph_id` in order to manage multiple graphs in same DB.

## Algorithm
The program uses `dijkstra`'s algorithm which is quite fast and efficient when dealing with data structure like graphs and trees to find the shortest distance between 2 points.

**Time Complexity:**
    O(V^2) for the naive implementation.
    O(V + E log V) for more efficient implementations using priority queues.
## Troubleshoots
Upon running the same file multiple times, you would face the duplication errors. You can clean the database for new testing as follows:

1. **Open Python Shell**:
   ```bash
   python
   ```
2. **Run the following commands**:
   ```bash
   from db_handler import clean_data
   clean_data()
   exit()
   ```


### Summary
This project showcases our dedication to efficient data handling and problem-solving. Thank you for exploring this test project, and we look forward to any feedback or insights you might have. Your input is valuable in refining and enhancing our approach to data analysis.

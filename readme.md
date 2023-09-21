## To initialize the app
```bash
$ python -m venv venv
$ ./venv/Scripts/activate
$ pip install -r requirements.txt
```

## Configuration

Set the appropriate settings in `config.py`

```python
INPUTFILE = "map.osm"
DATAFILE = "data.json"
INDEXFILE = "index.json"
```

## Running the app
Edit `main.py`, which is seperated by block comments and comment in or out the operations you wish to perform.

Currently, as-is, a demo run is performed, where the tree is instantiated through bulk loading, and insert, delete and query operations are performed
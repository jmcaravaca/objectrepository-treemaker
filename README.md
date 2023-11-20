# Install packages

`pip install -r requirements.txt`
`pip install -e .`

# Add secret.py

secrey.py with keyvals:

```python
AZURE_PAT = '****'
AZURE_ORG_URL = 'https://dev.azure.com/AutomatizacionRPA'
DBNAME = 'uidata.db'
DBCONNSTRING = f'sqlite:///{DBNAME}'
REPO_BASE_DIRECTORY = 'Repos'
REPO_LIBRARY_DIRECTORY = 'Libraries'
REPO_PROCESS_DIRECTORY = 'Processes'
REPO_OTHER_DIRECTORY = 'Other'
```
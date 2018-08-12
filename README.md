# Research Project
__Using cloud speech recognition in low bandwidth environments__

### Launch Project
1. Clone project

```git clone https://github.com/chezecz/research-project.git```

2. Install dependencies

``` pip install -r requirements.txt```

3. Set enviroment variables

``` FLASK_ENV=development```

``` FLASK_APP=server```

4. Launch Flask server

``` flask run```

**By Default:** Server is located on http://127.0.0.1:5000/ or http://localhost:5000/

5. __(Optional)__ Upload necessary files into *resources* folder
6. Update your ```apiKey.py``` with your Google Cloud API Key
7. Run Client application

``` python3 client.py```

# Research Project
__Using cloud speech recognition in low bandwidth environments__

### Pre-requisite

__portaudio__ package for using ```stream.py```

Install for macOS using Homebrew

```brew install portaudio```

### Launch Project
1. Clone project

```git clone https://github.com/chezecz/research-project.git```

2. Install dependencies

``` pip install -r requirements.txt```

3. Set enviroment variables

``` FLASK_ENV=development```

``` FLASK_APP=server```

__(Optional)__ Google Cloud API key

```export GOOGLE_APPLICATION_CREDENTIALS=$PATH_TO_FILE/api_key.json```

4. Launch Flask server

``` flask run```

**By Default:** Server is located on http://127.0.0.1:5000/ or http://localhost:5000/

5. __(Optional)__ Upload necessary files into *resources* folder
6. Set your Google Cloud API Key

```export GOOGLE_APPLICATION_CREDENTIALS=$PATH_TO_FILE/api_key.json```

7. Run Application

    a. Client application

    ``` python3 client.py [filename] ```

    b. Run Stream Application for recording microphone

    ```python3 stream.py```

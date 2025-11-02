<h1>Py-Agent</h1>

<p> 
This project is a template agent project used to build more complex agents. 
It comes with already basic methods to listed below and a basic project/example.
The API model used for the agent is GeminiAI, that can be swapped out to any another.
The structure is designed to handle single or multiple actions to be executed on the AI tracking its responses and calls. 
</p>

<li> List files and directories</li>
<li> Read file contents</li>
<li> Execute Python files with optional arguments</li>
<li> Write or overwrite files</li>

Key in .env
Google API Key : `https://aistudio.google.com/u/1/apikey`

source : `.venv/bin/active`

This python environment run with the uv<br>
uv run tests.py

packages include: <br>
`uv add google-genai=1.12.1`
`uv add python-dotenv=1.1.0`


FILENAME: deps.md
COMPLETE PATH: ./audit/deps.md
Auteur: Bruno DELNOZ
Email: bruno.delnoz@protonmail.com
Version: v1.0
Date: 2026-02-08 00:26:26

---

# Dependency Inventory

## Declared dependency sources
- `requirements.txt` (pinned versions)
- `Pipfile` (version ranges, Python 3.13 target)

## requirements.txt (verbatim)
```
-i https://pypi.org/simple
aiofiles==25.1.0; python_version >= '3.9'
annotated-doc==0.0.4; python_version >= '3.8'
annotated-types==0.7.0; python_version >= '3.8'
anyio==4.12.1; python_version >= '3.9'
attrs==25.4.0; python_version >= '3.9'
backoff==2.2.1; python_version >= '3.7' and python_version < '4.0'
bcrypt==5.0.0; python_version >= '3.8'
beautifulsoup4==4.14.3; python_full_version >= '3.7.0'
build==1.4.0; python_version >= '3.9'
certifi==2026.1.4; python_version >= '3.7'
cffi==2.0.0; python_version >= '3.9'
charset-normalizer==3.4.4; python_version >= '3.7'
chromadb==1.4.1; python_version >= '3.9'
click==8.3.1; python_version >= '3.10'
coloredlogs==15.0.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'
cryptography==46.0.4; python_version >= '3.8' and python_full_version not in '3.9.0, 3.9.1'
cuda-bindings==12.9.4; platform_system == 'Linux' and platform_machine == 'x86_64'
cuda-pathfinder==1.3.3; python_version >= '3.10'
dataclasses-json==0.6.7; python_version >= '3.7' and python_version < '4.0'
distro==1.9.0; python_version >= '3.6'
durationpy==0.10
emoji==2.15.0; python_version >= '3.8'
fastapi==0.128.4; python_version >= '3.9'
ffmpeg-python==0.2.0
filelock==3.20.3; python_version >= '3.10'
filetype==1.2.0
flatbuffers==25.12.19
fsspec==2026.2.0; python_version >= '3.10'
future==1.0.0; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'
googleapis-common-protos==1.72.0; python_version >= '3.7'
greenlet==3.3.1; python_version >= '3.10'
grpcio==1.78.0; python_version >= '3.9'
h11==0.16.0; python_version >= '3.8'
hf-xet==1.2.0; python_version >= '3.8'
html5lib==1.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'
httpcore==1.0.9; python_version >= '3.8'
httptools==0.7.1; python_version >= '3.9'
httpx==0.28.1; python_version >= '3.8'
huggingface-hub==1.4.1; python_full_version >= '3.9.0'
humanfriendly==10.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'
idna==3.11; python_version >= '3.8'
importlib-metadata==8.7.1; python_version >= '3.9'
importlib-resources==6.5.2; python_version >= '3.9'
jinja2==3.1.6; python_version >= '3.7'
joblib==1.5.3; python_version >= '3.9'
jsonpatch==1.33; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6'
jsonpointer==3.0.0; python_version >= '3.7'
jsonschema==4.26.0; python_version >= '3.10'
jsonschema-specifications==2025.9.1; python_version >= '3.9'
kubernetes==35.0.0; python_version >= '3.6'
langchain==1.2.9; python_full_version >= '3.10.0' and python_full_version < '4.0.0'
langchain-core==1.2.9; python_full_version >= '3.10.0' and python_full_version < '4.0.0'
langdetect==1.0.9
langgraph==1.0.8; python_version >= '3.10'
langgraph-checkpoint==4.0.0; python_version >= '3.10'
langgraph-prebuilt==1.0.7; python_version >= '3.10'
langgraph-sdk==0.3.4; python_version >= '3.10'
langsmith==0.6.9; python_version >= '3.10'
llvmlite==0.46.0; python_version >= '3.10'
lxml==6.0.2; python_version >= '3.8'
markdown==3.10.1; python_version >= '3.10'
markdown-it-py==4.0.0; python_version >= '3.10'
markupsafe==3.0.3; python_version >= '3.9'
marshmallow==3.26.2; python_version >= '3.9'
mdurl==0.1.2; python_version >= '3.7'
mmh3==5.2.0; python_version >= '3.9'
mpmath==1.3.0
mypy-extensions==1.1.0; python_version >= '3.8'
networkx==3.6.1; python_version >= '3.11' and python_full_version != '3.14.1'
nltk==3.9.2; python_version >= '3.9'
numba==0.63.1; python_version >= '3.10'
numpy==1.26.4; python_version >= '3.9'
nvidia-cublas-cu12==12.8.4.1; platform_system == 'Linux' and platform_machine == 'x86_64'
nvidia-cuda-cupti-cu12==12.8.90; platform_system == 'Linux' and platform_machine == 'x86_64'
nvidia-cuda-nvrtc-cu12==12.8.93; platform_system == 'Linux' and platform_machine == 'x86_64'
nvidia-cuda-runtime-cu12==12.8.90; platform_system == 'Linux' and platform_machine == 'x86_64'
nvidia-cudnn-cu12==9.10.2.21; platform_system == 'Linux' and platform_machine == 'x86_64'
nvidia-cufft-cu12==11.3.3.83; platform_system == 'Linux' and platform_machine == 'x86_64'
nvidia-cufile-cu12==1.13.1.3; platform_system == 'Linux' and platform_machine == 'x86_64'
nvidia-curand-cu12==10.3.9.90; platform_system == 'Linux' and platform_machine == 'x86_64'
nvidia-cusolver-cu12==11.7.3.90; platform_system == 'Linux' and platform_machine == 'x86_64'
nvidia-cusparse-cu12==12.5.8.93; platform_system == 'Linux' and platform_machine == 'x86_64'
nvidia-cusparselt-cu12==0.7.1; platform_system == 'Linux' and platform_machine == 'x86_64'
nvidia-nccl-cu12==2.27.5; platform_system == 'Linux' and platform_machine == 'x86_64'
nvidia-nvjitlink-cu12==12.8.93; platform_system == 'Linux' and platform_machine == 'x86_64'
nvidia-nvshmem-cu12==3.4.5; platform_system == 'Linux' and platform_machine == 'x86_64'
nvidia-nvtx-cu12==12.8.90; platform_system == 'Linux' and platform_machine == 'x86_64'
oauthlib==3.3.1; python_version >= '3.8'
olefile==0.47; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'
onnxruntime==1.24.1; python_version >= '3.10'
opentelemetry-api==1.39.1; python_version >= '3.9'
opentelemetry-exporter-otlp-proto-common==1.39.1; python_version >= '3.9'
opentelemetry-exporter-otlp-proto-grpc==1.39.1; python_version >= '3.9'
opentelemetry-proto==1.39.1; python_version >= '3.9'
opentelemetry-sdk==1.39.1; python_version >= '3.9'
opentelemetry-semantic-conventions==0.60b1; python_version >= '3.9'
orjson==3.11.7; python_version >= '3.10'
ormsgpack==1.12.2; python_version >= '3.10'
overrides==7.7.0; python_version >= '3.6'
packaging==26.0; python_version >= '3.8'
pandas==3.0.0; python_version >= '3.11'
pdfminer.six==20251230; python_version >= '3.10'
pdfplumber==0.11.9; python_version >= '3.8'
pillow==12.1.0; python_version >= '3.10'
posthog==5.4.0; python_version >= '3.9'
protobuf==6.33.5; python_version >= '3.9'
psutil==7.2.2; python_version >= '3.6'
pybase64==1.4.3; python_version >= '3.8'
pycparser==3.0; python_version >= '3.10'
pydantic==2.12.5; python_version >= '3.9'
pydantic-core==2.41.5; python_version >= '3.9'
pygments==2.19.2; python_version >= '3.8'
pypdf==6.6.2; python_version >= '3.9'
pypdfium2==5.3.0; python_version >= '3.6'
pypika==0.51.1
pyproject-hooks==1.2.0; python_version >= '3.7'
python-dateutil==2.9.0.post0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'
python-docx==1.2.0; python_version >= '3.9'
python-dotenv==1.2.1; python_version >= '3.9'
python-iso639==2026.1.31; python_version >= '3.10'
python-magic==0.4.27; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'
python-multipart==0.0.22; python_version >= '3.10'
python-oxmsg==0.0.2; python_version >= '3.9'
pyyaml==6.0.3; python_version >= '3.8'
rapidfuzz==3.14.3; python_version >= '3.10'
referencing==0.37.0; python_version >= '3.10'
regex==2026.1.15; python_version >= '3.9'
requests==2.32.5; python_version >= '3.9'
requests-oauthlib==2.0.0; python_version >= '3.4'
requests-toolbelt==1.0.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'
rich==14.3.2; python_full_version >= '3.8.0'
rpds-py==0.30.0; python_version >= '3.10'
safetensors==0.7.0; python_version >= '3.9'
scikit-learn==1.8.0; python_version >= '3.11'
scipy==1.17.0; python_version >= '3.11'
sentence-transformers==5.2.2; python_version >= '3.10'
setuptools==81.0.0; python_version >= '3.12'
shellingham==1.5.4; python_version >= '3.7'
six==1.17.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'
soupsieve==2.8.3; python_version >= '3.9'
sqlalchemy==2.0.46; python_version >= '3.7'
starlette==0.52.1; python_version >= '3.10'
sympy==1.14.0; python_version >= '3.9'
tenacity==9.1.4; python_version >= '3.10'
threadpoolctl==3.6.0; python_version >= '3.9'
tokenizers==0.22.2; python_version >= '3.9'
torch==2.10.0; python_version >= '3.10'
tqdm==4.67.3; python_version >= '3.7'
transformers==5.1.0; python_full_version >= '3.10.0'
triton==3.6.0; platform_system == 'Linux' and platform_machine == 'x86_64'
typer==0.21.1; python_version >= '3.9'
typer-slim==0.21.1; python_version >= '3.9'
typing-extensions==4.15.0; python_version >= '3.9'
typing-inspect==0.9.0
typing-inspection==0.4.2; python_version >= '3.9'
unstructured==0.18.31; python_full_version >= '3.10.0'
unstructured-client==0.42.10; python_full_version >= '3.9.2'
urllib3==2.6.3; python_version >= '3.9'
uuid-utils==0.14.0; python_version >= '3.9'
uvicorn[standard]==0.40.0; python_version >= '3.10'
uvloop==0.22.1; python_full_version >= '3.8.1'
watchfiles==1.1.1; python_version >= '3.9'
webencodings==0.5.1
websocket-client==1.9.0; python_version >= '3.9'
websockets==16.0; python_version >= '3.10'
wrapt==2.1.1; python_version >= '3.9'
xxhash==3.6.0; python_version >= '3.7'
zipp==3.23.0; python_version >= '3.9'
zstandard==0.25.0; python_version >= '3.9'
```

## Pipfile [packages] (verbatim)
```
[packages]
langchain = ">=1.2.8"
chromadb = ">=1.4.1"
python-dotenv = ">=1.2.1"
fastapi = ">=0.95.0"
uvicorn = ">=0.40.0"
sentence-transformers = ">=2.2.2"
torch = "*"
transformers = "*"
aiofiles = ">=25.1.0"
annotated-doc = ">=0.0.4"
annotated-types = ">=0.7.0"
anyio = ">=4.12.1"
attrs = ">=25.4.0"
backoff = ">=2.2.1"
bcrypt = ">=5.0.0"
beautifulsoup4 = ">=4.14.3"
build = ">=1.4.0"
certifi = ">=2026.1.4"
cffi = ">=2.0.0"
charset-normalizer = ">=3.4.4"
click = ">=8.3.1"
coloredlogs = ">=15.0.1"
cryptography = ">=46.0.4"
dataclasses-json = ">=0.6.7"
distro = ">=1.9.0"
durationpy = ">=0.10"
emoji = ">=2.15.0"
filelock = ">=3.20.3"
filetype = ">=1.2.0"
flatbuffers = ">=25.12.19"
fsspec = ">=2026.1.0"
googleapis-common-protos = ">=1.72.0"
greenlet = ">=3.3.1"
grpcio = ">=1.76.0"
h11 = ">=0.16.0"
hf-xet = ">=1.2.0"
html5lib = ">=1.1"
httpcore = ">=1.0.9"
httptools = ">=0.7.1"
httpx = ">=0.28.1"
huggingface-hub = ">=1.4.0"
humanfriendly = ">=10.0"
idna = ">=3.11"
importlib-metadata = ">=8.7.1"
importlib-resources = ">=6.5.2"
joblib = ">=1.5.3"
jsonpatch = ">=1.33"
jsonpointer = ">=3.0.0"
jsonschema = ">=4.26.0"
jsonschema-specifications = ">=2025.9.1"
kubernetes = ">=35.0.0"
langchain-core = ">=1.2.8"
langdetect = ">=1.0.9"
langgraph = ">=1.0.7"
langgraph-checkpoint = ">=4.0.0"
langgraph-prebuilt = ">=1.0.7"
langgraph-sdk = ">=0.3.3"
langsmith = ">=0.6.8"
llvmlite = ">=0.46.0"
lxml = ">=6.0.2"
markdown = ">=3.10.1"
markdown-it-py = ">=4.0.0"
marshmallow = ">=3.26.2"
mdurl = ">=0.1.2"
mmh3 = ">=5.2.0"
mpmath = ">=1.3.0"
mypy-extensions = ">=1.1.0"
nltk = ">=3.9.2"
numba = ">=0.63.1"
numpy = ">=1.24.0,<2.0.0"  # Exemple de plage compatible
oauthlib = ">=3.3.1"
olefile = ">=0.47"
onnxruntime = ">=1.23.2"
opentelemetry-api = ">=1.39.1"
opentelemetry-exporter-otlp-proto-common = ">=1.39.1"
opentelemetry-exporter-otlp-proto-grpc = ">=1.39.1"
opentelemetry-proto = ">=1.39.1"
opentelemetry-sdk = ">=1.39.1"
opentelemetry-semantic-conventions = ">=0.60b1"
orjson = ">=3.11.7"
ormsgpack = ">=1.12.2"
overrides = ">=7.7.0"
packaging = ">=26.0"
pandas = ">=3.0.0"
"pdfminer.six" = ">=20251230"
pdfplumber = ">=0.11.9"
pillow = ">=12.1.0"
posthog = ">=5.4.0"
protobuf = ">=6.33.5"
psutil = ">=7.2.2"
pybase64 = ">=1.4.3"
pycparser = ">=3.0"
pydantic = ">=2.12.5"
pydantic-core = ">=2.41.5"
pygments = ">=2.19.2"
pypdf = "*"
pypdfium2 = ">=5.3.0"
pypika = ">=0.51.1"
pyproject-hooks = ">=1.2.0"
python-dateutil = ">=2.9.0.post0"
python-docx = ">=1.2.0"
python-iso639 = ">=2026.1.31"
python-magic = ">=0.4.27"
python-multipart = ">=0.0.22"
python-oxmsg = ">=0.0.2"
pyyaml = ">=6.0.3"
rapidfuzz = ">=3.14.3"
referencing = ">=0.37.0"
regex = ">=2026.1.15"
requests = ">=2.32.5"
requests-oauthlib = ">=2.0.0"
requests-toolbelt = ">=1.0.0"
rich = ">=14.3.2"
rpds-py = ">=0.30.0"
shellingham = ">=1.5.4"
six = ">=1.17.0"
soupsieve = ">=2.8.3"
sqlalchemy = ">=2.0.46"
starlette = ">=0.50.0"
sympy = ">=1.14.0"
tenacity = ">=9.1.2"
tokenizers = ">=0.22.2"
tqdm = ">=4.67.3"
typer = ">=0.21.1"
typer-slim = ">=0.21.1"
typing-extensions = ">=4.15.0"
typing-inspect = ">=0.9.0"
typing-inspection = ">=0.4.2"
unstructured = ">=0.18.31"
unstructured-client = ">=0.42.10"
urllib3 = ">=2.6.3"
uuid-utils = ">=0.14.0"
uvloop = ">=0.22.1"
watchfiles = ">=1.1.1"
webencodings = ">=0.5.1"
websocket-client = ">=1.9.0"
websockets = ">=16.0"
wrapt = ">=2.1.1"
xxhash = ">=3.6.0"
zipp = ">=3.23.0"
zstandard = ">=0.25.0"
ffmpeg-python = "*"

```

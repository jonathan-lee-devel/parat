# parat
## (Packaging and Release Automation Tool)

## Usage
### With Docker
```shell
docker run --rm parat --help
```
### Without Docker
Make sure to have Python Poetry installed by running the following command:
```shell
pip install poetry
```

Then you must enable a Poetry virtual environment:

```shell
poetry shell
```

Install all the dependencies inside this virtual environment:

 ```shell
poetry install
```

Now run the tool. Example Usage:

```shell
python -m parat --help
```

```shell
python -m parat example-command -v
```

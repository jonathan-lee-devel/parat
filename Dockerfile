FROM python:3.9.4-slim-buster

RUN pip install poetry==1.2.2

# A locale needs to be installed and set for later use by some python packages like click
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Store all of the packages under the /usr/src/app/ directory
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app
COPY poetry.lock pyproject.toml /usr/src/app/

# We turn off virtual env as not needed inside the container
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy the rptrc code into the image
COPY ./pipeline_download_injector /usr/src/app/pipeline_download_injector/

# Run the rptrc
ENTRYPOINT ["python", "-m", "pipeline_download_injector"]

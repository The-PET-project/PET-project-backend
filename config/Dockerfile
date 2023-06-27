FROM python:3.8-slim
EXPOSE 5000

RUN apt-get -y update
RUN apt-get -y install gcc default-libmysqlclient-dev
RUN python -m pip install --upgrade pip
RUN python --version & pip --version

ADD dist/pet_project_backend-0.1.0.tar.gz /tmp/
RUN mkdir /server
WORKDIR /tmp/pet_project_backend-0.1.0
RUN cp -r ./pet_project_backend/ ./setup.py /server/

WORKDIR /server
RUN ls -la ./ && ls -la ./pet_project_backend
RUN pip install -e .

ENV PYTHONPATH=/server/
CMD python ./pet_project_backend/app.py

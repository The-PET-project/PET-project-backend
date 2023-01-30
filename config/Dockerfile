FROM python:3.8
EXPOSE 5000
WORKDIR /server

RUN python -m pip install --upgrade pip
RUN python --version & pip --version

COPY requirements.txt .
RUN cat requirements.txt
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --no-cache-dir -r requirements.txt

ADD dist/pet_project_backend-0.1.0.tar.gz /tmp/
RUN cp -r /tmp/pet_project_backend-0.1.0/pet_project_backend/ /server/
RUN ls -la ./pet_project_backend

ENV PYTHONPATH=/server/
CMD python ./pet_project_backend/app.py

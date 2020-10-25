FROM python:3.8
RUN    apt-get update -y && apt-get install -y \
                    libsnappy-dev
COPY requirements-docker.txt requirements-docker.txt
RUN pip install -r requirements-docker.txt
RUN mkdir /project
COPY scripts_airflow/ /project/scripts/

RUN chmod +x /project/scripts/init.sh
ENTRYPOINT [ "/project/scripts/init.sh" ]
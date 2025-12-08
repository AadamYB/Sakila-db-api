# Ran locally on machine testing a local API server serving Sakila data from mysql
# This file is saved under the local instance of Airflow at ~/airflow/dags/data_pipeline_dag.py
import json
import os
import requests
import pendulum
from airflow.sdk import dag, task
from airflow.providers.standard.operators.bash import BashOperator


@dag(
    dag_id="sakila_data_pipeline",
    schedule=None,
    start_date=pendulum.datetime(2024, 1, 1),
    catchup=False,
)
def sakila_data_pipeline():

    @task()
    def get_data():
        """Fetch actor + film data and save to file."""
        data_path = os.path.expanduser("~/airflow/dags/files/data.json")
        os.makedirs(os.path.dirname(data_path), exist_ok=True)

        url = "http://localhost:8000/api/"

        actors = requests.get(url + "actors/")
        films = requests.get(url + "films/")

        if actors.status_code != 200:
            raise Exception(f"Failed to fetch actors: {actors.status_code}")

        if films.status_code != 200:
            raise Exception(f"Failed to fetch films: {films.status_code}")

        output = {
            "actors": actors.json(),
            "films": films.json(),
        }

        with open(data_path, "w") as f:
            json.dump(output, f)

        print(f"Saved data to {data_path}")
        return data_path

    print_file = BashOperator(
        task_id="print_file",
        bash_command="echo '--- File contents:' && cat {{ ti.xcom_pull(task_ids='get_data') }}",
    )

    @task()
    def process_data(data_path: str):
        with open(data_path, "r") as f:
            data = json.load(f)

        num_actors = len(data["actors"])
        num_films = len(data["films"])

        print(f"Actors retrieved: {num_actors}")
        print(f"Films retrieved: {num_films}")

    data_file = get_data()
    print_file << data_file
    process_data(data_file)


dag = sakila_data_pipeline()

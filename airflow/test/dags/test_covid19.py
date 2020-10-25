def test_task_count(dag_bag):
    dag_id = 'covid19'
    dag = dag_bag.get_dag(dag_id)
    assert len(dag.tasks) == 2


def test_contains_tasks(dag_bag):
    dag_id = 'covid19'
    dag = dag_bag.get_dag(dag_id)
    task_ids = list(map(lambda task: task.task_id, dag.tasks))
    assert sorted(task_ids) == sorted(['ingest_covid19_day', 'transform_covid19_day'])


def test_task_dependency(dag_bag):
    dag_id = 'covid19'
    dag = dag_bag.get_dag(dag_id)
    ingestion_downstream = dag.get_task('ingest_covid19_day').downstream_list[0].task_id
    ingestion_upstream = dag.get_task('ingest_covid19_day').upstream_list
    transformation_downstream = dag.get_task('transform_covid19_day').downstream_list
    transformation_upstream = dag.get_task('transform_covid19_day').upstream_list[0].task_id
    assert ingestion_downstream == 'transform_covid19_day'
    assert ingestion_upstream == []
    assert transformation_downstream == []
    assert transformation_upstream == 'ingest_covid19_day'



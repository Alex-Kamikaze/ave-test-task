from prometheus_client import Counter, Gauge
from prometheus_fastapi_instrumentator.metrics import Info
from app.repository.repo import repository_instance

def total_keys_in_application():
    METRIC = Gauge(
        "total_keys",
        "Total amount of keys stored in the DB"   
    )

    def instrumentation(info: Info):
        total_keys_in_application = repository_instance.get_total_keys()
        METRIC.set(total_keys_in_application)

    return instrumentation
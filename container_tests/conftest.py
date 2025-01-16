import psycopg
import pytest
import requests


@pytest.fixture(scope="session")
def docker_compose_file():
    return "container_tests/docker-compose.yml"


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        return False


def is_db_responsive():
    try:
        conn = psycopg.connect(
            host="localhost",
            port=5432,
            user="testuser",
            password="testpassword",
            dbname="testdb",
        )
        conn.close()
        return True
    except psycopg.OperationalError:
        return False


@pytest.fixture(scope="session")
def web_service_url(docker_ip, docker_services):
    """Get the URL for the web service."""
    port = docker_services.port_for("web", 8000)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    # return url

    return f"http://localhost:{port}"


@pytest.fixture(scope="session")
def db_connection(docker_ip, docker_services):
    """Wait for the database to be ready and return connection info."""

    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_db_responsive()
    )

    return {
        "host": "localhost",
        "port": docker_services.port_for("db", 5432),
        "user": "testuser",
        "password": "testpassword",
        "database": "testdb",
    }

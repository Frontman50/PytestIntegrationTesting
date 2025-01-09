import pytest



@pytest.fixture(scope="session")
def docker_compose_file():
    return "container_tests/docker-compose.yml"


@pytest.fixture(scope="session")
def web_service_url(docker_services):
    """Get the URL for the web service."""
    port = docker_services.port_for("web", 8000)
    return f"http://localhost:{port}"


@pytest.fixture(scope="session")
def db_connection(docker_services):
    """Wait for the database to be ready and return connection info."""
    return {
        "host": "localhost",
        "port": docker_services.port_for("db", 5432),
        "user": "testuser",
        "password": "testpassword",
        "database": "testdb",
    }

import requests
import psycopg

def test_web_service(web_service_url):
    response = requests.get(web_service_url)
    assert response.status_code == 200


def test_db_connection(db_connection):
    with psycopg.connect(
        host=db_connection["host"],
        port=db_connection["port"],
        user=db_connection["user"],
        password=db_connection["password"],
        dbname=db_connection["database"],
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            result = cur.fetchone()
    assert result == (1,)


def test_insert_and_select_user(db_connection):
    # Establish connection
    with psycopg.connect(
            host=db_connection["host"],
            port=db_connection["port"],
            user=db_connection["user"],
            password=db_connection["password"],
            dbname=db_connection["database"],
    ) as conn:
        with conn.cursor() as cur:
            # Create table if it doesn't exist (for testing purposes)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    email VARCHAR(100) UNIQUE
                );
            """)

            # Insert a new user
            cur.execute("""
                INSERT INTO users (name, email) 
                VALUES (%s, %s) 
                RETURNING id, name, email;
            """, ("John Doe", "john.doe@example.com"))
            inserted_user = cur.fetchone()

            # Verify that the user was inserted correctly
            assert inserted_user is not None
            assert inserted_user[1] == "John Doe"
            assert inserted_user[2] == "john.doe@example.com"

            # Fetch the user we just inserted
            cur.execute("""
                SELECT id, name, email FROM users WHERE email = %s;
            """, ("john.doe@example.com",))
            user = cur.fetchone()

            # Verify that the inserted data can be retrieved correctly
            assert user is not None
            assert user[1] == "John Doe"
            assert user[2] == "john.doe@example.com"

            # Clean up - delete the inserted user
            cur.execute("""
                DELETE FROM users WHERE id = %s;
            """, (inserted_user[0],))

            # Verify deletion
            cur.execute("""
                SELECT id FROM users WHERE id = %s;
            """, (inserted_user[0],))
            deleted_user = cur.fetchone()
            assert deleted_user is None
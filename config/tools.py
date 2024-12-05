from dotenv import dotenv_values


def get_env():
    return dotenv_values(".env")

#def get_db():
#    config = get_config()
#    connection_string = config["DATABASE_URL"]
#    client = MongoClient(connection_string)
#    scripts = client.get_database()
#    return scripts

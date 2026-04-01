"""
Flask CLI Command Extensions
"""
from service import app
from service.models import db


######################################################################
# Command to force tables to be rebuilt
# Usage:
#   flask db-create
######################################################################
@app.cli.command("db-create")
def db_create():
    """
    Recreates a local database. You probably should not use this on
    production. ;-)
    """
    print(f"Objeto db utilizado: {db}")
    try:
        print("Ejecutando db.drop_all()")
        db.drop_all()

        print("Ejecutando db.create_all()")
        db.create_all()

        print("Ejecutando db.session.commit()")
        db.session.commit()

        print("Base de datos creada exitosamente.")
    except Exception as e:
        print(f"Error al recrear la base de datos: {e}")
        raise

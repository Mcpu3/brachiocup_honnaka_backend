from sqlalchemy.orm import Session
from typing import Optional
from api.v1 import models, schemas

def create_hello_world(database: Session, new_hello_world: schemas.Helloworld) ->Optional[models.Helloworld]:
    hello_world= models.Helloworld(
        name = new_hello_world.name
    )

    database.add(hello_world)
    database.commit()
    database.refresh(hello_world)

    return hello_world

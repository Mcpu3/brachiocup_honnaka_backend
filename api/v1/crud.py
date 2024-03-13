from typing import Optional

from sqlalchemy.orm import Session

from api.v1 import models, schemas


def read_hello_world(database: Session, hello_world_uuid: str) -> Optional[models.HelloWorld]:
    return database.query(models.HelloWorld).filter(models.HelloWorld.uuid == hello_world_uuid).first()

def create_hello_world(database: Session, new_hello_world: schemas.HelloWorld) -> Optional[models.HelloWorld]:
    hello_world = models.HelloWorld(
        name = new_hello_world.name
    )

    database.add(hello_world)
    database.commit()
    database.refresh(hello_world)

    return hello_world

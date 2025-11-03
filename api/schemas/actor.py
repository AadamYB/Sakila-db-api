from api.models.actor import Actor
from api.schemas import ma

class ActorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Actor

    link = ma.Hyperlinks(
        {
            "href": ma.URLFor(
                'api.actors.read_actor', 
                values=dict(actor_id='<actor_id>', _scheme="http", _external=True)
            )
        }
    )


actor_schema = ActorSchema()
actors_schema = ActorSchema(many=True)
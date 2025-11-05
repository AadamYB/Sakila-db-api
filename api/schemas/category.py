from api.models.category import Category
from api.schemas import ma

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category

    # link = ma.Hyperlinks(
    #     {
    #         "href": ma.URLFor(
    #             'api.categories.read_category', 
    #             values=dict(category_id='<category_id>', _scheme="http", _external=True)
    #         )
    #     }
    # )  


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
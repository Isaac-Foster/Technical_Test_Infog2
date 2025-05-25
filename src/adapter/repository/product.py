from src.adapter.schema import ImageIn
from src.infra.models.image import ImageModel
from src.infra.models.product import ProductModel
from src.adapter.repository.public import BaseRepo
from src.interfaces.schema.product import (
    ProducCreatetSchema,
    ProductSchema,
)


class ProductRepo(BaseRepo):
    def __init__(self):
        super().__init__()
        self.model = ProductModel
        self.image_model = ImageModel
        self.public = ProductSchema

    def create(self, data: ProducCreatetSchema, images: list[ImageIn]):
        already = self.find_all(barcode=data.barcode, name=data.name)

        if already.get('results'):
            return Exception('Client already exists')

        model = self.model(**data.dict())

        with self.session.begin() as session:
            session.add(model)
            session.flush()

            append_images = []

            for image in images:
                image = self.image_model(
                    name=image.name,
                    image=image.image,
                    product=model,
                    product_id=model.id,
                )

                session.add(image)
                session.flush()
                append_images.append(image)

            if append_images:
                model.images = append_images
            session.flush()
            session.refresh(model)
            return self.public.model_validate(model)

    def update(self, id: int, **kwargs):
        # Verifica se o produto existe (via schema)
        existing_schema = self.find(id=id)
        if not existing_schema:
            return Exception('Product not found')

        # Verifica duplicidade (ignorando o próprio item)
        barcode = kwargs.get("barcode")
        name = kwargs.get("name")
        if barcode or name:
            already_results = self.find_all(barcode=barcode, name=name)
            for item in already_results.get("results", []):
                if item.id != id:
                    return Exception("Product already exists")

        with self.session.begin() as session:
            # Recupera o model real do banco
            model = session.get(self.model, id)
            if not model:
                return Exception("Product not found in database")

            # Atualiza apenas os campos válidos fornecidos
            for key, value in kwargs.items():
                if hasattr(model, key) and value not in ("", None):
                    setattr(model, key, value)

            session.flush()
            session.refresh(model)

            return self.public.model_validate(model)



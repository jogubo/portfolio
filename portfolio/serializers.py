class Serializer():

    def list(self, objects: list) -> dict:
        data = {
            'count': len(objects),
            'results': [self.preview(object) for object in objects],
        }
        return data


class UserSerializer(Serializer):

    @staticmethod
    def preview(object: object) -> dict:
        data = {
            'id': object.id,
            'username': object.username,
        }
        return data

    @staticmethod
    def detail(object: object) -> dict:
        data = {
            'id': object.id,
            'username': object.username,
        }
        return data


class CategorySerializer(Serializer):

    @staticmethod
    def preview(object: object) -> dict:
        data = {
            'id': object.id,
            'name': object.name,
            'name_url': object.name_url,
            'hidden': object.hidden,
        }
        return data

    @staticmethod
    def detail(object: object) -> dict:
        data = {
            'id': object.id,
            'name': object.name,
            'name_url': object.name_url,
            'pictures': PicturesSerializer.list(objects=object.pictures),
            'hidden': object.hidden
        }
        return data


class PicturesSerializer(Serializer):

    @staticmethod
    def preview(object: object) -> dict:
        data = {
            'id': object.id,
            'title': object.title,
            'url': object.url,
            'category': object.category.id
        }
        return data

    @staticmethod
    def detail(object: object) -> dict:
        data = {
            'id': object.id,
            'title': object.title,
            'description': object.description,
            'filename': object.filename,
            'url': object.url,
            'category': CategorySerializer.preview(object=object.category)
        }
        return data

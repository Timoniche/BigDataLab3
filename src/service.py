from database import Database
from repository.image_predictions_dao import ImagePredictionsDAO


class Service:
    def __init__(self, db: Database):
        self.imagedao = ImagePredictionsDAO(db)

    def init_db(self):
        self.imagedao.init_table()

    def save_image_prediction(
            self,
            image_name: str,
            is_male: bool,
    ):
        self.imagedao.insert_image_predictions(
            image_name=image_name,
            is_male=is_male,
        )

    def get_image_male(
            self,
            image_name: str,
    ):
        return self.imagedao.select_image_predictions(
            image_name=image_name,
        )

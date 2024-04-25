from database import Database
from logger import Logger


class ImagePredictionsDAO:
    def __init__(self, db: Database):
        logger = Logger(show=True)
        self.log = logger.get_logger(__name__)
        self.db = db

    def init_table(self):
        self.log.info('Initializing image_prediction table')
        self.db.execute(
            '''
            CREATE TABLE IF NOT EXISTS image_predictions (
                filename TEXT NOT NULL PRIMARY KEY,
                is_male BOOLEAN NOT NULL
            )
            '''
        )

    def insert_image_predictions(
            self,
            image_name: str,
            is_male: bool,
    ):
        self.db.execute(
            '''
            INSERT INTO image_predictions (filename, is_male) VALUES 
                (%s, %s)
            ''',
            args=(image_name, is_male)
        )

    def select_image_predictions(
            self,
            image_name: str,
    ):
        return self.db.execute(
            '''
            SELECT is_male FROM image_predictions WHERE filename = %s
            ''',
            args=(image_name,)
        )

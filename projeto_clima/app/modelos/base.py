from abc import ABC, abstractmethod
from datetime import datetime
import pandas as pd

class DataPoint(ABC):
    def __init__(self, fonte:str):
        self.fonte = fonte
        self.timestamp = datetime.now()

    @abstractmethod
    def para_df(self) -> pd.DataFrame:
        pass

    def dict(self) -> dict:
        return {

            'fonte':self.fonte ,
            'timestamp': self.timestamp.isoformat()

        }
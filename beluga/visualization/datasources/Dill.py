from beluga.visualization.datasources import BaseDataSource
import dill
import logging

class Dill(BaseDataSource):
    valid_exts = ['dill']
    def __init__(self, filename = 'data.dill'):
        """
        Initializes the data source with supplied filename
        """
        self.is_loaded = False
        self.filename = filename

    def load(self):
        """
        Loads solution data using dill
        """
        with open(self.filename,'rb') as f:
            logging.info("Loading datafile "+self.filename+"...")
            self._data = dill.load(f)
            if 'solution' not in self._data:
                self.is_loaded = False
                logging.error("Solution missing in data file :"+self.filename)
                raise RuntimeError("Solution missing in data file :"+self.filename)
            if 'problem_data' not in self._data:
                self.is_loaded = False
                logging.error("Problem data missing in data file :"+self.filename)
                raise RuntimeError("Problem data missing in data file :"+self.filename)

            logging.info("Loaded "+str(len(self._data['solution']))+" solution sets from "+self.filename)
            self.is_loaded = True

    def get_problem(self):
        """
        Return problem data
        """
        if not self.is_loaded:
            logging.error("Data source should be loaded before being used")
            raise RuntimeError("Data source should be loaded before being used")
        return self._data['problem_data']


    def get_solution(self):
        """
        Returns solution array
        """
        if not self.is_loaded:
            logging.error("Data source should be loaded before being used")
            raise RuntimeError("Data source should be loaded before being used")
        return self._data['solution']

import logging
import os
from dataclasses import dataclass

from src.cleaners.local_cleaner import LocalCleaner
from src.dataloaders.csv_dataloader import PandasDataloader
from src.dataloaders.dill_dataloader import LocalTimeSeriesDillDataloader
from clearml import Task


@dataclass
class CleanCommand:
    cleaner: LocalCleaner
    dataset_path: str
    output_folder: str
    logger = logging.getLogger(__name__)

    def __post_init__(self):
        os.makedirs(self.output_folder, exist_ok=True)

    def run(self):
        task = Task.init(project_name='BRGM', task_name='local cleaning')
        task.connect({
            'dataset_path': self.dataset_path,
            'output_folder': self.output_folder,
            'min_date': self.cleaner.min_date,
            'max_date': self.cleaner.max_date
        })

        output_filename = self.cleaner.generate_file_name()
        data = PandasDataloader(self.dataset_path, sep=";").load()
        data = self.cleaner.clean(data)

        LocalTimeSeriesDillDataloader.save(data, os.path.join(self.output_folder, output_filename))



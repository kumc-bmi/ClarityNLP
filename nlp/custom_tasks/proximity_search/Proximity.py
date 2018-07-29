from tasks.task_utilities import BaseTask
from pymongo import MongoClient
import util

try:
    from .proximity_txt import get_proximity_txt
    from .proximity_phrase import get_proximity_phrase
except Exception as e:
    from proximity_txt import get_proximity_txt
    from proximity_phrase import get_proximity_phrase


class Proximity(BaseTask):
    task_name = "Proximity"

    def run_custom_task(self, temp_file, mongo_client: MongoClient):
        for doc in self.docs:
            txt = self.get_document_text(doc)

            # My custom stuff here
            length = len(txt)
            if length > 0:
                if self.pipeline_config.custom_arguments['order'] == 'false':
                    self.pipeline_config.custom_arguments['order'] = False
                else:
                    self.pipeline_config.custom_arguments['order']= True
                obj = dict()
                if get_proximity_txt(txt,self.pipeline_config.custom_arguments['word1'], self.pipeline_config.custom_arguments['word2'], int(self.pipeline_config.custom_arguments['number']), self.pipeline_config.custom_arguments['order']):
                    obj['doc'] = txt
                    phrase = get_proximity_phrase(txt,self.pipeline_config.custom_arguments['word1'], self.pipeline_config.custom_arguments['word2'], int(self.pipeline_config.custom_arguments['number']), self.pipeline_config.custom_arguments['order'])
                    obj['phrase'] = phrase


                # writing results
                self.write_result_data(temp_file, mongo_client, doc, obj)

                # writing to log
                self.write_log_data("Proximity_positive docs and phrases", "done writing data")

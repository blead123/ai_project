from dataclasses import dataclass
import datetime

datetime_format = '%y-%m-%d-%H-%M-%S'

@dataclass
class Record:
    started_at: datetime.datetime # unix time from time.time()
    ended_at: datetime.datetime

    def to_csv(self):
        return f'{self.started_at.strftime(datetime_format)},{self.ended_at.strftime(datetime_format)}'

class RecordModule:
    def __init__(self, save_file_path):
        assert save_file_path is not None

        self.save_file_path = save_file_path
        self.records = []

    def load(self):
        self.records = []

        with open(self.save_file_path, 'r') as f:
            lines = f.readlines()

            assert lines is not None

            self.records = [*map(lambda line: datetime.datetime.strptime(line, datetime_format), lines)]

    def save(self):
        raw_text = '\n'.join([*map(lambda x: x.to_csv(), self.records)])

        assert len(raw_text) > 0

        with open(self.save_file_path, 'w') as f:
            f.write(raw_text)

    '''
        @param record Record
        @return None
    '''
    def append_record(self, record):
        self.records.append(record)

    '''
        @returns List<Record> by descending order
    '''
    def get_records(self):
        return [*self.records]


# Usage
'''py
record_module = RecordModule('F:/savefile.csv') # 변수 선언

# 기록하기
record_module.append(Record(<started_at>, <ended_at>))
record_module.append(Record(<started_at>, <ended_at>))

record_module.save() # 저장

record_module.load() # 불러오기
'''
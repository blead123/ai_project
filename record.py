from dataclasses import dataclass
from datetime import *

datetime_format = r'%Y-%m-%d-%H-%M-%S'

@dataclass
class Record:
    started_at: datetime # unix time from time.time() dataclass의 인스턴스 변수
    ended_at: datetime

    def to_csv(self):
        return f'{self.started_at.strftime(datetime_format)},{self.ended_at.strftime(datetime_format)}'

    def studied_time(self):
        delta = (self.ended_at - self.started_at)

        hour = delta.seconds // 3600
        minute = (delta.seconds % 3600) // 60
        second = delta.seconds % 60

        return delta, (hour, minute, second)

class RecordManager:
    def __init__(self, save_file_path):
        assert save_file_path is not None

        self.save_file_path = save_file_path
        self.records = []

    def load(self):
        self.records = []

        with open(self.save_file_path, 'r') as f:
            self.records = []

            for line in f.readlines():
                start, end = line.split(',')
                record = Record(datetime.strptime(start, datetime_format), datetime.strptime(end, datetime_format))

                self.records.append(record)

    def save(self):
        raw_text = '\n'.join([*map(lambda x: x.to_csv(), self.records)])

        # [1, 2, 3, 4, 5...] -> 1, 2, 3, 4, 5...

        assert len(raw_text) > 0

        with open(self.save_file_path, 'w') as f:
            f.write(raw_text)

    '''
        @param record Record
        @return None
    '''
    def append_record(self, record: Record):
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
record = RecordManager('./file.csv')
record.append_record(Record(datetime(2021, 1, 1, 16), datetime(2021, 1, 1, 17))) # 16시부터 17시 까지
record.save()
record.load()
print(record.get_records())
from dorian_assessment.enum import BaseEnum


class LOBEnum(BaseEnum):
    ALL_OTHER_MISCELLANEOUS = ('All Other miscellaneous', 'All Other miscellaneous')
    AVIATION = ('Aviation', 'Aviation')
    CREDIT_GUARANTEE = ('Credit Guarantee', 'Credit Guarantee')
    CROP_INSURANCE = ('Crop Insurance', 'Crop Insurance')
    ENGINEERING = ('Engineering', 'Engineering')
    FIRE = ('Fire', 'Fire')
    HEALTH_GOVERNMENT_SCHEMES = ('Health-Government schemes', 'Health-Government schemes')
    HEALTH_GROUP = ('Health-Group', 'Health-Group')
    HEALTH_RETAIL = ('Health-Retail', 'Health-Retail')
    MARINE_CARGO = ('Marine Cargo', 'Marine Cargo')
    MARINE_HULL = ('Marine Hull', 'Marine Hull')
    MOTOR_OD = ('Motor OD', 'Motor OD')
    MOTOR_TP = ('Motor TP', 'Motor TP')
    OVERSEAS_MEDICAL = ('Overseas Medical', 'Overseas Medical')
    PA = ('P.A. ', 'P.A. ')


class FileUploadStatusEnum(BaseEnum):
    INITIATED = ('Initiated', ('initiated',))
    PROCESSING = ('Processing', ('processing',))
    SUCCESS = ('Success', ('success',))
    FAILED = ('Failed', ('failed',))

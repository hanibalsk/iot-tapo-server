from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def get_database_engine(db_name="iot_devices.db"):
    return create_engine(f'sqlite:///{db_name}')

class IoTDevice(Base):
    __tablename__ = 'iot_devices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String, nullable=False, index=True)
    mac = Column(String)
    state = Column(String)
    avatar = Column(String)
    device_id = Column(String)
    device_on = Column(Boolean)
    fw_id = Column(String)
    fw_ver = Column(String)
    has_set_location_info = Column(Boolean)
    hw_id = Column(String)
    hw_ver = Column(String)
    lang = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    model = Column(String)
    nickname = Column(String, index=True)
    oem_id = Column(String)
    on_time = Column(Integer)
    region = Column(String)
    rssi = Column(Integer)
    signal_level = Column(Integer)
    specs = Column(String)
    ssid = Column(String)
    time_diff = Column(Integer)
    device_type = Column(String)

    __table_args__ = (
        Index('ix_ip', 'ip'),
        Index('ix_nickname', 'nickname'),
    )

class IoTDeviceDatabase:
    def __init__(self, db_name="iot_devices.db"):
        self.engine = get_database_engine(db_name)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_device(self, device_data):
        session = self.Session()
        try:
            device = IoTDevice(**device_data)
            session.add(device)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_all_devices(self, page=1, page_size=10, filters=None):
        session = self.Session()
        try:
            query = session.query(IoTDevice)

            # Apply filters if provided
            if filters:
                for attr, value in filters.items():
                    query = query.filter(getattr(IoTDevice, attr) == value)

            # Apply pagination
            offset = (page - 1) * page_size
            return query.offset(offset).limit(page_size).all()
        finally:
            session.close()

    def get_device_by_ip(self, ip):
        session = self.Session()
        try:
            return session.query(IoTDevice).filter_by(ip=ip).first()
        finally:
            session.close()

    def update_device(self, device_id, update_fields):
        session = self.Session()
        try:
            session.query(IoTDevice).filter_by(id=device_id).update(update_fields)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_device(self, device_id):
        session = self.Session()
        try:
            session.query(IoTDevice).filter_by(id=device_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

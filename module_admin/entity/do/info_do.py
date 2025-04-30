from sqlalchemy import Column, CHAR, Integer, String, DateTime
from config.database import Base


class SshInfo(Base):
    """
    服务器表
    """

    __tablename__ = 'ssh_info'
    __table_args__ = ({'comment': '服务器表'})

    ssh_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='服务器ID')
    ssh_name = Column(String(10), nullable=False, comment='服务器名称')
    ssh_host = Column(String(512), nullable=False, comment='服务器地址')
    ssh_username = Column(String(512), nullable=True, comment='服务器用户名')
    ssh_password = Column(String(512), nullable=True, comment='服务器密码')
    ssh_port = Column(Integer, nullable=True, comment='服务器端口')
    create_by = Column(String(64), nullable=True, comment='创建者')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(64), nullable=True, comment='更新者')
    update_time = Column(DateTime, nullable=True, comment='更新时间')
    remark = Column(String(100), nullable=True, comment='备注')
    del_flag = Column(CHAR(1), nullable=True, comment='删除标志（0代表存在 2代表删除）')




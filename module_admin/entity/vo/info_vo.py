from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query


class InfoModel(BaseModel):
    """
    服务器表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    ssh_id: Optional[int] = Field(default=None, description='服务器D')
    ssh_name: Optional[str] = Field(default=None, description='服务器名称')
    ssh_host: Optional[str] = Field(default=None, description='服务器地址')
    ssh_username: Optional[str] = Field(default=None, description='服务器用户名')
    ssh_password: Optional[str] = Field(default=None, description='服务器密码')
    ssh_port: Optional[int] = Field(default=None, description='服务器端口')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    del_flag: Optional[str] = Field(default=None, description='删除标志（0代表存在 2代表删除）')

    @NotBlank(field_name='ssh_name', message='服务器名称不能为空')
    def get_ssh_name(self):
        return self.ssh_name

    @NotBlank(field_name='ssh_host', message='服务器地址不能为空')
    def get_ssh_host(self):
        return self.ssh_host

    def validate_fields(self):
        self.get_ssh_name()
        self.get_ssh_host()


class InfoQueryModel(InfoModel):
    """
    服务器不分页查询模型
    """
    pass


@as_query
class InfoPageQueryModel(InfoQueryModel):
    """
    服务器分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteInfoModel(BaseModel):
    """
    删除服务器模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ssh_ids: str = Field(description='需要删除的服务器D')

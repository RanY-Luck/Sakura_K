# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time    : 2024/8/29 10:54
# # @Author  : 冉勇
# # @Site    :
# # @File    : vo_generate.py
# # @Software: PyCharm
# # @desc    : 生成 xx_vo.py
import sys
from typing import Type
import inspect
from sqlalchemy import inspect as model_inspect
from pathlib import Path
from config.database import Base
from scripts.crud_generate.utils.schema import SchemaField
from sqlalchemy.sql.schema import Column as ColumnType
from scripts.crud_generate.utils.generate_base import GenerateBase


class VoGenerate(GenerateBase):
    BASE_FIELDS = ["id", "create_datetime", "update_datetime"]

    def __init__(
            self,
            model: Type[Base],
            zh_name: str,
            en_name: str,
            vo_file_path: Path,
            vo_dir_path: Path,
            vo_base_class_name: str,
            vo_query_class_name: str,  # 不分页查询模型
            vo_page_query_class_name: str,  # 分页查询模型
            vo_delete_class_name: str  # 删除模型

    ):
        """
        初始化工作
        :param model: 提前定义好的 ORM 模型
        :param zh_name: 功能中文名称，主要用于描述、注释
        :param en_name: 功能英文名称，主要用于 schema、param 文件命名，以及它们的 class 命名，dal、url 命名，默认使用 model class
        en_name 例子：
            如果 en_name 由多个单词组成那么请使用 _ 下划线拼接
            在命名文件名称时，会执行使用 _ 下划线名称
            在命名 class 名称时，会将下划线名称转换为大驼峰命名（CamelCase）
            在命名 url 时，会将下划线转换为 /
        :param vo_file_path: vo 文件的地址
        :param vo_dir_path: vo 文件的 app 路径
        :param vo_base_class_name: 基础类
        :param vo_query_class_name: 不分页查询模型
        :param vo_page_query_class_name: 分页查询模型
        :param vo_delete_class_name: 删除模型
        """
        self.model = model
        self.zh_name = zh_name
        self.en_name = en_name
        self.vo_file_path = vo_file_path
        self.vo_dir_path = vo_dir_path
        self.vo_base_class_name = vo_base_class_name
        self.vo_query_class_name = vo_query_class_name
        self.vo_page_query_class_name = vo_page_query_class_name
        self.vo_delete_class_name = vo_delete_class_name

    def write_generate_code(self):
        """
        生成 vo 文件，以及代码内容
        :return:
        """
        self.vo_file_path.parent.mkdir(parents=True, exist_ok=True)
        if self.vo_file_path.exists():
            # 存在则直接删除，重新创建写入
            self.vo_file_path.unlink()
        self.vo_file_path.touch()

        code = self.generate_code()
        self.vo_file_path.write_text(code, "utf-8")
        print(f"===========================vo 代码创建完成=================================")

    def generate_code(self) -> str:
        """
        生成 vo 代码内容
        :return:
        """
        fields = []
        mapper = model_inspect(self.model)
        for attr_name, column_property in mapper.column_attrs.items():
            if attr_name in self.BASE_FIELDS:
                continue
            # 假设它是单列属性
            column: ColumnType = column_property.columns[0]
            item = SchemaField(
                name=attr_name,
                field_type=column.type.python_type.__name__,
                nullable=column.nullable,
                default=column.default.__dict__.get("arg", None) if column.default else None,
                title=column.comment,
                max_length=column.type.__dict__.get("length", None)
            )
            fields.append(item)

        code = self.generate_file_desc(self.vo_file_path.name, desc=f"{self.zh_name}--pydantic模型")

        modules = {
            "datetime": ["datetime"],
            "pydantic": ['BaseModel', 'ConfigDict', 'Field', 'model_validator'],
            "pydantic.alias_generators": ['to_camel'],
            "pydantic_validation_decorator": ['NotBlank', 'Size', 'Pattern', 'Xss'],
            "typing": ['Literal', 'Optional', 'Union', 'List'],
            "module_admin.annotation.pydantic_annotation": ['as_form,as_query'],
        }
        code += self.generate_modules_code(modules)
        base_schema_code = f"\n\nclass {self.vo_base_class_name}:"
        for item in fields:
            field = f"\n\t{item.name}: Optional[{item.field_type}] {'' if item.nullable else ''}"
            default = None
            if item.default is not None:
                if item.field_type == "str":
                    default = f"\"{item.default}\""
                else:
                    default = item.default
            elif default is None and not item.nullable:
                default = "None"
            # 对所有字段统一使用 None 作为默认值
            if item.title == "创建时间" or item.title == "更新时间":
                field += f"= Field(default=None, description=\"{item.title}\")"
            else:
                field += f"= Field(default={default}, description=\"{item.title}\")"
            base_schema_code += field
        base_schema_code += "\n"
        code += base_schema_code

        # 不分页查询模型
        base_query_code = f"\n\nclass {self.vo_query_class_name}({self.vo_base_class_name}):"
        base_query_code += f'''
    """
    {self.zh_name}不分页查询模型
    """
                '''
        base_query_code += f"\n\tbegin_time: Optional[str] = Field(default=None, description=\"开始时间\")"
        base_query_code += "\n\tend_time: Optional[str] = Field(default=None, description=\"结束时间\")"
        base_query_code += "\n"
        code += base_query_code

        # 分页查询模型
        base_page_query_code = '''\n\n@as_query\n@as_form'''
        base_page_query_code += f"\nclass {self.vo_page_query_class_name}({self.vo_base_class_name}):"
        base_page_query_code += f'''
    """
    {self.zh_name}分页查询模型
    """
                '''
        base_page_query_code += f"\n\tpage_num: int = Field(default=1, description=\"当前页码\")"
        base_page_query_code += "\n\tpage_size: int = Field(default=10, description=\"每页记录数\")"
        base_page_query_code += "\n"
        code += base_page_query_code

        # 删除模型
        base_delete_code = f"\n\nclass {self.vo_delete_class_name}(BaseModel):"
        base_delete_code += f'''
    """
    删除{self.zh_name}模型
    """
                '''
        base_delete_code += "\n\tmodel_config = ConfigDict(alias_generator=to_camel)\n"
        base_delete_code += "\n\t# 需要xx自行修改：比如我有上面 pydantic 有个 dept_id, 那么这里就改成 dept_ids)"
        base_delete_code += f"\n\t{self.en_name}_ids: str = Field(description='需要删除的{self.en_name}_id')"
        base_delete_code += f"\n\tupdate_by: Optional[str] = Field(default=None, description=\"更新者\")"
        base_delete_code += "\n\tupdate_time: Optional[str] = Field(default=None, description=\"更新时间\")"
        base_delete_code += "\n"
        code += base_delete_code
        return code.replace("\t", "    ")

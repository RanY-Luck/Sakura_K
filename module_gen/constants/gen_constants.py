#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/8 9:49
# @Author   : 冉勇
# @File     : gen_constants.py
# @Software : PyCharm
# @Desc     : 代码生成通用常量
class GenConstants:
    """代码生成通用常量"""

    # 单表（增删改查）
    TPL_CRUD = "crud"

    # 树表（增删改查）
    TPL_TREE = "tree"

    # 主子表（增删改查）
    TPL_SUB = "sub"

    # 树编码字段
    TREE_CODE = "treeCode"

    # 树父编码字段
    TREE_PARENT_CODE = "treeParentCode"

    # 树名称字段
    TREE_NAME = "treeName"

    # 上级菜单ID字段
    PARENT_MENU_ID = "parentMenuId"

    # 上级菜单名称字段
    PARENT_MENU_NAME = "parentMenuName"

    # 数据库字符串类型
    TYPE_STRING = ["char", "varchar", "nvarchar", "varchar2"]

    # 数据库文本类型
    TYPE_TEXT = ["tinytext", "text", "mediumtext", "longtext"]

    # 数据库时间类型
    TYPE_DATE_TIME = ["datetime", "time", "date", "timestamp"]

    # 数据库数字类型
    TYPE_NUMBER = ["tinyint", "smallint", "mediumint", "int", "number", "integer",
                   "bigint", "float", "float", "double", "decimal"]

    # 页面不需要编辑字段
    COLUMN_NAME_NOT_EDIT = ["id", "create_by", "create_time", "del_flag", "update_time"]

    # 页面不需要显示的列表字段
    COLUMN_NAME_NOT_LIST = ["id", "create_by", "create_time", "del_flag", "update_by"]

    # 页面不需要查询字段
    COLUMN_NAME_NOT_QUERY = ["id", "create_by", "create_time", "del_flag", "update_by",
                             "update_time", "remark"]

    # Entity基类字段
    BASE_ENTITY = ["createBy", "createTime", "updateBy", "updateTime", "remark"]

    # Tree基类字段
    TREE_ENTITY = ["parentName", "parentId", "orderNum", "ancestors"]

    # 文本框
    HTML_INPUT = "input"

    # 文本域
    HTML_TEXTAREA = "textarea"

    # 下拉框
    HTML_SELECT = "select"

    # 单选框
    HTML_RADIO = "radio"

    # 复选框
    HTML_CHECKBOX = "checkbox"

    # 日期控件
    HTML_DATETIME = "datetime"

    # 图片上传控件
    HTML_IMAGE_UPLOAD = "imageUpload"

    # 文件上传控件
    HTML_FILE_UPLOAD = "fileUpload"

    # 富文本控件
    HTML_EDITOR = "editor"

    # 模糊查询
    QUERY_LIKE = "LIKE"

    # 相等查询
    QUERY_EQ = "EQ"

    # 需要
    REQUIRE = "1"

    # MySQL -> SQLAlchemy 类型映射
    MYSQL_TO_SQLALCHEMY = {
        # Numeric Types
        "TINYINT": "SmallInteger",
        "SMALLINT": "SmallInteger",
        "MEDIUMINT": "Integer",
        "INT": "Integer",
        "INTEGER": "Integer",
        "BIGINT": "BigInteger",
        "FLOAT": "Float",
        "DOUBLE": "Float",
        "DECIMAL": "Numeric",
        "NUMERIC": "Numeric",

        # String Types
        "CHAR": "String",
        "VARCHAR": "String",
        "TEXT": "Text",
        "TINYTEXT": "Text",
        "MEDIUMTEXT": "Text",
        "LONGTEXT": "Text",
        "BLOB": "LargeBinary",
        "TINYBLOB": "LargeBinary",
        "MEDIUMBLOB": "LargeBinary",
        "LONGBLOB": "LargeBinary",

        # Date and Time Types
        "DATE": "Date",
        "DATETIME": "DateTime",
        "TIMESTAMP": "DateTime",
        "TIME": "Time",
        "YEAR": "Integer",  # MySQL YEAR type is commonly represented as Integer in SQLAlchemy

        # Binary Types
        "BINARY": "Binary",
        "VARBINARY": "Binary",

        # Enum and Set Types
        "ENUM": "Enum",
        "SET": "Enum",  # Set can be represented using Enum type in SQLAlchemy

        # JSON Types
        "JSON": "JSON",  # SQLAlchemy supports JSON type from 1.3.0 version

        # Spatial Types (less common in typical usage)
        "GEOMETRY": "String",  # Can be represented as String or Binary
        "POINT": "String",  # Represented as String in SQLAlchemy
        "LINESTRING": "String",  # Represented as String in SQLAlchemy
        "POLYGON": "String",  # Represented as String in SQLAlchemy

        # Other Types
        "BIT": "Boolean",
        "BOOL": "Boolean",
        "UUID": "String",  # UUIDs in SQLAlchemy can be represented as String
        "BINARY": "Binary",  # MySQL BINARY type corresponds to SQLAlchemy's Binary
    }

    MYSQL_TO_PYTHON = {
        # 字符串类型
        "VARCHAR": "str",
        "CHAR": "str",
        "TEXT": "str",
        "TINYTEXT": "str",
        "MEDIUMTEXT": "str",
        "LONGTEXT": "str",
        # 数值类型
        "INT": "int",
        "TINYINT": "int",
        "SMALLINT": "int",
        "MEDIUMINT": "int",
        "BIGINT": "int",
        "FLOAT": "float",
        "DOUBLE": "float",
        "DECIMAL": "float",
        "NUMERIC": "float",
        "BIT": "bool",  # 位字段，0 或 1
        # 日期和时间类型
        "DATETIME": "datetime",
        "TIMESTAMP": "datetime",
        "DATE": "datetime.date",
        "TIME": "datetime.time",
        "YEAR": "int",  # 存储年份
        "TINYINT UNSIGNED": "int",  # 无符号小整数类型
        # 布尔类型
        "BOOLEAN": "bool",
        "BOOL": "bool",  # 布尔类型，通常与 BOOLEAN 相同
        # JSON 数据类型
        "JSON": "dict",  # JSON 数据存储为字典
        # 二进制类型
        "BLOB": "bytes",
        "TINYBLOB": "bytes",
        "MEDIUMBLOB": "bytes",
        "LONGBLOB": "bytes",
        # 枚举和集合类型
        "ENUM": "str",  # 枚举类型作为字符串
        "SET": "list",  # 集合类型作为列表
        # 时间单位类型
        "DATE": "datetime.date",  # 仅日期
        "TIME": "datetime.time",  # 仅时间
        # 大文本类型
        "LONGTEXT": "str",
        "MEDIUMTEXT": "str",
        "TINYTEXT": "str",
        # UUID
        "UUID": "str",  # UUID 一般作为字符串
        # 用于二进制数据
        "BINARY": "bytes",  # 固定长度的二进制数据
        "VARBINARY": "bytes",  # 可变长度的二进制数据
        # 其他数据类型
        "GEOMETRY": "bytes",  # 空间数据类型，通常存储为字节流
        "POINT": "bytes",  # 点数据类型
        "LINESTRING": "bytes",  # 线数据类型
        "POLYGON": "bytes",  # 多边形数据类型
        "MULTIPOINT": "bytes",  # 多点数据类型
        "MULTILINESTRING": "bytes",  # 多线数据类型
        "MULTIPOLYGON": "bytes",  # 多多边形数据类型
        "GEOMETRYCOLLECTION": "bytes",  # 几何集合类型
    }

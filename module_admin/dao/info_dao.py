from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.info_do import SshInfo
from module_admin.entity.vo.info_vo import InfoModel, InfoPageQueryModel
from utils.page_util import PageUtil


class InfoDao:
    """
    环境模块数据库操作层
    """

    @classmethod
    async def get_info_detail_by_id(cls, db: AsyncSession, ssh_id: int):
        """
        根据服务器D获取环境详细信息

        :param db: orm对象
        :param ssh_id: 服务器D
        :return: 环境信息对象
        """
        info_info = (
            (
                await db.execute(
                    select(SshInfo)
                    .where(
                        SshInfo.ssh_id == ssh_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return info_info

    @classmethod
    async def get_info_detail_by_info(cls, db: AsyncSession, info: InfoModel):
        """
        根据环境参数获取环境信息

        :param db: orm对象
        :param info: 环境参数对象
        :return: 环境信息对象
        """
        info_info = (
            (
                await db.execute(
                    select(SshInfo).where(
                        SshInfo.ssh_name == info.ssh_name
                    )
                )
            )
            .scalars()
            .first()
        )

        return info_info

    @classmethod
    async def get_info_list(cls, db: AsyncSession, query_object: InfoPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取环境列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 环境列表信息对象
        """
        query = (
            select(SshInfo)
            .where(
            )
            .order_by(SshInfo.ssh_id)
            .distinct()
        )
        info_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return info_list

    @classmethod
    async def add_info_dao(cls, db: AsyncSession, info: InfoModel):
        """
        新增环境数据库操作

        :param db: orm对象
        :param info: 环境对象
        :return:
        """
        db_info = SshInfo(**info.model_dump(exclude={}))
        db.add(db_info)
        await db.flush()

        return db_info

    @classmethod
    async def edit_info_dao(cls, db: AsyncSession, info: dict):
        """
        编辑环境数据库操作

        :param db: orm对象
        :param info: 需要更新的环境字典
        :return:
        """
        ssh_id = info.get('ssh_id')
        if ssh_id:
            await db.execute(
                update(SshInfo)
                .where(SshInfo.ssh_id == ssh_id)
                .values(**info)
            )
        else:
            raise ValueError("Missing ssh_id for update operation")

    @classmethod
    async def delete_info_dao(cls, db: AsyncSession, info: InfoModel):
        """
        删除环境数据库操作

        :param db: orm对象
        :param info: 环境对象
        :return:
        """
        await db.execute(delete(SshInfo).where(SshInfo.ssh_id.in_([info.ssh_id])))


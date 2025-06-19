import logging
import json
from app import vn
from datetime import datetime
from typing import List, Dict

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VannaTrainer:
    """Vanna AI SQL 助手训练器"""

    def __init__(self, vn_instance):
        self.vn = vn_instance
        self.training_log = []

    def save_training_log(self, filename: str = None):
        """保存训练日志"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"training_log_{timestamp}.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.training_log, f, ensure_ascii=False, indent=2)
            print(f"📄 训练日志已保存到: {filename}")
        except Exception as e:
            print(f"❌ 保存训练日志失败: {e}")

    def train_database_structure(self) -> bool:
        """训练数据库结构"""
        print("\n📊 步骤 1: 训练数据库表结构...")
        success_count = 0

        try:
            # 获取所有表名
            tables = self.vn.run_sql("SHOW TABLES")
            if tables.empty:
                print("❌ 未找到任何表")
                return False

            table_names = tables.iloc[:, 0].tolist()
            print(f"发现 {len(table_names)} 个表: {', '.join(table_names)}")

            # 为每个表添加结构信息
            for table in table_names:
                print(f"正在训练表: {table}")

                try:
                    # 方法1: 获取建表语句
                    create_result = self.vn.run_sql(f"SHOW CREATE TABLE `{table}`")
                    if not create_result.empty and len(create_result.columns) >= 2:
                        ddl = create_result.iloc[0, 1]  # 第二列是建表语句
                        self.vn.train(ddl=ddl)
                        success_count += 1

                        # 记录日志
                        log_entry = {
                            "timestamp": datetime.now().isoformat(),
                            "type": "DDL",
                            "table": table,
                            "status": "success",
                            "content": ddl[:200] + "..." if len(ddl) > 200 else ddl
                        }
                        self.training_log.append(log_entry)
                        print(f"  ✅ 已添加 {table} 的表结构")

                except Exception as e:
                    print(f"  ⚠️ 无法获取 {table} 的建表语句: {e}")

                    # 备用方案：使用 DESCRIBE
                    try:
                        desc = self.vn.run_sql(f"DESCRIBE `{table}`")
                        if not desc.empty:
                            # 构建更详细的表信息
                            table_info = f"""
-- 表 {table} 的详细信息
-- 字段信息：
{desc.to_string()}

-- 表注释和使用说明
-- 表名: {table}
-- 字段数量: {len(desc)}
-- 主要字段: {', '.join(desc['Field'].head(5).tolist())}
                            """
                            self.vn.train(documentation=table_info)
                            success_count += 1

                            # 记录日志
                            log_entry = {
                                "timestamp": datetime.now().isoformat(),
                                "type": "DESCRIBE",
                                "table": table,
                                "status": "success",
                                "content": table_info[:200] + "..."
                            }
                            self.training_log.append(log_entry)
                            print(f"  ✅ 已添加 {table} 的字段信息（备用方案）")
                    except Exception as e2:
                        print(f"  ❌ 备用方案也失败: {e2}")
                        log_entry = {
                            "timestamp": datetime.now().isoformat(),
                            "type": "ERROR",
                            "table": table,
                            "status": "failed",
                            "error": str(e2)
                        }
                        self.training_log.append(log_entry)

            print(f"✅ 成功训练了 {success_count}/{len(table_names)} 个表的结构")
            return success_count > 0

        except Exception as e:
            print(f"❌ 训练表结构时出错: {e}")
            return False

    def add_business_documentation(self):
        """添加业务文档和说明"""
        print("\n📚 步骤 2: 添加业务文档...")

        business_docs = [
            """
数据库业务说明：
- 这是一个业务系统数据库，包含核心业务数据
- 日期字段命名规范：created_at（创建时间）、updated_at（更新时间）
- ID字段通常是自增主键，命名为 id 或 表名_id
- 状态字段通常使用数字编码：1=启用/正常，0=禁用/删除
- 金额字段通常使用 DECIMAL 类型，单位为分或元
            """,

            """
常用SQL查询模式和最佳实践：
- 日期范围查询：WHERE created_at BETWEEN '开始日期' AND '结束日期'
- 分页查询：LIMIT 每页数量 OFFSET 偏移量
- 模糊搜索：WHERE 字段名 LIKE '%关键词%'
- 统计查询：COUNT(*)计数, AVG()平均值, SUM()求和, MAX()最大值, MIN()最小值
- 分组统计：GROUP BY 分组字段 HAVING 分组条件
- 排序：ORDER BY 字段名 ASC/DESC
- 去重：SELECT DISTINCT 字段名
            """,

            """
中文查询关键词映射：
- "所有"、"全部" -> SELECT * 或 COUNT(*)
- "最新"、"最近" -> ORDER BY created_at DESC
- "统计"、"计算"、"数量" -> COUNT(), SUM(), AVG()等聚合函数
- "按...分组" -> GROUP BY
- "排序"、"排列" -> ORDER BY
- "前N个"、"最多N个" -> LIMIT N
- "包含"、"含有" -> LIKE '%...%'
- "大于"、"超过" -> >
- "小于"、"少于" -> <
- "等于"、"是" -> =
            """
        ]

        for i, doc in enumerate(business_docs, 1):
            try:
                self.vn.train(documentation=doc)
                print(f"  ✅ 已添加业务文档 {i}")

                # 记录日志
                log_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "DOCUMENTATION",
                    "content": f"业务文档 {i}",
                    "status": "success"
                }
                self.training_log.append(log_entry)

            except Exception as e:
                print(f"  ❌ 添加业务文档 {i} 失败: {e}")

    def generate_dynamic_examples(self) -> List[Dict]:
        """根据实际表结构生成动态示例"""
        examples = []

        try:
            # 获取表名列表
            tables_result = self.vn.run_sql("SHOW TABLES")
            if tables_result.empty:
                return examples

            table_names = tables_result.iloc[:, 0].tolist()

            # 为每个表生成基础示例
            for table in table_names[:3]:  # 限制前3个表，避免过多
                try:
                    # 获取表结构
                    desc = self.vn.run_sql(f"DESCRIBE `{table}`")
                    if desc.empty:
                        continue

                    columns = desc['Field'].tolist()

                    # 基础查询示例
                    examples.extend(
                        [
                            {
                                "question": f"查看{table}表的所有数据",
                                "sql": f"SELECT * FROM `{table}` LIMIT 100;"
                            },
                            {
                                "question": f"统计{table}表有多少条记录",
                                "sql": f"SELECT COUNT(*) as 记录总数 FROM `{table}`;"
                            },
                            {
                                "question": f"显示{table}表的前10条记录",
                                "sql": f"SELECT * FROM `{table}` LIMIT 10;"
                            }
                        ]
                    )

                    # 如果有时间字段，添加时间相关示例
                    time_columns = [col for col in columns if any(
                        keyword in col.lower()
                        for keyword in ['time', 'date', 'created', 'updated']
                    )]

                    if time_columns:
                        time_col = time_columns[0]
                        examples.extend(
                            [
                                {
                                    "question": f"按{time_col}倒序查看{table}表的最新数据",
                                    "sql": f"SELECT * FROM `{table}` ORDER BY `{time_col}` DESC LIMIT 20;"
                                },
                                {
                                    "question": f"查看{table}表今天的数据",
                                    "sql": f"SELECT * FROM `{table}` WHERE DATE(`{time_col}`) = CURDATE();"
                                },
                                {
                                    "question": f"统计{table}表每天的记录数",
                                    "sql": f"SELECT DATE(`{time_col}`) as 日期, COUNT(*) as 记录数 FROM `{table}` GROUP BY DATE(`{time_col}`) ORDER BY 日期 DESC;"
                                }
                            ]
                        )

                    # 如果有状态字段，添加状态相关示例
                    status_columns = [col for col in columns if any(
                        keyword in col.lower()
                        for keyword in ['status', 'state', 'enabled', 'active']
                    )]

                    if status_columns:
                        status_col = status_columns[0]
                        examples.extend(
                            [
                                {
                                    "question": f"统计{table}表不同{status_col}的数量",
                                    "sql": f"SELECT `{status_col}`, COUNT(*) as 数量 FROM `{table}` GROUP BY `{status_col}`;"
                                }
                            ]
                        )

                except Exception as e:
                    print(f"  ⚠️ 为表 {table} 生成示例时出错: {e}")
                    continue

        except Exception as e:
            print(f"❌ 生成动态示例时出错: {e}")

        return examples

    def add_example_questions(self):
        """添加示例问题和SQL对"""
        print("\n💡 步骤 3: 添加示例问题和SQL对...")

        # 通用示例
        general_examples = [
            {
                "question": "显示数据库中所有的表",
                "sql": "SHOW TABLES;"
            },
            {
                "question": "显示数据库信息",
                "sql": "SELECT DATABASE() as 当前数据库, VERSION() as MySQL版本, NOW() as 当前时间;"
            },
            {
                "question": "查看数据库大小",
                "sql": "SELECT table_schema AS '数据库', ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS '大小(MB)' FROM information_schema.tables WHERE table_schema = DATABASE() GROUP BY table_schema;"
            }
        ]

        # 获取动态生成的示例
        dynamic_examples = self.generate_dynamic_examples()

        # 合并所有示例
        all_examples = general_examples + dynamic_examples

        success_count = 0
        for i, pair in enumerate(all_examples, 1):
            try:
                self.vn.train(question=pair["question"], sql=pair["sql"])
                print(f"  ✅ 已添加示例 {i}: {pair['question']}")
                success_count += 1

                # 记录日志
                log_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "QUESTION_SQL_PAIR",
                    "question": pair["question"],
                    "sql": pair["sql"],
                    "status": "success"
                }
                self.training_log.append(log_entry)

            except Exception as e:
                print(f"  ❌ 添加示例 {i} 失败: {e}")

        print(f"✅ 成功添加了 {success_count}/{len(all_examples)} 个示例")

    def validate_training(self):
        """验证训练结果"""
        print("\n🔍 步骤 4: 验证训练结果...")

        test_questions = [
            "数据库中有哪些表？",
            "显示第一个表的结构",
            "统计数据总量",
            "查看最新的10条记录",
            "按时间排序显示数据"
        ]

        success_count = 0
        for question in test_questions:
            try:
                sql = self.vn.generate_sql(question)
                if sql and sql.strip():
                    print(f"  ✅ 问题: '{question}' -> SQL: {sql.strip()[:80]}...")
                    success_count += 1
                else:
                    print(f"  ❌ 问题: '{question}' -> 未生成SQL")
            except Exception as e:
                print(f"  ❌ 问题: '{question}' 失败: {e}")

        print(f"✅ 验证通过率: {success_count}/{len(test_questions)} ({success_count / len(test_questions) * 100:.1f}%)")
        return success_count / len(test_questions)

    def full_training_pipeline(self):
        """完整的训练流程"""
        print("🚀 开始训练 Vanna AI SQL 助手...")

        start_time = datetime.now()

        try:
            # 1. 训练数据库结构
            structure_success = self.train_database_structure()

            # 2. 添加业务文档
            # self.add_business_documentation()

            # 3. 添加示例问题
            self.add_example_questions()

            # 4. 验证训练结果
            validation_score = self.validate_training()

            # 保存训练日志
            self.save_training_log()

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            print(f"\n🎉 训练完成！")
            print(f"⏱️  用时: {duration:.2f} 秒")
            print(f"📊 验证得分: {validation_score * 100:.1f}%")

            if validation_score >= 0.6:
                print("✅ 训练质量良好，可以开始使用！")
            else:
                print("⚠️  训练质量一般，建议添加更多示例数据")

            print("\n💡 建议:")
            print("1. 继续使用过程中，如果发现生成的SQL不准确，可以继续添加更多示例")
            print("2. 可以使用 interactive_training() 进行交互式训练")
            print("3. 定期备份训练数据")

            return True

        except Exception as e:
            print(f"❌ 训练过程中出现错误: {e}")
            return False

    def add_custom_training_data(self, examples: List[Dict] = None, docs: List[str] = None):
        """添加自定义训练数据"""
        print("\n🔧 添加自定义训练数据...")

        if examples:
            for example in examples:
                try:
                    self.vn.train(question=example["question"], sql=example["sql"])
                    print(f"  ✅ 已添加自定义示例: {example['question']}")
                except Exception as e:
                    print(f"  ❌ 添加自定义示例失败: {e}")

        if docs:
            for doc in docs:
                try:
                    self.vn.train(documentation=doc)
                    print(f"  ✅ 已添加自定义文档")
                except Exception as e:
                    print(f"  ❌ 添加自定义文档失败: {e}")

    def interactive_training(self):
        """交互式训练模式"""
        print("\n🤖 交互式训练模式")
        print("输入 'quit' 退出，输入 'help' 查看帮助")

        while True:
            try:
                question = input("\n请输入一个问题: ").strip()

                if question.lower() == 'quit':
                    print("👋 退出交互式训练模式")
                    break
                elif question.lower() == 'help':
                    print(
                        """
帮助信息：
- 输入自然语言问题，系统会生成对应的SQL
- 如果SQL正确，输入 'y' 确认
- 如果SQL错误，输入 'n' 并提供正确的SQL
- 输入 'quit' 退出
- 输入 'help' 查看此帮助
                    """
                    )
                    continue
                elif not question:
                    print("⚠️ 请输入有效的问题")
                    continue

                # 生成SQL
                print("🤔 正在生成SQL...")
                sql = self.vn.generate_sql(question)
                print(f"生成的SQL: {sql}")

                # 询问是否正确
                is_correct = input("这个SQL正确吗？(y/n/skip): ").lower().strip()

                if is_correct == 'n':
                    correct_sql = input("请输入正确的SQL: ").strip()
                    if correct_sql:
                        self.vn.train(question=question, sql=correct_sql)
                        print("✅ 已添加到训练数据")
                elif is_correct == 'y':
                    self.vn.train(question=question, sql=sql)
                    print("✅ 已确认并添加到训练数据")
                elif is_correct == 'skip':
                    print("⏭️ 已跳过此问题")
                else:
                    print("⚠️ 无效的输入，已跳过")

            except KeyboardInterrupt:
                print("\n\n👋 用户中断，退出交互式训练模式")
                break
            except Exception as e:
                print(f"❌ 出错: {e}")


def main():
    """主函数"""
    try:
        # 导入 vn 实例


        # 创建训练器
        trainer = VannaTrainer(vn)

        # 执行完整训练流程
        success = trainer.full_training_pipeline()

        if success:
            # 可选：添加自定义训练数据
            # custom_examples = [
            #     {
            #         "question": "你的业务问题",
            #         "sql": "对应的SQL查询"
            #     }
            # ]
            # trainer.add_custom_training_data(examples=custom_examples)

            # 可选：交互式训练
            interactive_choice = input("\n是否进入交互式训练模式？(y/n): ").lower().strip()
            if interactive_choice == 'y':
                trainer.interactive_training()

    except ImportError as e:
        print(f"❌ 无法导入 vn 实例: {e}")
        print("请确保 app2.py 文件存在且 vn 实例已正确初始化")
    except Exception as e:
        print(f"❌ 程序执行出错: {e}")


if __name__ == "__main__":
    main()
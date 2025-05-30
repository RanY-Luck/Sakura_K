#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025-05-28 18:15:00
# @Author   : 冉勇
# @File     : rewrite_ask.py
# @Software : PyCharm
# @Desc     : 重写Vanna的ask函数，增强功能

import io
import traceback
import pandas as pd
import plotly
from typing import Union, Tuple
from PIL import Image as PILImage


def ask(
        vanna_instance,
        question: Union[str, None] = None,
        print_results: bool = True,
        auto_train: bool = True,
        visualize: bool = True,  # if False, will not generate plotly code
        allow_llm_to_see_data: bool = False,
) -> Union[
    Tuple[
        Union[str, None],
        Union[pd.DataFrame, None],
        Union[plotly.graph_objs.Figure, None],
    ],
    None,
]:
    """
    **Example:**
    python
    vn.ask("What are the top 10 customers by sales?")
    Ask Vanna.AI a question and get the SQL query that answers it.

    Args:
        vanna_instance: Vanna实例
        question (str): 要问的问题
        print_results (bool): 是否打印SQL查询结果
        auto_train (bool): 是否自动训练Vanna.AI问题和SQL查询
        visualize (bool): 是否生成plotly代码并显示plotly图形
        allow_llm_to_see_data (bool): 是否允许大语言模型看到数据

    Returns:
        Tuple[str, pd.DataFrame, plotly.graph_objs.Figure]: SQL查询、查询结果和plotly图形
    """

    if question is None:
        question = input("输入一个问题: ")

    try:
        sql = vanna_instance.generate_sql(question=question, allow_llm_to_see_data=allow_llm_to_see_data)
    except Exception as e:
        print(e)
        return f"-- Error generating SQL: {str(e)}", pd.DataFrame(), None

    if print_results:
        try:
            Code = __import__("IPython.display", fromlist=["Code"]).Code
            display = __import__("IPython.display", fromlist=["display"]).display
            display(Code(sql))
        except Exception as e:
            print(sql)

    if vanna_instance.run_sql_is_set is False:
        print(
            "如果要运行SQL查询，请先连接到数据库。"
        )

        if print_results:
            return sql, pd.DataFrame(), None
        else:
            return sql, pd.DataFrame(), None

    try:
        df = vanna_instance.run_sql(sql)

        if print_results:
            try:
                display = __import__("IPython.display", fromlist=["display"]).display
                display(df)
            except Exception as e:
                print(df)

        if len(df) > 0 and auto_train:
            vanna_instance.add_question_sql(question=question, sql=sql)

        # 初始化fig为None
        fig = None
        
        # 只有当visualize为True时才生成plotly代码
        if visualize:
            try:
                plotly_code = vanna_instance.generate_plotly_code(
                    question=question,
                    sql=sql,
                    df_metadata=f"Running df.dtypes gives:\n {df.dtypes}",
                )
                fig = vanna_instance.get_plotly_figure(plotly_code=plotly_code, df=df)
                if print_results:
                    try:
                        display = __import__("IPython.display", fromlist=["display"]).display
                        display(plotly_code)
                    except Exception as e:
                        print(plotly_code)

            except Exception as e:
                # 打印堆栈跟踪
                traceback.print_exc()
                print("无法运行plotly代码: ", e)
                if print_results:
                    return sql, df, None
                else:
                    return sql, df, None
        else:
            return sql, df, None

    except Exception as e:
        print("无法运行SQL: ", e)
        if print_results:
            return sql, pd.DataFrame(), None
        else:
            return sql, pd.DataFrame(), None
    
    # 确保总是返回三元组
    return sql, df, fig


def display_image_in_pycharm(fig):
    """在PyCharm中使用matplotlib或PIL显示图像。"""
    try:
        # 尝试使用IPython.display（如果可用）
        try:
            display = __import__("IPython.display", fromlist=["display"]).display
            Image = __import__("IPython.display", fromlist=["Image"]).Image
            img_bytes = fig.to_image(format="png", scale=2)
            display(Image(img_bytes))
        except AttributeError:
            print("fig没有to_image方法，使用fig.savefig代替")
            fig.savefig("output.png")
            display(Image("output.png"))
        except ImportError:
            print("IPython.display不可用，使用matplotlib显示图像")
            fig.show()
    except Exception as e:
        print(f"使用IPython.display显示图像失败: {e}")
        traceback.print_exc()
        try:
            # 使用matplotlib显示图像
            fig.show()
        except Exception as e:
            print(f"使用fig.show显示图像失败: {e}")
            traceback.print_exc()
        try:
            # 使用PIL显示图像
            img_bytes = io.BytesIO()
            fig.savefig(img_bytes, format='png')
            img_bytes.seek(0)
            pil_img = PILImage.open(img_bytes)
            pil_img.show()
        except Exception as e:
            print(f"使用PIL显示图像失败: {e}")
            traceback.print_exc() 
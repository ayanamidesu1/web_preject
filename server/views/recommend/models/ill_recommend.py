import random
import re
from django.db import connection
from ..log.log import Logger


class IllRecommendation:
    def __init__(self):
        # 初始化 Logger
        self.logger = Logger()

    def get_userid(self, userid, offset=0, limit=9):
        # SQL 查询语句
        watch_sql = 'SELECT * FROM user_watch_table WHERE userid=%s AND type=%s LIMIT %s OFFSET %s'
        like_sql = 'SELECT * FROM user_like_table WHERE userid=%s AND type=%s LIMIT %s OFFSET %s'
        collect_sql = 'SELECT * FROM user_collection_table WHERE userid=%s AND type=%s LIMIT %s OFFSET %s'

        try:
            # 提取用户行为数据
            watch_id_list = self.query_work_ids(watch_sql, userid, offset, limit)
            like_id_list = self.query_work_ids(like_sql, userid, offset, limit)
            collect_id_list = self.query_work_ids(collect_sql, userid, offset, limit)

            # 合并并加权标签
            all_tags = self.get_weighted_tags(watch_id_list, 1) + \
                       self.get_weighted_tags(like_id_list, 2) + \
                       self.get_weighted_tags(collect_id_list, 3)

            # 记录加权后的标签
            tags_str = ', '.join(all_tags)
            print('加权后的标签: %s' % tags_str)

            # 统计标签频率
            tag_frequency = self.count_tag_frequency(all_tags)

            # 从插画信息表中获取所有作品
            all_works = self.query_works(offset, limit)

            # 基于标签频率推荐作品
            recommendations = self.recommend_works(all_works, tag_frequency)

            # 确保列表长度达到 limit
            total_recommendations = len(recommendations)
            if total_recommendations < limit:
                # 获取额外的作品
                additional_count = limit - total_recommendations
                additional_works = self.query_additional_works(additional_count)
                # 仅对额外的作品进行随机
                recommendations.extend(additional_works)
                # 随机打乱补充的作品顺序
                additional_works.sort(key=lambda x: x.get('score', 0), reverse=True)  # 保持原有排序
                random.shuffle(recommendations[total_recommendations:])

            # 实现分页并处理循环
            total_works = len(recommendations)
            if total_works == 0:
                self.logger.info('没有推荐的作品')
                return []  # 如果没有推荐的作品，返回空列表

            start_index = offset % total_works
            end_index = start_index + limit
            paginated_recommendations = recommendations[start_index:end_index]

            if end_index > total_works:
                paginated_recommendations.extend(recommendations[:end_index % total_works])

            return paginated_recommendations

        except Exception as e:
            self.logger.error('获取用户推荐时发生错误: %s' % str(e))
            return []

    def query_work_ids(self, sql, userid, offset, limit):
        """执行 SQL 查询并返回 work_ids 列表"""
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql, [userid, 'ill', limit, offset])
                results = cursor.fetchall()
                # 转换结果为字典格式
                results_dict = [self.convert_tuple_to_dict(cursor.description, row) for row in results]
                return [item['workid'] for item in results_dict]
            except Exception as e:
                self.logger.error('执行查询时发生错误: %s' % str(e))
                return []

    def query_works(self, offset, limit):
        """从插画信息表中获取作品，考虑分页"""
        sql = 'SELECT * FROM illustration_work LIMIT %s OFFSET %s'
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql, [limit, offset])
                results = cursor.fetchall()
                # 转换结果为字典格式
                results_dict = [self.convert_tuple_to_dict(cursor.description, row) for row in results]
                return results_dict
            except Exception as e:
                self.logger.error('获取作品信息时发生错误: %s' % str(e))
                return []

    def get_weighted_tags(self, work_ids, weight):
        # 获取带权重的标签
        weighted_tags = []
        for work_id in work_ids:
            tags = self.set_tag_list(work_id)
            weighted_tags.extend(tags * weight)
        return weighted_tags

    def set_tag_list(self, work_id):
        sql = 'SELECT work_tags FROM illustration_work WHERE Illustration_id=%s'
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql, [work_id])
                result = cursor.fetchone()
                # 转换结果为字典格式
                if result:
                    result_dict = self.convert_tuple_to_dict(cursor.description, result)
                    tags_str = result_dict.get('work_tags', '')
                    return self.split_tags(tags_str)
            except Exception as e:
                self.logger.error('获取标签列表时发生错误: %s' % str(e))
        return []

    def split_tags(self, tags_str):
        # 将标签字符串按英文逗号和中文逗号分隔成标签列表
        return re.split(r'[，,]', tags_str.strip())

    def count_tag_frequency(self, tags):
        # 计算每个标签的频率
        frequency = {}
        for tag in tags:
            tag = tag.strip()
            if tag:
                frequency[tag] = frequency.get(tag, 0) + 1
        return frequency

    def recommend_works(self, works, tag_frequency):
        # 根据标签频率对作品进行评分，并按得分排序返回推荐的作品信息字典列表
        recommendations = []
        for work in works:
            # 获取作品标签
            work_tags = self.split_tags(work.get('work_tags', ''))
            # 计算作品得分
            score = sum(tag_frequency.get(tag.strip(), 0) for tag in work_tags)
            # 确保作品包含 'Illustration_id' 键
            if 'Illustration_id' in work:
                work_id = work['Illustration_id']
                work_info = self.get_work_info(work_id)
                if work_info:
                    work_info['score'] = score  # 将得分添加到作品信息中
                    recommendations.append(work_info)

        # 按得分排序，返回得分最高的作品信息字典列表
        recommendations.sort(key=lambda x: x.get('score', 0), reverse=True)
        return recommendations

    def get_work_info(self, work_id):
        sql = 'SELECT * FROM illustration_work WHERE Illustration_id=%s'
        get_author_info = 'SELECT * FROM users WHERE userid=%s'

        with connection.cursor() as cursor:
            try:
                # 查询作品信息
                cursor.execute(sql, [work_id])
                result = cursor.fetchone()
                # 转换结果为字典格式
                if result:
                    result_dict = self.convert_tuple_to_dict(cursor.description, result)
                    userid = result_dict.get('belong_to_user_id')
                    if userid:
                        # 查询作者信息
                        cursor.execute(get_author_info, [userid])
                        author_info = cursor.fetchone()
                        # 转换结果为字典格式
                        if author_info:
                            author_info_dict = self.convert_tuple_to_dict(cursor.description, author_info)
                            # 删除不需要的字段
                            author_info_dict.pop('password', None)
                            author_info_dict.pop('token', None)
                            # 将作者信息添加到作品信息中
                            result_dict['author_info'] = author_info_dict

                return result_dict

            except Exception as e:
                self.logger.error('获取作品信息时发生错误: %s' % str(e))
                return None

    def convert_tuple_to_dict(self, description, row):
        """将元组结果转换为字典"""
        return dict(zip([col[0] for col in description], row))

    def query_additional_works(self, additional_count):
        """获取额外的作品以填充到指定数量"""
        sql = 'SELECT * FROM illustration_work'
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql)
                all_works = cursor.fetchall()
                # 转换结果为字典格式
                all_works_dict = [self.convert_tuple_to_dict(cursor.description, row) for row in all_works]

                # 随机选择额外作品
                selected_work_ids = random.choices([work['Illustration_id'] for work in all_works_dict],
                                                   k=additional_count)

                # 获取每个作品的详细信息
                additional_works = []
                for work_id in selected_work_ids:
                    work_info = self.get_work_info(work_id)
                    if work_info:
                        additional_works.append(work_info)

                return additional_works
            except Exception as e:
                self.logger.error('获取额外作品时发生错误: %s' % str(e))
                return []

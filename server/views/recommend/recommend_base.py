import re
from collections import defaultdict
from datetime import datetime, timedelta

import numpy as np
import pymysql
from base_api import BaseApi

# 数据库连接配置
sql_info = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'admin',
    'password': '123456',
    'database': 'admin',
    'charset': 'utf8mb4'
}

class RecommendBase(BaseApi):
    # 配置不同内容类型的元数据
    CONTENT_CONFIG = {
        'ill': {
            'table': 'illustration_work',
            'id_field': 'Illustration_id',
            'user_field': 'belong_to_user_id',
            'time_field': 'time'
        },
        'comic': {
            'table': 'comic',
            'id_field': 'id',
            'user_field': 'belong_to_userid',
            'time_field': 'time'
        },
        'novel': {
            'table': 'novel_work',
            'id_field': 'work_id',
            'user_field': 'belong_to_userid',
            'time_field': 'time'
        }
    }

    # 权重配置（个性化推荐中用于标签权重计算）
    WEIGHT_CONFIG = {
        'watch': 1.0,
        'like': 2.0,
        'collect': 3.0,
        'follow_work': 1.5  # 关注用户作品额外加成
    }

    def __init__(self):
        # 初始化 pymysql 连接
        self.conn = pymysql.connect(**sql_info)

    def execute_sql(self, sql, params):
        """执行 SQL 语句并返回字典格式的结果"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, params)
                result = self.dictfetchall(cursor)
            return result
        except Exception as e:
            print(f"执行 SQL 失败: {str(e)}")
            return []

    def dictfetchall(self, cursor):
        """将 SQL 结果转换为字典列表"""
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_user_history(self, userid, content_type):
        """获取用户行为记录"""
        try:
            watch_data = self.execute_sql(
                "SELECT workid, MAX(create_time) as last_time "
                "FROM user_watch_table "
                "WHERE userid=%s AND type=%s "
                "GROUP BY workid LIMIT 100",
                [userid, content_type]
            )
            collect_data = self.execute_sql(
                "SELECT workid FROM user_collection_table "
                "WHERE userid=%s AND type=%s LIMIT 100",
                [userid, content_type]
            )
            like_data = self.execute_sql(
                "SELECT workid FROM user_like_table "
                "WHERE userid=%s AND type=%s LIMIT 100",
                [userid, content_type]
            )

            # 获取关注用户的作品
            follow_works = self.get_follow_works(userid, content_type)

            return {
                'watch': [item['workid'] for item in watch_data],
                'collect': [item['workid'] for item in collect_data],
                'like': [item['workid'] for item in like_data],
                'follow_work': follow_works,
                'watch_times': {item['workid']: item['last_time'] for item in watch_data}
            }
        except Exception as e:
            print(f"获取用户历史记录失败: {str(e)}")
            return defaultdict(list)

    def get_follow_works(self, userid, content_type):
        """批量获取关注用户的作品"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "SELECT follow_user_id FROM user_follow "
                    "WHERE user_id=%s LIMIT 100",
                    [userid]
                )
                follow_ids = [row[0] for row in cursor.fetchall()]
                if not follow_ids:
                    return []
                config = self.CONTENT_CONFIG[content_type]
                cursor.execute(
                    f"SELECT {config['id_field']} FROM {config['table']} "
                    f"WHERE {config['user_field']} IN %s "
                    f"ORDER BY {config['time_field']} DESC LIMIT 100",
                    [tuple(follow_ids)]
                )
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"获取关注作品失败: {str(e)}")
            return []

    def parse_tags(self, tag_str):
        """标准化标签解析"""
        if not tag_str:
            return []
        return [tag.strip().lower() for tag in re.split(r'[，,、]', tag_str) if tag.strip()]

    def get_candidates(self, content_type):
        """
        获取候选作品列表（全部内容均可作为候选）
        """
        try:
            config = self.CONTENT_CONFIG[content_type]
            with self.conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT {config['id_field']}, work_tags, {config['time_field']} "
                    f"FROM {config['table']}"
                )
                return self.dictfetchall(cursor)
        except Exception as e:
            print(f"获取候选作品失败: {str(e)}")
            return []

    def jaccard_similarity(self, set1, set2):
        """计算 Jaccard 相似度"""
        if not set1 or not set2:
            return 0.0
        intersection = set1 & set2
        union = set1 | set2
        return len(intersection) / len(union) if union else 0.0

    def get_item_cf_recommendations(self, userid, content_type, limit=10, offset=0):
        """
        基于物品协同过滤（标签集合的 Jaccard 相似度）的推荐：
          1. 获取用户历史作品（直接消费过的作品），构建其标签集合；
          2. 遍历候选作品（内容表），对每个作品计算与用户历史中各作品标签集合的最大相似度；
          3. 排除用户已消费作品，按相似度得分降序排序返回。
        """
        # 获取用户历史行为，合并各类行为形成用户已消费作品集合
        history = self.get_user_history(userid, content_type)
        user_items = set(history['watch'] + history['collect'] + history['like'] + history['follow_work'])
        if not user_items:
            return self.get_fallback_recommend(content_type, limit)
        config = self.CONTENT_CONFIG[content_type]

        # 查询用户历史中各作品的标签集合
        user_history_tags = {}
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"SELECT {config['id_field']}, work_tags FROM {config['table']} "
                f"WHERE {config['id_field']} IN %s",
                [tuple(user_items)]
            )
            for row in cursor.fetchall():
                wid, tags = row
                user_history_tags[wid] = set(self.parse_tags(tags))

        # 获取所有候选作品
        candidates = self.get_candidates(content_type)
        scored_candidates = []
        for work in candidates:
            work_id = work[config['id_field']]
            # 排除用户已消费的作品
            if work_id in user_items:
                continue
            candidate_tags = set(self.parse_tags(work['work_tags']))
            max_sim = 0.0
            # 对用户历史中每个作品，计算候选作品与之的相似度，取最大值
            for tags in user_history_tags.values():
                sim = self.jaccard_similarity(candidate_tags, tags)
                if sim > max_sim:
                    max_sim = sim
            scored_candidates.append((work, max_sim))

        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        # 分页返回结果
        result_candidates = [item[0] for item in scored_candidates]
        return self.paginate(result_candidates, offset, limit)

    def paginate(self, items, offset, limit):
        """智能分页处理，支持循环翻页"""
        total = len(items)
        if total == 0:
            return []
        offset = offset % total
        end = offset + limit
        if end <= total:
            return items[offset:end]
        return items[offset:] + items[:end - total]

    def get_fallback_recommend(self, content_type, limit):
        """
        降级推荐：
          采用观看历史统计标签热度进行简单排序
        """
        try:
            # 此处复用之前的降级策略
            tag_popularity = defaultdict(int)
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "SELECT workid FROM user_watch_table WHERE type=%s ORDER BY create_time DESC LIMIT 100000",
                    [content_type]
                )
                work_ids = [row[0] for row in cursor.fetchall()]
            if work_ids:
                work_freq = defaultdict(int)
                for wid in work_ids:
                    work_freq[wid] += 1
                config = self.CONTENT_CONFIG[content_type]
                with self.conn.cursor() as cursor:
                    cursor.execute(
                        f"SELECT {config['id_field']}, work_tags FROM {config['table']} "
                        f"WHERE {config['id_field']} IN %s",
                        [tuple(work_freq.keys())]
                    )
                    for row in cursor.fetchall():
                        wid, tags = row
                        for tag in self.parse_tags(tags):
                            tag_popularity[tag] += work_freq[wid]
            # 根据标签热度对候选作品打分
            config = self.CONTENT_CONFIG[content_type]
            with self.conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT {config['id_field']}, work_tags, {config['time_field']} "
                    f"FROM {config['table']}"
                )
                candidates = self.dictfetchall(cursor)
            scored = []
            for work in candidates:
                score = sum(tag_popularity.get(tag, 0) for tag in self.parse_tags(work['work_tags']))
                scored.append((work, score))
            scored.sort(key=lambda x: x[1], reverse=True)
            return [x[0] for x in scored][:limit]
        except Exception as e:
            print(f"获取降级推荐失败: {str(e)}")
            return []

    def build_global_tag_index(self, content_type, min_count=5):
        """构建全局标签索引（带低频过滤）"""
        # 获取所有候选作品的标签
        config = self.CONTENT_CONFIG[content_type]
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"SELECT work_tags FROM {config['table']}"
            )
            all_tags = []
            for row in cursor.fetchall():
                all_tags.extend(self.parse_tags(row[0]))

        # 统计标签频率
        tag_counts = defaultdict(int)
        for tag in all_tags:
            tag_counts[tag] += 1

        # 过滤低频标签并建立索引
        filtered_tags = [tag for tag, cnt in tag_counts.items() if cnt >= min_count]
        return filtered_tags, {tag: idx for idx, tag in enumerate(filtered_tags)}

    def get_feature_matrix(self, work_ids, content_type, all_tags, tag_idx):
        """批量生成特征矩阵"""
        config = self.CONTENT_CONFIG[content_type]
        matrix = np.zeros((len(work_ids), len(all_tags)), dtype=np.float32)

        # 批量获取作品标签
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"SELECT {config['id_field']}, work_tags FROM {config['table']} "
                f"WHERE {config['id_field']} IN %s",
                [tuple(work_ids)]
            )
            for idx, row in enumerate(cursor.fetchall()):
                tags = self.parse_tags(row[1])
                for tag in tags:
                    if tag in tag_idx:
                        matrix[idx, tag_idx[tag]] = 1.0
        return matrix

    def get_candidate_matrix(self, content_type, all_tags, tag_idx):
        """获取候选作品特征矩阵"""
        config = self.CONTENT_CONFIG[content_type]
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"SELECT {config['id_field']} FROM {config['table']}"
            )
            candidate_ids = [row[0] for row in cursor.fetchall()]
        return self.get_feature_matrix(candidate_ids, content_type, all_tags, tag_idx), candidate_ids

    def get_history_matrix(self, content_type, user_items, all_tags, tag_idx):
        """获取历史作品特征矩阵"""
        return self.get_feature_matrix(list(user_items), content_type, all_tags, tag_idx), list(user_items)

    def calculate_jaccard_similarity(self, candidate_mat, history_mat):
        """矩阵化计算Jaccard相似度"""
        # 计算交集和并集
        intersection = np.dot(candidate_mat, history_mat.T)
        union = np.sum(candidate_mat, axis=1, keepdims=True) + np.sum(history_mat, axis=1) - intersection

        # 避免除以零
        union[union == 0] = 1e-9
        return intersection / union

    def build_paginated_results(self, candidate_ids, sorted_indices, user_items, offset, limit, config):
        """构建分页结果"""
        results = []
        seen = set()

        # 遍历排序后的索引
        for idx in sorted_indices:
            work_id = candidate_ids[idx]
            # 跳过用户已消费的
            if work_id in user_items or work_id in seen:
                continue
            # 获取完整作品信息
            with self.conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT * FROM {config['table']} "
                    f"WHERE {config['id_field']}=%s",
                    [work_id]
                )
                result = self.dictfetchall(cursor)
                if result:
                    results.append(result[0])
                    seen.add(work_id)
                if len(results) >= limit * 2:  # 预取两倍数据防止分页缺失
                    break

        return self.paginate(results, offset, limit)

    def get_item_cf_recommendations(self, userid, content_type, limit=10, offset=0):
        """优化后的基于物品协同过滤的推荐算法（使用numpy加速）"""
        # 获取用户历史行为数据
        history = self.get_user_history(userid, content_type)
        user_items = set(history['watch'] + history['collect'] + history['like'] + history['follow_work'])
        if not user_items:
            return self.get_fallback_recommend(content_type, limit)

        config = self.CONTENT_CONFIG[content_type]

        # 步骤1: 构建全局标签索引
        all_tags, tag_idx = self.build_global_tag_index(content_type)

        # 步骤2: 批量获取特征矩阵
        candidate_matrix, candidate_ids = self.get_candidate_matrix(content_type, all_tags, tag_idx)
        history_matrix, history_ids = self.get_history_matrix(content_type, user_items, all_tags, tag_idx)

        # 步骤3: 矩阵化计算相似度
        similarity_matrix = self.calculate_jaccard_similarity(candidate_matrix, history_matrix)

        # 步骤4: 获取最大相似度并排序
        max_similarities = np.max(similarity_matrix, axis=1)
        sorted_indices = np.argsort(-max_similarities)

        # 步骤5: 构建结果并分页
        return self.build_paginated_results(
            candidate_ids,
            sorted_indices,
            user_items,
            offset,
            limit,
            config
        )
    def get_recommend_work(self, userid, content_type='ill', limit=10, offset=0):
        """
        综合推荐算法：
          - 若 userid 为空，则采用降级推荐（基于观看历史标签热度）；
          - 否则采用基于物品协同过滤（次一级相关性最高）的推荐。
        """
        if not userid:
            return self.get_fallback_recommend(content_type, limit)
        try:
            return self.get_item_cf_recommendations(userid, content_type, limit, offset)
        except Exception as e:
            print(f"获取推荐作品失败: {str(e)}")
            return self.get_fallback_recommend(content_type, limit)


# 测试用例
if __name__ == '__main__':
    recommend_base = RecommendBase()
    # 当 user_id 为空时，直接使用降级推荐；否则使用协同过滤推荐
    user_id = 'f575b4d3-0683-11ef-adf4-00ffc6b98bdb'  # 或设置为 '' 测试空用户降级推荐
    result = recommend_base.get_item_cf_recommendations(user_id, 'novel', 3, 0)
    print("推荐结果：{}".format(result))

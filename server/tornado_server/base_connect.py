import json
from datetime import datetime
import jwt
import pymysql
import tornado
from fsspec.asyn import private
from tornado import httputil, web, websocket, httpclient
from tornado.ioloop import IOLoop
import sys
import os
from pathlib import Path

# 获取当前文件所在目录的绝对路径（tornado_server目录）
current_dir = Path(__file__).resolve().parent
# 计算项目根目录路径（H:\web_project\server）
server_dir = current_dir.parent
# 将server目录添加到Python路径
sys.path.append(str(server_dir))
# 现在可以正确导入djangoWebServer
from djangoWebServer.settings import BASE_DIR
import ssl
import json
from typing import Dict, Union, Optional
from threading import Lock
import tornado.websocket


class BaseConnect(tornado.websocket.WebSocketHandler):
    """
    WebSocket连接管理基类（线程安全版）
    功能：
    - 线程安全的连接池管理
    - 细粒度的消息发送控制
    - 三级权限体系（用户/管理员/系统管理员）
    """

    # 系统保留池（只能由系统管理员管理）
    SYSTEM_POOLS = {'default', 'admin'}

    # 角色常量
    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'
    ROLE_SYSTEM_ADMIN = 'sys_admin'

    # 连接池与锁初始化
    _pool_lock = Lock()

    connected_users = {
        'default': {},  # 普通用户池
        'admin': {}  # 管理员池
    }

    def add_to_pool(self, user_id: str, role: str = ROLE_USER, pool_name: str = 'default') -> bool:
        """
        线程安全的连接添加方法（更新权限控制）
        Args:
            user_id: 用户唯一标识
            role: 用户角色
            pool_name: 目标连接池
        Rules:
            1. default池：允许任何用户自由加入
            2. admin池：仅允许系统管理员加入
            3. 自定义池：允许任何用户加入（需后续管理权限控制）
        """
        with self._pool_lock:
            try:
                # 角色验证
                if role not in {self.ROLE_USER, self.ROLE_ADMIN, self.ROLE_SYSTEM_ADMIN}:
                    raise ValueError(f"无效角色: {role}")

                # 系统管理员必须放在admin池
                if role == self.ROLE_SYSTEM_ADMIN and pool_name != 'admin':
                    raise PermissionError("系统管理员必须存在于admin池")

                # admin池权限检查
                if pool_name == 'admin' and role != self.ROLE_SYSTEM_ADMIN:
                    raise PermissionError("只有系统管理员可以加入admin池")

                # 初始化连接池
                if pool_name not in self.connected_users:
                    self.connected_users[pool_name] = {}

                # 处理已有连接
                if user_id in self.connected_users[pool_name]:
                    old_conn = self.connected_users[pool_name][user_id]
                    try:
                        old_conn.close()
                    except:
                        pass

                # 添加新连接
                self.connected_users[pool_name][user_id] = self
                setattr(self, '_ws_role', role)
                setattr(self, '_ws_pool', pool_name)
                setattr(self, '_ws_user_id', user_id)  # 新增：记录用户ID
                return True

            except Exception as e:
                print(f"[ERROR] 添加连接失败: {str(e)}")
                return False

    def _check_permission(self, action: str, target_pool: str = None) -> bool:
        """
        统一的权限检查方法
        Args:
            action: 操作类型（send/manage）
            target_pool: 目标连接池
        """
        current_role = getattr(self, '_ws_role', self.ROLE_USER)
        current_pool = getattr(self, '_ws_pool', None)

        # 系统管理员拥有全部权限
        if current_role == self.ROLE_SYSTEM_ADMIN:
            return True

        # 普通管理员的管理权限
        if action == 'manage':
            return (current_role == self.ROLE_ADMIN and
                    target_pool not in self.SYSTEM_POOLS and
                    target_pool == current_pool)

        # 消息发送权限
        elif action == 'send':
            # 禁止操作系统保留池
            if target_pool in self.SYSTEM_POOLS:
                return False
            # 只能向当前所在池发送
            return target_pool == current_pool

        return False

    def send_to_group(self, message: Union[str, dict], pool_name: str) -> bool:
        """
        线程安全的组播方法
        Args:
            message: 要发送的消息
            pool_name: 目标连接池（all表示全局广播）
        """
        with self._pool_lock:
            try:
                # 消息序列化
                if isinstance(message, dict):
                    message = json.dumps(message)

                current_role = getattr(self, '_ws_role', self.ROLE_USER)

                # 系统管理员路径
                if current_role == self.ROLE_SYSTEM_ADMIN:
                    if pool_name == 'all':
                        return self._broadcast(message)
                    return self._send_to_specific_pool(message, pool_name)

                # 非系统管理员路径
                if not self._check_permission('send', pool_name):
                    raise PermissionError("没有发送消息的权限")

                return self._send_to_specific_pool(message, pool_name)

            except Exception as e:
                print(f"[ERROR] 组播失败: {str(e)}")
                return False

    def _send_to_specific_pool(self, message: str, pool_name: str) -> bool:
        """内部方法：向指定池发送消息"""
        if pool_name not in self.connected_users:
            raise ValueError(f"连接池不存在: {pool_name}")

        success = True
        for conn in list(self.connected_users[pool_name].values()):
            try:
                conn.write_message(message)
            except:
                success = False
        return success

    def _broadcast(self, message: Union[str, dict]) -> bool:
        """内部方法：全局广播"""
        success = True
        for pool in self.connected_users.values():
            for conn in pool.values():
                try:
                    conn.write_message(message)
                except:
                    success = False
        return success
    #遍历池内所有连接发送全局消息

    def manage_pool(self, action: str, target_pool: str, user_id: Optional[str] = None) -> bool:
        """
        线程安全的连接池管理
        Args:
            action: 操作类型（remove_user/delete_pool）
            target_pool: 目标连接池
            user_id: 目标用户ID
        """
        with self._pool_lock:
            try:
                if not self._check_permission('manage', target_pool):
                    raise PermissionError("没有管理权限")

                if action == 'remove_user':
                    if not user_id:
                        raise ValueError("需要指定user_id")
                    return self._remove_user(target_pool, user_id)

                elif action == 'delete_pool':
                    return self._delete_pool(target_pool)

                raise ValueError(f"未知操作类型: {action}")

            except Exception as e:
                print(f"[ERROR] 管理操作失败: {str(e)}")
                return False

    def _remove_user(self, pool_name: str, user_id: str) -> bool:
        """内部方法：移除用户"""
        if user_id in self.connected_users.get(pool_name, {}):
            try:
                self.connected_users[pool_name][user_id].close()
            except:
                pass
            del self.connected_users[pool_name][user_id]
            return True
        return False

    def _delete_pool(self, pool_name: str) -> bool:
        """内部方法：删除连接池"""
        if pool_name in self.connected_users:
            for conn in self.connected_users[pool_name].values():
                try:
                    conn.close()
                except:
                    pass
            del self.connected_users[pool_name]
            return True
        return False

    # 兼容原有接口
    def broadcast_message(self, message: Union[str, dict]) -> bool:
        return self.send_to_group(message, 'all')

    def send_to_user(self, user_id: str, message: Union[str, dict], pool_name: str = 'default') -> bool:
        """
        单播消息（线程安全版）
        Args:
            user_id: 发送消息给指定用户
            message: 发送的消息可以为字符串或集合
            pool_name: 发送的连接池，默认为default
        """
        with self._pool_lock:
            try:
                if isinstance(message, dict):
                    message = json.dumps(message)

                if pool_name == 'all':
                    sent = False
                    for pool in self.connected_users.values():
                        if user_id in pool:
                            pool[user_id].write_message(message)
                            sent = True
                    return sent

                if pool_name in self.connected_users and user_id in self.connected_users[pool_name]:
                    self.connected_users[pool_name][user_id].write_message(message)
                    return True
                return False

            except Exception as e:
                print(f"[ERROR] 单播失败: {str(e)}")
                return False

    #退出连接
    def disconnect(self, user_id: Optional[str] = None, pool_name: str = 'default') -> bool:
        """
        断开连接（更新权限控制）
        Args:
            user_id: 要退出的用户ID（None表示当前连接）
            pool_name: 目标池名称
        Rules:
            1. default池：允许用户自行退出
            2. admin池：仅系统管理员可操作
            3. 自定义池：允许用户自行退出或管理员操作
        """
        with self._pool_lock:
            try:
                current_role = getattr(self, '_ws_role', self.ROLE_USER)

                # 处理未提供user_id的情况
                if user_id is None:
                    user_id = getattr(self, '_ws_user_id', None)
                    if user_id is None:
                        raise ValueError("未提供user_id且当前连接无用户ID")
                    pool_name = getattr(self, '_ws_pool', 'default')

                # 检查admin池权限
                if pool_name == 'admin' and current_role != self.ROLE_SYSTEM_ADMIN:
                    raise PermissionError("只有系统管理员可以操作admin池")

                # 检查是否是自己的连接
                if (pool_name != 'default' and
                        current_role != self.ROLE_SYSTEM_ADMIN and
                        current_role != self.ROLE_ADMIN and
                        user_id != getattr(self, '_ws_user_id', None)):
                    raise PermissionError("只能操作自己的连接")

                # 执行断开操作
                if pool_name == 'all':
                    removed = False
                    for pool in list(self.connected_users.values()):
                        if user_id in pool:
                            try:
                                pool[user_id].close()
                            except:
                                pass
                            del pool[user_id]
                            removed = True
                    return removed
                else:
                    if pool_name in self.connected_users and user_id in self.connected_users[pool_name]:
                        try:
                            self.connected_users[pool_name][user_id].close()
                        except:
                            pass
                        del self.connected_users[pool_name][user_id]
                        return True
                    return False

            except Exception as e:
                print(f"[ERROR] 断开连接失败: {str(e)}")
                return False

    def get_pool_info(self, pool_name: str = 'all') -> Dict:
        """获取连接池信息（线程安全版）"""
        with self._pool_lock:
            if pool_name == 'all':
                return {name: len(pool) for name, pool in self.connected_users.items()}
            return {pool_name: len(self.connected_users.get(pool_name, {}))}

    def get_connection(self, identifier: str, pool_name: str = 'default',
                       conn_type: str = 'conn') -> Union[Dict[str, websocket.WebSocketHandler],
    websocket.WebSocketHandler,None]:
        """
        获取连接信息（线程安全版）

        Args:
            identifier: 用户ID（当type='conn'时）或连接池名称（当type='pool'时）
            pool_name: 要查询的连接池名称（默认default）
            conn_type: 查询类型，'conn'表示获取单个连接，'pool'表示获取整个连接池

        Returns:
            - 当type='conn': 返回单个WebSocket连接对象，未找到返回None
            - 当type='pool': 返回指定连接池的所有连接字典，未找到返回空字典
            - 发生错误返回None

        Raises:
            ValueError: 参数错误时抛出
        """
        with self._pool_lock:
            try:
                if conn_type not in ('conn', 'pool'):
                    raise ValueError("conn_type必须是'conn'或'pool'")

                # 获取整个连接池
                if conn_type == 'pool':
                    return self.connected_users.get(identifier, {}).copy()  # 返回副本避免外部修改

                # 获取单个连接
                if pool_name not in self.connected_users:
                    return None

                return self.connected_users[pool_name].get(identifier)

            except Exception as e:
                print(f"[ERROR] 获取连接失败: {str(e)}")
                return None if conn_type == 'conn' else {}

    @classmethod
    def broadcast_heartbeat(cls):
        """最终修正版心跳广播"""
        heartbeat_msg = json.dumps({
            "time": datetime.now().isoformat(),
            "msg": "心跳消息",
            "server": "alive"
        })

        with cls._pool_lock:
            for pool_name, connections in cls.connected_users.items():
                print("连接池: {}，连接列表：{}".format(pool_name, connections))
                for user_id, conn in list(connections.items()):
                    try:
                        if isinstance(conn, tornado.websocket.WebSocketHandler):
                            if getattr(conn, 'close_code', None) is None:
                                conn.write_message(heartbeat_msg)
                            else:
                                del cls.connected_users[pool_name][user_id]
                                print(f"清理断开连接: {user_id}")
                        else:
                            print(f"移除无效连接: {user_id}")
                            del cls.connected_users[pool_name][user_id]
                    except Exception as e:
                        print(f"心跳发送失败[{user_id}]: {str(e)}")
    def check_origin(self, origin):
        # 允许所有来源
        return True

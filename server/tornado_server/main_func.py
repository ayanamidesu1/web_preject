import json
from datetime import datetime
from threading import Lock
import tornado.websocket


class MainFunc:
    @classmethod
    async def handle_heartbeat(cls, handler, msg_data):
        """
        处理一对一心跳
        Args:
            handler: WebSocketHandler实例
            msg_data: 消息数据
        """
        try:
            target_id = msg_data.get('target_user_id')
            if not target_id:
                await handler.write_message({
                    'type': 'error',
                    'message': 'target_user_id is required'
                })
                return

            # 发送自身心跳响应
            await handler.write_message({
                'type': 'heartbeat_ack',
                'from_user': handler.user_id,
                'timestamp': datetime.now().isoformat(),
                'status': 'active'
            })

            # 检查目标用户状态
            with handler._pool_lock:
                target_conn = handler.connected_users.get('default', {}).get(target_id)

                if target_conn and getattr(target_conn, 'close_code', None) is None:
                    try:
                        await target_conn.write_message({
                            'type': 'heartbeat_notify',
                            'from_user': handler.user_id,
                            'timestamp': datetime.now().isoformat()
                        })
                    except Exception as e:
                        print(f"心跳发送失败: {str(e)}")
                        cls.clean_connection(handler, target_id)
                else:
                    await handler.write_message({
                        'type': 'heartbeat_status',
                        'target_user': target_id,
                        'online': bool(target_conn),
                        'timestamp': datetime.now().isoformat()
                    })

        except Exception as e:
            print(f"心跳处理异常: {str(e)}")
            await handler.write_message({
                'type': 'error',
                'message': 'heartbeat processing failed',
                'details': str(e)
            })

    @classmethod
    async def handle_group_heartbeat(cls, handler, msg_data):
        """
        处理群组心跳（线程安全版）

        Args:
            handler: WebSocketHandler实例
            msg_data: {
                "target_user_ids": ["user1", "user2"],
                "custom_data": {}  # 可选附加数据
            }
        """
        try:
            target_ids = msg_data.get('target_user_ids', [])
            if not target_ids:
                await handler.write_message({
                    "type": "error",
                    "message": "target_user_ids cannot be empty"
                })
                return

            stats = {
                "total": len(target_ids),
                "success": 0,
                "failed": 0,
                "details": []
            }

            with handler._pool_lock:
                pool = handler.connected_users.get('default', {})

                for uid in target_ids:
                    record = {"user_id": uid, "status": "failed"}
                    conn = pool.get(uid)
                    print(f"[INFO] 检查用户 {uid} 的连接状态")

                    if conn:
                        try:
                            # 连接状态检查（兼容Tornado 5.0+）
                            is_active = not getattr(conn, 'close_code', None)

                            if is_active:
                                await conn.write_message({
                                    "type": "group_heartbeat_ack",
                                    "from": handler.user_id,
                                    "timestamp": datetime.now().isoformat(),
                                    **msg_data.get('custom_data', {})
                                })
                                stats["success"] += 1
                                record["status"] = "success"
                            else:
                                del pool[uid]  # 清理无效连接
                        except Exception as e:
                            print(f"[ERROR] 心跳发送失败 {uid}: {str(e)}")
                            del pool[uid]
                    else:
                        record["reason"] = "not_connected"

                    stats["details"].append(record)

            # 返回详细报告
            await handler.write_message({
                "type": "group_heartbeat_result",
                "timestamp": datetime.now().isoformat(),
                "stats": stats
            })

        except Exception as e:
            print(f"[CRITICAL] 群组心跳处理异常: {str(e)}")
            await handler.write_message({
                "type": "error",
                "message": "group heartbeat failed",
                "details": str(e)[:200]  # 防止超长错误信息
            })

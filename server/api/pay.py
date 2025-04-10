from decimal import Decimal, getcontext
from base_api import BaseApi
from django.http import JsonResponse
from datetime import datetime, timedelta, timezone

# 设置Decimal精度上下文
getcontext().prec = 14


class OrderService(BaseApi):
    """订单服务基类（自动生成goods_id版本）"""

    def __init__(self, request, user_id, amount, order_data):
        self.request = request
        self.user_id = user_id
        self.amount = Decimal(str(amount))
        self.order_data = order_data
        # 系统自动生成唯一订单ID
        self.order_id = self.get_uuid()
        # 确保订单数据中包含生成的goods_id
        self.order_data['goods_id'] = self.order_id

    def validate_order_data(self):
        """验证订单数据完整性（不再验证goods_id）"""
        required_fields = {
            'system': ['type', 'amount_of_money','user_id'],  # 系统订单必填字段
            'user': ['type', 'amount_of_money', 'user_id', 'target_user_id', 'work_type']  # 用户订单必填字段
        }

        order_type = 'system' if self.order_data.get('type') == 'vip' else 'user'
        for field in required_fields[order_type]:
            if not self.order_data.get(field):
                raise ValueError(f'缺少必填字段: {field}')

        if self.amount <= Decimal('0'):
            raise ValueError('金额必须大于0')

    def create_order(self):
        """创建订单记录（使用自动生成的goods_id）"""
        fields = [
            'type', 'amount_of_money', 'user_id', 'target_user_id',
            'goods_id', 'status', 'work_type', 'work_introduce', 'back',
            'age_classification'
        ]

        params = {
            'time': datetime.now(),
            'status': 2,  # 默认状态：待处理
            'goods_id': self.order_id  # 使用自动生成的ID
        }

        # 合并传入的订单数据
        params.update({k: v for k, v in self.order_data.items() if k in fields})
        params['amount_of_money'] = str(self.amount)

        # 构建动态SQL
        columns = []
        values = []
        for col in fields + ['time']:
            if col in params:
                columns.append(col)
                values.append(params[col])

        sql = f'''
        INSERT INTO admin.`order` 
        ({", ".join(columns)}) 
        VALUES ({", ".join(["%s"] * len(values))})
        '''

        return self.execute_sql(sql, values, False) == 1

    def check_balance(self):
        """检查用户余额（返回Decimal）"""
        sql = 'SELECT balance FROM admin.money WHERE user_id = %s'
        result = self.execute_sql(sql, self.user_id)
        return Decimal(str(result[0]['balance'])) if result else Decimal('0')

    def deduct_balance(self, amount):
        """扣除用户余额"""
        now = datetime.now(timezone.utc)
        sql = 'UPDATE admin.money SET balance = balance - %s,last_update=%s WHERE user_id = %s'
        return self.execute_sql(sql, [str(amount), now, self.user_id], False) == 1

    def complete_order(self):
        """完成订单（使用实例保存的goods_id）"""
        sql = 'UPDATE admin.order SET status = 1 WHERE goods_id = %s'
        return self.execute_sql(sql, [self.order_id], False) == 1


class VipOrderService(OrderService):
    """VIP订单服务（系统订单）"""
    VIP_TYPES = {
        '1d': {'days': 1, 'price': '0.5'},
        '1w': {'days': 7, 'price': '3.43'},
        '1m': {'days': 30, 'price': '13.5'},
        '3m': {'days': 90, 'price': '36.0'},
        '6m': {'days': 180, 'price': '63.0'},
        '1y': {'days': 365, 'price': '91.25'}
    }

    def __init__(self, request, user_id, order_data):
        vip_type = order_data.get('back')  # VIP类型存储在back字段
        vip_info = self.VIP_TYPES.get(vip_type)
        if not vip_info:
            raise ValueError('无效的VIP类型')

        # 设置系统订单数据
        order_data.update({
            'type': 'vip',
            'amount_of_money': vip_info['price'],
            'back': vip_type,# VIP类型存储在back字段
            'user_id':request.user.id
        })

        super().__init__(request, user_id, Decimal(vip_info['price']), order_data)
        self.vip_days = vip_info['days']

    def get_current_vip_status(self):
        """获取当前VIP状态和到期时间"""
        sql = '''
        SELECT vip, vip_last_date 
        FROM admin.users 
        WHERE userid = %s
        '''
        result = self.execute_sql(sql, [self.user_id])
        if result:
            return {
                'is_vip': result[0]['vip'] == 1,  # 明确使用1判断VIP状态
                'expiry_date': result[0]['vip_last_date']
            }
        return {'is_vip': False, 'expiry_date': None}

    def calculate_new_expiry(self):
        """计算新的VIP到期时间"""
        current_status = self.get_current_vip_status()
        now = datetime.now(timezone.utc)

        # 如果不是VIP或已过期，从当前时间开始计算
        if not current_status['is_vip'] or not current_status['expiry_date'] or current_status['expiry_date'] < now:
            new_expiry = now + timedelta(days=self.vip_days)
        else:
            # 如果是VIP且未过期，在原有到期时间上增加
            new_expiry = current_status['expiry_date'] + timedelta(days=self.vip_days)

        return new_expiry

    def activate_vip(self):
        """激活VIP会员"""
        new_expiry = self.calculate_new_expiry()

        sql = '''
        UPDATE admin.users 
        SET vip = 1, vip_last_date = %s 
        WHERE userid = %s
        '''
        return self.execute_sql(sql, [new_expiry, self.user_id], False) == 1

    def process(self):
        """处理VIP订单"""
        try:
            self.validate_order_data()
            balance = self.check_balance()

            if balance < self.amount:
                return {'code': 410, 'msg': '余额不足'}

            if not self.create_order():
                return {'code': 500, 'msg': '创建订单失败'}

            if not self.complete_order():
                return {'code': 500, 'msg': '完成订单失败'}

            if not self.deduct_balance(self.amount):
                return {'code': 500, 'msg': '扣除余额失败'}

            if not self.activate_vip():
                return {'code': 500, 'msg': '激活VIP失败'}

            return {'code': 200, 'msg': 'VIP开通成功'}

        except ValueError as e:
            print(e)
            return {'code': 400, 'msg': str(e)}
        except Exception as e:
            print(e)
            return {'code': 500, 'msg': f'服务器错误: {str(e)}'}


class UserOrderService(OrderService):
    """用户订单服务"""

    def __init__(self, request, user_id, order_data):
        super().__init__(request, user_id, Decimal(str(order_data['amount_of_money'])), order_data)

    def process(self):
        """处理用户订单"""
        try:
            self.validate_order_data()

            # 用户订单需要检查更多字段
            if not self.order_data.get('target_user_id'):
                return {'code': 400, 'msg': '必须指定目标用户'}

            if not self.order_data.get('work_type'):
                return {'code': 400, 'msg': '必须指定作品类型'}

            balance = self.check_balance()
            if balance < self.amount:
                return {'code': 410, 'msg': '余额不足'}

            if not self.create_order():
                return {'code': 500, 'msg': '创建订单失败'}

            if not self.complete_order():
                return {'code': 500, 'msg': '完成订单失败'}

            if not self.deduct_balance(self.amount):
                return {'code': 500, 'msg': '扣除余额失败'}

            return {'code': 200, 'msg': '订单处理成功'}
        except Exception as e:
            print(f"用户订单处理失败: {str(e)}")
            return {'code': 500, 'msg': '订单处理异常'}


class OrderHandler(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.user.is_login:
                return JsonResponse(
                    {'code': 401, 'msg': '未登录'},
                    status=401
                )

            data = self.format_request(request)
            user_id = request.user.id

            # 根据订单类型路由
            if data.get('type') == 'vip':
                if self.validate_pay_password(request,data) is False:
                    return JsonResponse(
                        {'code': 401, 'msg': '支付密码错误'},
                        status=401
                    )
                elif self.validate_pay_password(request,data) is True:
                    service = VipOrderService(request, user_id, data)
                else:
                    return self.validate_pay_password(request,data)

            else:
                service = UserOrderService(request, user_id, data)

            result = service.process()
            return JsonResponse(result, status=result['code'])

        except ValueError as e:
            return JsonResponse(
                {'code': 400, 'msg': str(e)},
                status=400
            )
        except Exception as e:
            print(f"订单处理异常: {str(e)}")
            self.error_log(e, request)
            return JsonResponse(
                {'code': 500, 'msg': '服务器内部错误'},
                status=500
            )
        # 验证支付密码

    def validate_pay_password(self,request,order_data):
        sql = '''select pay_password from admin.money where user_id=%s'''
        pay_password = self.execute_sql(sql, [request.user.id])
        print('用户支付密码',pay_password)
        if not pay_password or len(pay_password) == 0:
            print('用户支付密码为空')
            return JsonResponse({'code':411,'msg':'请先初始化钱包，并设置支付密码'},status=411)
        password = order_data.get('pay_password')
        if password != pay_password[0]['pay_password']:
            return False
        else:
            return True

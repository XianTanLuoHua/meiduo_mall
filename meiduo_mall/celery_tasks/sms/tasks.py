

from meiduo_mall.celery_tasks.main import celery_app
from meiduo_mall.libs.yuntongxun.ccp_sms import CCP


@celery_app.task(bind=True, name='ccp_send_sms_code', retry_backoff=3)

def ccp_send_sms_code(self, mobile, sms_code):
    try:
        result = CCP().send_template_sms(mobile,
                                         [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60],
                                         constants.SEND_SMS_TEMPLATE_ID)
        pass
    except:
        pass
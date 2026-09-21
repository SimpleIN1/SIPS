import logging
import pprint

from core.services.redis_service import async_redis_client, sync_redis_client


async def get_all_logs_stream(run_id: str):
    messages = await async_redis_client.xrevrange(f"app_logs_stream_{run_id}")
    messages.reverse()
    return {
        "type": "all_logs_stream",
        "messages": messages,
    }


def transform_redis_logs_stream_to_str(run_id: str) -> str:
    # logging.info("Чтение логов с redis")
    messages = sync_redis_client.xrevrange(f"app_logs_stream_{run_id}")
    messages.reverse()
    sync_redis_client.delete(f"app_logs_stream_{run_id}")
    return "\n".join(map(lambda x: x[1]["message"], messages))


def get_type_line(line: str) -> str:
    line_class = ''
    if 'STEP:' in line:
        line_class = 'log-step'
    elif 'PROGRESS:' in line:
        line_class = 'log-progress'
    elif 'Ошибка' in line or 'Error' in line or line.startswith('❌'):
        line_class = 'log-error'
    elif 'завершено' in line.lower() or line.startswith('✅'):
        line_class = 'log-success'

    return line_class

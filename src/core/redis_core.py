import asyncio
import aioredis as rc


async def update_death_count(death_count):
    redis = await rc.create_redis_pool("redis://localhost:6379")

    data = await redis.get('covid_deaths', encoding="utf-8")
    if(data == None):
        redis.set("covid_deaths", death_count)
    else:
        redis.set('covid_deaths', int(data) + death_count)

    print("Death count is now on: " + data)
    redis.close()
    await redis.wait_closed()

async def get_death_count():
    redis = await rc.create_redis_pool("redis://localhost:6379")

    death_count = await redis.get('covid_deaths', encoding="utf-8")

    if(death_count == None):
        return 0
    else:
        return death_count
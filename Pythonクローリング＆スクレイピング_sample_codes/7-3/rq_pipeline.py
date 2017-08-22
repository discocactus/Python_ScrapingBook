from redis import Redis
from rq import Queue


class RQPipeline:
    """
    RQにジョブを投入するPipeline。
    """

    def open_spider(self, spider):
        """
        Spiderの開始時にRedisに接続してQueueオブジェクトを取得する。
        """

        self.queue = Queue(connection=Redis())

    def process_item(self, item, spider):
        """
        RQにジョブを投入する。
        """

        self.queue.enqueue('scraper_tasks.scrape', item['key'], result_ttl=0)
        return item

import logging

from collections import namedtuple

from sense_server.settings import ELASTIC_SEARCH_HOST, ELASTIC_SEARCH_PORT

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import HTTP_EXCEPTIONS

LOG = logging.getLogger(__name__)

es_client = Elasticsearch(hosts=[{"host": ELASTIC_SEARCH_HOST, "port": ELASTIC_SEARCH_PORT}])


def es_result_to_list(result):
    if result is None:
        return []
    if result.get("hits"):

        data = result['hits']['hits']
        posts = []
        for d in data:
            p = Post.new_post(id=d['_id'],
                              url=d['_source']['url'],
                              timestamp=d['_source']['timestamp'],
                              document=d['_source']['document'])
            posts.append(p)

        return map(lambda x: x._asdict(), posts)
    else:
        if not result.get("_source"):
            return []
        p = Post.new_post(id=result['_id'],
                          url=result['_source']['url'],
                          timestamp=result['_source']['timestamp'],
                          document=result['_source']['document'])
        return [p._asdict()]


def es_query(index, **kwargs):
    return es_result_to_list(es_client.search(index=index, doc_type=kwargs.get("doc_type"), params={"offsets": -1}))


def fetch_post(index, id):
    try:

        result = es_client.get(index, id=id, doc_type="post")
    except HTTP_EXCEPTIONS[404] as e:
        LOG.error("Fetch post from index `%s` id `%s` failure, not found", index, id)
        return None

    posts = es_result_to_list(result)
    if len(posts) > 0:
        return posts[0]
    else:
        return None


def update_post(index, id, body):
    return es_result_to_list(es_client.index(index, doc_type="post", body=body, id=id))


class Post(namedtuple("_Post", ["id", "url", "timestamp", "document"
                                ])):
    @staticmethod
    def new_post(id, url, timestamp, document):
        return Post(id=id, url=url, timestamp=timestamp, document=document)

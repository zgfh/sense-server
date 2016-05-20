from .elastic_search import es_query, fetch_post, update_post

import model
from functools import partial

backup_index = "backup_v2ex"
master_index = "v2ex"
post_doc_type = "post"

fetch_post_from_master_index = partial(fetch_post, master_index)
fetch_post_from_backup_index = partial(fetch_post, backup_index)
backup_read_post = partial(update_post, backup_index)


def is_new(cur, pre):
    if pre is None or cur["document"]["update_ts"] > pre["document"]["update_ts"]:
        return True

    if cur["document"]["comments_num"] == pre["document"]["comments_num"]:
        return False

    return True


def simplify_post(post):
    p = model.get_post(post['id'])
    if p:
        post['is_favorite'] = p.is_favorite
    else:
        post['is_favorite'] = False

    return p or post


def list_post(read=False):
    if read:
        raw_data = es_query(index=backup_index, doc_type=post_doc_type)
    else:
        all_posts = es_query(index=master_index, doc_type=post_doc_type)
        raw_data = filter(lambda x: is_new(x, fetch_post_from_backup_index(x["id"])), all_posts)
    return map(simplify_post, raw_data)


def remove_favorites(ids):
    model.remove_favorites(ids)


def read_post(id):
    model.read_post(id)
    post = fetch_post_from_master_index(id)
    if post is None:
        return {}
    backup_read_post(id, post)
    model.read_post(id)
    return post


def unread_post(id):
    model.unread_post(id)


def list_favorites():
    posts = map(lambda x: x.to_dict(), model.list_favorite_post())
    map(lambda x: x.update(fetch_post_from_master_index(x['id'])), posts
        )
    return posts


def add_favorites(ids):
    model.add_favorites(ids)

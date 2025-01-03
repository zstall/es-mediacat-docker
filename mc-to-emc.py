import psycopg2
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# Script to manually index DB to ES
def main():
    conn = psycopg2.connect(dbname="mc", user="admin", password="admin", host="postgres")
    cursor=conn.cursor()
    cursor.execute("select * from files")
    rows=cursor.fetchall()
    columns=[desc[0] for desc in cursor.description]
    data_to_index = [dict(zip(columns, row)) for row in rows]


    es=Elasticsearch(basic_auth=["elastic", "TtmooQ6-=jR9tU5WHdcZ"],hosts="https://elasticsearch:9200", verify_certs=False)
    index_name="emc"
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)

    actions = [
                {
                    "_index":"emc",
                    "_source": data,
                }
                for data in data_to_index
            ]
    result = bulk(es, actions)
    print(result)

if __name__ in "__main__":
    main()
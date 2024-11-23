dataVec向量数据库测试
1.创建一个有三维向量的表
CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));

openGauss=# CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));
NOTICE:  CREATE TABLE will create implicit sequence "items_id_seq" for serial column "items.id"
NOTICE:  CREATE TABLE / PRIMARY KEY will create implicit index "items_pkey" for table "items"
CREATE TABLE
2.插入向量数据

INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]'), ('[7,8,9]'), ('[10,11,12]'), ('[13,14,15]');

openGauss=# INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]'), ('[7,8,9]'), ('[10,11,12]'), ('[13,14,15]');
INSERT 0 5
3.更新向量数据
UPDATE items SET embedding = '[1,2,3]' WHERE id = 1;

openGauss=# UPDATE items SET embedding = '[1,2,3]' WHERE id = 1;
UPDATE 1
4.删除向量数据
DELETE FROM items WHERE id = 1;

openGauss=# DELETE FROM items WHERE id = 1;
DELETE 1
5.获取最近邻
SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;

openGauss=# SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;
 id | embedding----+------------
  2 | [4,5,6]
  3 | [7,8,9]
  4 | [10,11,12]
  5 | [13,14,15]
(4 rows)
6.获取距离
SELECT embedding <-> '[3,1,2]' AS distance FROM items;

openGauss=# SELECT embedding <-> '[3,1,2]' AS distance FROM items;
     distance

------------------
 5.74456264653803
 10.6770782520313
 15.7797338380595
 20.9284495364563
7.平均矢量
SELECT AVG(embedding) FROM items;

openGauss=# SELECT AVG(embedding) FROM items;
      avg

----------------
 [8.5,9.5,10.5]
(1 row)dataVec向量数据库测试
1.创建一个有三维向量的表
CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));

openGauss=# CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));
NOTICE:  CREATE TABLE will create implicit sequence "items_id_seq" for serial column "items.id"
NOTICE:  CREATE TABLE / PRIMARY KEY will create implicit index "items_pkey" for table "items"
CREATE TABLE
2.插入向量数据

INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]'), ('[7,8,9]'), ('[10,11,12]'), ('[13,14,15]');

openGauss=# INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]'), ('[7,8,9]'), ('[10,11,12]'), ('[13,14,15]');
INSERT 0 5
3.更新向量数据
UPDATE items SET embedding = '[1,2,3]' WHERE id = 1;

openGauss=# UPDATE items SET embedding = '[1,2,3]' WHERE id = 1;
UPDATE 1
4.删除向量数据
DELETE FROM items WHERE id = 1;

openGauss=# DELETE FROM items WHERE id = 1;
DELETE 1
5.获取最近邻
SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;

openGauss=# SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;
 id | embedding----+------------
  2 | [4,5,6]
  3 | [7,8,9]
  4 | [10,11,12]
  5 | [13,14,15]
(4 rows)
6.获取距离
SELECT embedding <-> '[3,1,2]' AS distance FROM items;

openGauss=# SELECT embedding <-> '[3,1,2]' AS distance FROM items;
     distance

------------------
 5.74456264653803
 10.6770782520313
 15.7797338380595
 20.9284495364563
7.平均矢量
SELECT AVG(embedding) FROM items;

openGauss=# SELECT AVG(embedding) FROM items;
      avg

----------------
 [8.5,9.5,10.5]
(1 row)
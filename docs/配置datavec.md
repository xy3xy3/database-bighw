https://opengauss.org/zh/blogs/%E9%A3%8E%E4%B8%80%E6%A0%B7%E8%87%AA%E7%94%B1/openGauss%206.0.0-RC1%20dataVec%E5%90%91%E9%87%8F%E6%95%B0%E6%8D%AE%E5%BA%93%E6%B5%8B%E8%AF%95.html

create extension datavec;


select * from pg_extension where extname='datavec';

测试

INSERT INTO knowledge_content (embedding) VALUES ('[1,2,3]'), ('[4,5,6]'), ('[7,8,9]'), ('[10,11,12]'), ('[13,14,15]');
SELECT embedding <-> '[3,1,2]' AS distance FROM knowledge_content;

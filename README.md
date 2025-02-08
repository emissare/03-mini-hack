# 03-mini-hack


SO
Python
- Q score above 10
- A score above 5
Results: 68,248




SELECT 
    q.id AS question_id, 
    q.title AS question_title, 
    q.body AS question_body, 
    q.creation_date AS question_creation_date, 
    q.score AS question_score, 
    q.view_count, 
    q.tags, 
    a.id AS answer_id, 
    a.body AS answer_body, 
    a.creation_date AS answer_creation_date, 
    a.score AS answer_score, 
    a.owner_user_id AS answer_owner_user_id
FROM `bigquery-public-data.stackoverflow.posts_questions` q
JOIN `bigquery-public-data.stackoverflow.posts_answers` a
ON q.id = a.parent_id
WHERE LOWER(q.tags) LIKE '%python%'
    AND q.score >= 10 
    AND a.score >= 5  
QUALIFY ROW_NUMBER() OVER (PARTITION BY q.id ORDER BY a.score DESC) = 1
LIMIT 100000;
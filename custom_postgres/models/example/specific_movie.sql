{% set film_title = 'The Godfather' %}

SELECT *
FROM {{ ref('films') }}
WHERE title = '{{ film_title }}'
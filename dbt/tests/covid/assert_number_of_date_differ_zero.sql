SELECT      COUNT("DateKey") as count_value
FROM        {{ ref('Date') }}
HAVING      NOT(COUNT("DateKey") > 0)
SELECT      COUNT("CovidCaseKey") as count_value
FROM        {{ ref('CovidCase') }}
HAVING      NOT(COUNT("CovidCaseKey") > 0)
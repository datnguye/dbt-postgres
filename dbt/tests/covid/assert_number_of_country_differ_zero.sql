SELECT      COUNT("CountryKey") as count_value
FROM        {{ ref('Country') }}
HAVING      NOT(COUNT("CountryKey") > 0)
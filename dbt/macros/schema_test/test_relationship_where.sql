{#-- Cloned from https://github.com/dbt-labs/dbt-utils/blob/a7290442b401cdfb930d1f527cb9782022d867d9/macros/schema_tests/relationships_where.sql#}

{% macro test_relationship_where(model, column_name, to, field, from_condition="1=1", to_condition="1=1") %}

select      left_table.id,
            right_table.id as right_id
from        (
                select  {{column_name}} as id
                from    {{model}}
                where   {{column_name}} is not null
                    and {{from_condition}}
            ) as left_table
left join   (
                select  {{field}} as id
                from    {{to}}
                where   {{field}} is not null
                    and {{to_condition}}
            ) as right_table
    on      left_table.id = right_table.id
where       right_table.id is null

{% endmacro %}
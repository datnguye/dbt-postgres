{#-- Cloned from https://github.com/dbt-labs/dbt-utils/blob/a7290442b401cdfb930d1f527cb9782022d867d9/macros/schema_tests/unique_combination_of_columns.sql #}
{% macro test_unique_combination_of_columns(model, combination_of_columns, quote_columns=false) %}

{% if not quote_columns %}
    {%- set column_list=combination_of_columns %}
{% elif quote_columns %}
    {%- set column_list=[] %}
        {% for column in combination_of_columns -%}
            {% set column_list = column_list.append( adapter.quote(column) ) %}
        {%- endfor %}
{% else %}
    {{ exceptions.raise_compiler_error(
        "`quote_columns` argument for unique_combination_of_columns test must be one of [True, False] Got: '" ~ quote ~"'.'"
    ) }}
{% endif %}

{%- set columns_csv=column_list | join(', ') %}

select
    {{ columns_csv }}
from {{ model }}
group by {{ columns_csv }}
having count(*) > 1

{% endmacro %}
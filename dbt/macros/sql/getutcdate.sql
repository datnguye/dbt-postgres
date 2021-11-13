{% macro getutcdate(db='postgresql') %}
    {%- if db == "postgresql" -%}
    now() at time zone 'utc'
    {%- elif db == "mssql" -%}
    getutcdate()
    {%- endif -%}
{% endmacro %}
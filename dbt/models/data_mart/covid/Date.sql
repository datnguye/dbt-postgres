{{ config(alias='Date', unique_key='"DateKey"') }}

{% if is_incremental() %}
    {%- call statement('get_lastest_time', fetch_result=True) -%}
        SELECT MAX("LastUpdatedTimestamp") FROM {{ this }}
    {%- endcall -%}
    {%- set lastest_time = load_result('get_lastest_time')['data'][0][0] -%}
{% endif %}

SELECT  DISTINCT 
        {{ dbt_utils.surrogate_key(['"UpdatedDate"']) }} as "DateKey",
        {{getutcdate()}} as "LastUpdatedTimestamp",

        "UpdatedDate" as "Date Value",
        DATE_PART('day', "UpdatedDate") as "Day",
        DATE_PART('month', "UpdatedDate") as "Month",
        TO_CHAR("UpdatedDate", 'month') as "Month Name",
        'Q' || CAST(DATE_PART('quarter', "UpdatedDate") as varchar) as "Quarter",
        DATE_PART('year', "UpdatedDate") as "Year"

FROM    {{ref('ODS_Covid_Case')}}

WHERE   1=1
{% if is_incremental() %}
AND     (
            --update once a day
            CAST({{getutcdate()}} as date) > CAST('{{lastest_time}}' as date)
        )
{% endif %}
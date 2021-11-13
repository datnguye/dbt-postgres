{{ config(schema='ods', alias='ODS_Covid_Case', unique_key='"CovidCaseKey"') }}

{% if is_incremental() %}
    {%- call statement('get_lastest_time', fetch_result=True) -%}
        SELECT MAX("UpdatedDate") FROM {{ this }}
    {%- endcall -%}
    {%- set lastest_time = load_result('get_lastest_time')['data'][0][0] -%}
{% endif %}

SELECT  {{ dbt_utils.surrogate_key(['"Continent"', '"Country"', '"UpdatedDate"']) }} as "CovidCaseKey",
        
        "Continent",
        "Country",
        "UpdatedDate",
        "TotalCase",
        "NewCase",
        "TotalDeath",
        "NewDeath",

        {{getutcdate()}} as "LastUpdatedTimestamp"

FROM    {{ref('STAG_Covid_Data')}}

WHERE   1=1
{% if is_incremental() %}
AND     (
            "UpdatedDate" >= '{{lastest_time}}'
        )
{% endif %}
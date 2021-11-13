{{ config(alias='CovidCase', unique_key='"CovidCaseKey"') }}

{% if is_incremental() %}
    {%- call statement('get_lastest_time', fetch_result=True) -%}
        SELECT MAX("LastUpdatedTimestamp") FROM {{ this }}
    {%- endcall -%}
    {%- set lastest_time = load_result('get_lastest_time')['data'][0][0] -%}
{% endif %}

SELECT  CC."CovidCaseKey",
        C."CountryKey",
        D."DateKey",
        {{getutcdate()}} as "LastUpdatedTimestamp",

        CC."TotalCase" as "Total Case",
        CC."NewCase" as "New Case",
        CC."TotalDeath" as "Total Death",
        CC."NewDeath" as "New Death"

FROM    {{ref('ODS_Covid_Case')}} as CC 
JOIN    {{ref('Country')}} as C
    ON  C."Country" = CC."Country"
    AND C."Continent" = CC."Continent"
JOIN    {{ref('Date')}} as D
    ON  D."Date Value" = CC."UpdatedDate"

WHERE   1=1
{% if is_incremental() %}
AND     (
            --update once a day
            CAST({{getutcdate()}} as date) > CAST('{{lastest_time}}' as date)
        )
{% endif %}
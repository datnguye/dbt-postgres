{{ config(alias='Country', unique_key='"CountryKey"') }}

{% if is_incremental() %}
    {%- call statement('get_lastest_time', fetch_result=True) -%}
        SELECT MAX("LastUpdatedTimestamp") FROM {{ this }}
    {%- endcall -%}
    {%- set lastest_time = load_result('get_lastest_time')['data'][0][0] -%}
{% endif %}

SELECT  "CountryKey",
        {{getutcdate()}} as "LastUpdatedTimestamp",

        "CountryCode"     as "Country Code",
        "Continent"       as "Continent",
        "Country"         as "Country"

FROM    {{ref('ODS_Country')}}

WHERE   1=1
{% if is_incremental() %}
AND     (
            --update once a day
            CAST({{getutcdate()}} as date) > CAST('{{lastest_time}}' as date)
        )
{% endif %}
{{ config(schema='staging', alias='STAG_Covid_Data', unique_key='"CovidDataKey"') }}

{% if is_incremental() %}
    {%- call statement('get_lastest_time', fetch_result=True) -%}
        SELECT MAX("UpdatedDate") FROM {{ this }}
    {%- endcall -%}
    {%- set lastest_time = load_result('get_lastest_time')['data'][0][0] -%}
{% endif %}

SELECT  DISTINCT 
        {{ dbt_utils.surrogate_key(['continent', 'location', 'last_updated_date']) }} as "CovidDataKey",

        iso_code::varchar(3)                        as "CountryCode",
        continent::varchar(255)                     as "Continent",
        location::varchar(255)                      as "Country",
        last_updated_date::date                     as "UpdatedDate",
        COALESCE(total_cases::decimal(17,0),0)      as "TotalCase",
        COALESCE(new_cases::decimal(17,0),0)        as "NewCase",
        COALESCE(total_deaths::decimal(17,0),0)     as "TotalDeath",
        COALESCE(new_deaths::decimal(17,0),0)       as "NewDeath",

        {{getutcdate()}} as "LastUpdatedTimestamp"

FROM    {{ref('covid_raw')}}
WHERE   continent IS NOT NULL

{% if is_incremental() %}
AND     (
            last_updated_date::date >= '{{lastest_time}}'
        )
{% endif %}
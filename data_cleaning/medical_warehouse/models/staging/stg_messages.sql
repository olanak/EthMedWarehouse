-- models/staging/stg_messages.sql
{{ config(materialized='table') }}

WITH raw_data AS (
    SELECT
        id,
        channel_name,
        TRIM(message_text) AS cleaned_text,
        COALESCE(scraped_at, CURRENT_TIMESTAMP) AS cleaned_scraped_at,
        MD5(CONCAT(channel_name, TRIM(message_text))) AS message_hash
    FROM {{ source('public', 'raw_messages') }}
    WHERE TRIM(message_text) != ''
),

ranked_messages AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY message_hash 
            ORDER BY cleaned_scraped_at DESC
        ) AS rn
    FROM raw_data
)

SELECT
    id,
    channel_name,
    cleaned_text,
    cleaned_scraped_at,
    message_hash
FROM ranked_messages
WHERE rn = 1  -- Keep only the latest record per duplicate
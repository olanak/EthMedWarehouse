-- models/example/staging/stg_images.sql
{{ config(materialized='table') }}

SELECT
    id,
    channel_name,
    CASE
        WHEN image_path ~ '^data/images/[A-Za-z0-9_-]+/.*\.(jpg|png)$' 
        THEN image_path
        ELSE NULL 
    END AS valid_image_path,
    COALESCE(TRIM(caption), 'No caption') AS cleaned_caption,
    scraped_at AS cleaned_scraped_at
FROM {{ source('public', 'raw_images') }}
WHERE image_path IS NOT NULL
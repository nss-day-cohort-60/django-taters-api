SELECT "rareapi_post"."id",
    "rareapi_post"."author_id",
    "rareapi_post"."category_id",
    "rareapi_post"."title",
    "rareapi_post"."publication_date",
    "rareapi_post"."image_url",
    "rareapi_post"."content",
    "rareapi_post"."approved"
FROM "rareapi_post"
WHERE "rareapi_post"."author_id" IN (
        SELECT U0."id"
        FROM "rareapi_author" U0
            INNER JOIN "rareapi_subscription" U1 ON (U0."id" = U1."author_id")
            INNER JOIN "rareapi_author" U2 ON (U1."subscriber_id" = U2."id")
        WHERE U2."user_id" = 2
    )
ORDER BY "rareapi_post"."publication_date" DESC
# Supabase Connection

## Project

- **URL**: https://qqchfqxtmuttqbkbmmxt.supabase.co
- **Storage Bucket**: `public`

## Database (PostgreSQL)

```
postgresql://postgres:EZtGD5pJqbLTNu.@db.qqchfqxtmuttqbkbmmxt.supabase.co:5432/postgres
```

> Note: The database host resolves to IPv6 only. Works on cloud servers (Render, etc.) but may not work on local networks without IPv6.

## Storage

Files are uploaded to Supabase Storage and served via public URLs:

```
https://qqchfqxtmuttqbkbmmxt.supabase.co/storage/v1/object/public/public/{course_id}/{file}
```

## Environment Variables

Set these in `.env` (local) or in your hosting platform's environment:

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string (leave blank for local SQLite) |
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_KEY` | Supabase service role key |
| `SUPABASE_BUCKET` | Storage bucket name (`public`) |

## Local Development

- **Database**: SQLite (fallback when `DATABASE_URL` is not set)
- **File Storage**: Supabase Storage (via HTTPS API)

## Deployment (Render)

- Set `DATABASE_URL` to the PostgreSQL connection string above
- Set `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_BUCKET`
- Both database and file storage will use Supabase

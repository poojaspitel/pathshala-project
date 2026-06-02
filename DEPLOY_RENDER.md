Render deployment checklist for this Django app

1) Add build & start settings in Render
- Connect repository to Render and create a new Web Service.
- Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- Start Command: Leave blank (Procfile used) or set: `gunicorn web.wsgi --log-file -`
- Environment: Python 3.11+ recommended.

2) Provision a managed Postgres database on Render
- In Render dashboard, create a new Postgres database and note the `DATABASE_URL`.
- In your Web Service settings, set an environment variable `DATABASE_URL` to that value.

3) (Optional) Configure persistent media
Option A — Recommended (S3):
- Create an S3 bucket and IAM user with `s3:PutObject`, `s3:GetObject`, `s3:ListBucket`.
- Set these env vars in Render for the Web Service:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_S3_BUCKET_NAME`
  - (optional) `AWS_S3_REGION_NAME`
- The app will automatically use `storages.backends.s3boto3.S3Boto3Storage` when `AWS_S3_BUCKET_NAME` is present.

Option B — Render Persistent Disk:
- Configure a persistent volume and mount it to the service path used for `MEDIA_ROOT` (`/srv/web/media` for example).
- Update `MEDIA_ROOT` in settings to match the mounted path.

4) Deploy and run migrations
- After setting `DATABASE_URL`, deploy the service (or open a Shell in Render) and run:

```bash
# In Render shell or during a one-off deploy step
python manage.py migrate
python manage.py collectstatic --noinput
```

5) Verify
- Visit the app, create a record with an uploaded photo.
- Check the Postgres DB (via Render dashboard) to confirm rows are persisted.
- Verify uploaded media is present in S3 or the persistent disk.

6) Optional: Migrate existing sqlite data to Postgres
- Locally, create a dump of the sqlite DB or use `dumpdata`:

```bash
python manage.py dumpdata --natural-primary --natural-foreign --indent 2 > alldata.json
```

- On Render (after migrations), upload `alldata.json` and run:

```bash
python manage.py loaddata alldata.json
```

If you've committed `alldata.json` into the repository (as included here), you can run the `loaddata` command directly in the Render shell after deploying and applying migrations.

Notes & Troubleshooting
- Ensure `ALLOWED_HOSTS` includes your Render service domain or set it to `['*']` temporarily while testing.
- If `collectstatic` fails, ensure `STATIC_ROOT` exists and is writable.
- For S3, make sure the bucket policy allows public reads if you want direct public media URLs, or configure CloudFront.

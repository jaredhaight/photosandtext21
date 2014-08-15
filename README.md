##Photos and Text 2.1

Photos and Text 2.0 got too complicated. It was buggy, slow and didn't do what I had set out for it to do. I decided to scrap everything except some HTML templates and start over.

This revision, I'm trying to keep the focus on keeping things simple. Instead of an import page, a script runs that collects any photos in the /uploads directory and adds them to the DB. For deployment, the whole site is rendered out to static HTML, and then pushed into S3 for hosting.

Nice and simple.

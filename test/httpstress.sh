seq 1000 | xargs -I@ -n1 curl -so /dev/null -w "%{time_connect}\n" localhost/overview

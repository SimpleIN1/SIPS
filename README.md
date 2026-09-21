# SIPS

---

## Description
The web application is used for visualization and processing of VIIRS radiometer satellite data.

## Services

 - AccountService - http://127.0.0.1:8000/api/vaccount/docs/swagger/
 - AuthService - http://127.0.0.1:8001/api/vauth/docs/swagger/
 - InfoCompositeOutputDataRESTAPIService - http://127.0.0.1:8002/api/vicod/docs/swagger.json
 - CompositeDataRESTAPIService - http://127.0.0.1:8003/api/vcd/docs/swagger.json
 - DocsAgregatorSwaggerUI - http://127.0.0.1:8004/docs/swagger/
 - AlgorithmManagerService - http://127.0.0.1:8005/


## Settings nginx
    export $(xargs < .docker.nginx.env) && envsubst "$(echo $(vars=$(cut -d= -f1 .docker.nginx.env); echo "\$${vars}") | sed 's/ /,\$/g')" < ./nginx/conf.d/default.conf | sudo tee  /etc/nginx/conf.d/sips.conf
    sudo nginx -t
    sudo systemctl reload nginx.service
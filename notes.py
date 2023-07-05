

# https://github.com/CSM41-WEB/atividade-02-JordHisu/tree/master
# https://www.django-rest-framework.org/tutorial/2-requests-and-responses/
# https://awsacademy.instructure.com/courses/41555/modules


# docker build . -t jordhisu/django-rest-api
# docker image push jordhisu/django-rest-api
# docker compose up
# docker build . -t jordhisu/django-rest-api; docker image push jordhisu/django-rest-api; docker compose up
# docker compose run main /bin/bash

# docker run -it --entrypoint /bin/bash jordhisu/django-web-app-repo -s



# docker image tag django-rest-api jordhisu/django-rest-api



# Libera as portas na máquina virtual EC2
# sudo iptables -L
# sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
# docker run -d -p 8080:8080 jordhisu/django-rest-api


# No terminal local:
# ssh -i lab-web.pem ubuntu@<ec2_public_ip>

# No terminal ssh:
# docker pull jordhisu/django-rest-api
# docker stop $(docker ps -a -q) & docker ps & docker run -d -p 80:80 jordhisu/django-rest-api

# Acessar o site:
# http://<ec2_public_ip>:8080/



# docker build . -t jordhisu/django-rest-api; docker image push jordhisu/django-rest-api
# docker stop $(docker ps -a -q) ; docker rm $(docker ps -a -q) ; docker image prune -a --force
# docker pull jordhisu/django-rest-api ; docker run -p 8000:8000 jordhisu/django-rest-api
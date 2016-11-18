
FROM andrewrothstein/docker-ansible:alpine_edge
MAINTAINER "Andrew Rothstein" andrew.rothstein@gmail.com

RUN mkdir -p /role-to-test
ONBUILD ADD . /role-to-test
ONBUILD WORKDIR /role-to-test
<<<<<<< HEAD
ONBUILD RUN if [ -f requirements.yml ]; then ansible-galaxy install -r requirements.yml; fi
=======
ONBUILD RUN ansible-galaxy install -r requirements.yml
>>>>>>> shuffle supported upstreams
ONBUILD RUN ansible-playbook test.yml
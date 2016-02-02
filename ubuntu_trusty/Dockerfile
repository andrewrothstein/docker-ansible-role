
FROM andrewrothstein/docker-ansible:ubuntu_trusty
MAINTAINER "Andrew Rothstein" andrew.rothstein@gmail.com

RUN mkdir -p /role-to-test
ONBUILD ADD . /role-to-test
ONBUILD WORKDIR /role-to-rest
ONBUILD RUN ansible-galaxy install requirements.yml
ONBUILD RUN ansible-playbook test.yml
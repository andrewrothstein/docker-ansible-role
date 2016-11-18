
FROM andrewrothstein/docker-ansible:fedora_24
MAINTAINER "Andrew Rothstein" andrew.rothstein@gmail.com

RUN mkdir -p /role-to-test
ONBUILD ADD . /role-to-test
ONBUILD WORKDIR /role-to-test
ONBUILD RUN ansible-galaxy install -r requirements.yml
ONBUILD RUN ansible-playbook test.yml
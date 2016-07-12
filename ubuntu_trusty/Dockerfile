
FROM andrewrothstein/docker-ansible:ubuntu_trusty
MAINTAINER "Andrew Rothstein" andrew.rothstein@gmail.com

RUN mkdir -p /role-to-test
ONBUILD ADD . /role-to-test
ONBUILD WORKDIR /role-to-test
ONBUILD RUN if [ -f requirements.yml ]; then ansible-galaxy install -r requirements.yml; fi
ONBUILD RUN ansible-playbook test.yml
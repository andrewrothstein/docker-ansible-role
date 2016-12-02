
FROM andrewrothstein/docker-ansible:ubuntu_xenial
MAINTAINER "Andrew Rothstein" andrew.rothstein@gmail.com

RUN mkdir -p /freshen
WORKDIR /freshen
COPY requirements.yml requirements.yml
COPY playbook.yml playbook.yml
RUN ansible-galaxy install -r requirements.yml
RUN ansible-playbook playbook.yml

RUN mkdir -p /role-to-test
ONBUILD ADD . /role-to-test
ONBUILD WORKDIR /role-to-test
ONBUILD RUN if [ -f requirements.yml ]; then ansible-galaxy install -r requirements.yml; fi
ONBUILD RUN ansible-playbook test.yml
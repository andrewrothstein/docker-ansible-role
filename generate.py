#!/usr/bin/env python

import argparse
from jinja2 import Environment
from subprocess import call
import os
import shutil
from string import join

Dockerfile = """
FROM andrewrothstein/docker-ansible:{{tag}}
MAINTAINER "Andrew Rothstein" andrew.rothstein@gmail.com

RUN mkdir -p /role-to-test
ONBUILD ADD . /role-to-test
ONBUILD WORKDIR /role-to-test
ONBUILD RUN if [ -f requirements.yml ]; then ansible-galaxy install -r requirements.yml; fi
ONBUILD RUN ansible-playbook test.yml
"""

def copy_file(tag, file) :
  shutil.copyfile(file, '{0}/{1}'.format(tag, file))

def write(params) :
  tag = params["tag"]
  if (not os.path.isdir(tag)) :
    os.mkdir(tag)
  fq_dockerfile = "{0}/Dockerfile".format(tag) 
  print "writing {0}...".format(fq_dockerfile)
  f = open(fq_dockerfile, 'w')
  f.write(Environment().from_string(Dockerfile).render(params))
  f.close()
	
def build(params) :
  tag = params["tag"]
  container_name = 'andrewrothstein/docker-ansible-role'
  print "building the {0}:{1} container...".format(container_name, tag)
  cmd = ['docker', 'build', '-t', '{0}:{1}'.format(container_name, tag), tag]
  os.chdir
  return call(cmd, shell=False)

def push(registry) :
  def pusher(params) :
    tag = params["tag"]
    container_name = 'andrewrothstein/docker-ansible-role'
    url = "{0}/{1}:{2}".format(registry, container_name, tag)
    print "pushing building to {0}...".format(url)
    cmd = ['docker', 'push', url]
    os.chdir
    return call(cmd, shell=False)
  return pusher

def pull(params) :
  baseimg = "andrewrothstein/docker-ansible:{0}".format(params["tag"])
  print "pulling {0}...".format(baseimg)
  cmd = ['docker', 'pull', baseimg]
  return call(cmd, shell=False)

if __name__ == '__main__' :

  parser = argparse.ArgumentParser(
    description='generates a bunch of Docker base containers for use with Ansible'
  )
  parser.add_argument(
    '-w',
    '--write',
    action='store_true',
    help='write the Dockerfiles'
  )
  parser.add_argument(
    '-b',
    '--build',
    action='store_true',
    help='build the Docker containers'
  )
  parser.add_argument(
    '-p',
    '---push',
    help='push to the given docker registry'
  )
  parser.add_argument(
    '-f',
    '--pull',
    action='store_true',
    help='pull base images'
  )
  
  args = parser.parse_args()

  configs = [
    { "tag" : "fedora_23" },
    { "tag" : "fedora_24" },
    { "tag" : "centos_7" },
    { "tag" : "ubuntu_trusty" },
    { "tag" : "ubuntu_xenial" },
    { "tag" : "alpine_edge" },
    { "tag" : "alpine_3.3" },
    { "tag" : "alpine_3.4" }
  ]

  if (args.pull) :
    map(pull, configs)
    
  if (args.write) :
    map(write, configs)

  if (args.build) :
    map(build, configs)

  if (args.push) :
    map(push(args.push), configs)


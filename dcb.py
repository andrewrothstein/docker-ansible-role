#!/usr/bin/env python

import argparse
import logging
import os
import shutil
from jinja2 import Environment, FileSystemLoader
from string import join
from subprocess import check_call

def copy_file(tag, file) :
  shutil.copyfile(file, '{0}/{1}'.format(tag, file))

class Image:
  def __init__(self, group, app, registry=None, tag=None):
    self.registry=registry
    self.group=group
    self.app=app
    self.tag = "latest" if tag is None else tag

  def name(self):
    return "{0}/{1}:{2}".format(self.group, self.app, self.tag)

  def fq_name(self):
    if self.registry is None:
      return self.container()
    else:
      return "{0}/{1}".format(self.registry, self.name())

def login(registry, user, pwd, email):
  log = logging.getLogger("dcb.login")
  if pwd is not None:
    log.info("logging {0} into {1}...".format(user, registry))
    check_call(['docker',
                'login',
                '-u', user,
                '-p', pwd,
                '-e', email,
                registry])
  else:
    log.info("no password specified for {0}. not logging in.".format(user))
    
def dockerbuilddir(tag, writesubdirs):
  return tag if writesubdirs else '.'

def dockerfile(tag, writesubdirs):
  if writesubdirs:
    return "{0}/Dockerfile".format(dockerbuilddir(tag, writesubdirs))
  else:
    return "Dockerfile.{0}".format(tag)

def fmt_build_args(buildenv):
  log = logging.getLogger("dcb.fmt_build_args")
  setvars = filter(lambda e: e in os.environ, buildenv)
  r = reduce(list.__add__, map(lambda e: ["--build-arg", e], setvars))
  log.info("build args:{0}".format(r))
  return r
      
def describe(image):
  log = logging.getLogger("dcb.info")
  check_call(['docker', 'image', image.name()])

# writes ${OS}/Dockerfile and copies some stuff down...
def write(upstream_image, writesubdirs):
  log = logging.getLogger("dcb.write")
  dbd = dockerbuilddir(upstream_image.tag, writesubdirs)
  df = dockerfile(upstream_image.tag, writesubdirs)

  if (writesubdirs):
    if (not os.path.isdir(dbd)) :
      os.mkdir(dbd)
    copy_file(dbd, "requirements.yml")
    copy_file(dbd, "playbook.yml")
    
  template = Environment(
    loader=FileSystemLoader("snippets")
  ).get_template("Dockerfile")
  log.info("writing Dockerfile to {0}...".format(df))
  with open(df, 'w') as f:
    f.write(template.render({ "fq_upstream_image" : upstream_image.fq_name()}))

def build(target_image, buildenvs, writesubdirs):
  log = logging.getLogger("dcb.build")
  log.info("building the {0} container...".format(target_image.name()))
  cmd = ['docker', 'build', '--rm=false'] + fmt_build_args(buildenvs) + ['-t', target_image.name(),
                                                           dockerbuilddir(target_image.tag, writesubdirs)]
  r = check_call(cmd, shell=False)
  describe(target_image)
  return r

def push(target_image):
  log = logging.getLogger("dcb.push")
  log.info("tagging {0} as {1}...".format(target_image.name(), target_image.fq_name()))
  check_call(['docker', 'tag', target_image.name(), target_image.fq_name()])
  log.info("pushing {0}...".format(target_image.fq_name()))
  r = check_call(['docker',
                  'push',
                  target_image.fq_name()],
                 shell=False)
  describe(target_image)
  return r

def pull(upstream_image) :
  log = logging.getLogger("dcb.pull")
  log.info("pulling {0}...".format(upstream_image.fq_name()))
  r = check_call(['docker',
                  'pull',
                  upstream_image.fq_name()],
                 shell=False)
  describe(upstream_image)
  return r

def main() :

  parser = argparse.ArgumentParser(
    description='generates a bunch of Docker base containers for use testing Ansible roles'
  )

  parser.add_argument(
    '--upstreamregistry',
    default='quay.io',
    help='upstream registry for all pull operations'
  )
  
  parser.add_argument(
    '--upstreamgroup',
    default='andrewrothstein'
  )

  parser.add_argument(
    '--upstreamuser',
    default='andrewrothstein'
  )

  parser.add_argument(
    '--upstreampwd',
    help='password to login the upstream user'
  )

  parser.add_argument(
    '--upstreamemail',
    default='andrew.rothstein@gmail.com'
  )

  parser.add_argument(
    '--upstreamapp',
    default='docker-ansible'
  )

  parser.add_argument(
    '--targetregistry',
    default='quay.io',
    help='target registry for all push operations'
  )
  
  parser.add_argument(
    '--targetgroup',
    default='andrewrothstein'
  )

  parser.add_argument(
    '--targetuser',
    default='andrewrothstein'
  )
  
  parser.add_argument(
    '--targetpwd',
    help='password to login the target user'
  )

  parser.add_argument(
    '--targetemail',
    default='andrew.rothstein@gmail.com'
  )

  parser.add_argument(
    '--targetapp',
    default='docker-ansible-role'
  )

  parser.add_argument(
    '--write',
    help='write the subdirs for the specified tag'
  )

  parser.add_argument(
    '--pull',
    help='pull upstream image for specified tags'
  )
  
  parser.add_argument(
    '--build',
    help='build the Docker container for the specified tag'
  )
  
  parser.add_argument(
    '--push',
    help='push built Docker container to the target registry for specified tag'
  )

  parser.add_argument(
    '--writeall',
    action='store_true',
    help='write the subdirs for all tags'
  )

  parser.add_argument(
    '--writesubdirs',
    action='store_true'
  )
  
  parser.add_argument(
    '--pullall',
    action='store_true',
    help='pull upstream images for all tags'
  )
  
  parser.add_argument(
    '--buildall',
    action='store_true',
    help='build Docker containers for all tags'
  )

  parser.add_argument(
    '--pushall',
    action='store_true',
    help='push built Docker containers to the specified target registry for all tags'
  )

  parser.add_argument(
    '--buildenv',
    nargs='*',
    default=['HTTP_PROXY', 'HTTPS_PROXY', 'FTP_PROXY', 'NO_PROXY',
             'http_proxy', 'https_proxy', 'ftp_proxy', 'no_proxy'],
    help='list of environment variables to pass through as build args'
  )
  
  args = parser.parse_args()

  login(
    args.upstreamregistry,
    args.upstreamuser,
    args.upstreampwd,
    args.upstreamemail
  )

  login(
    args.targetregistry,
    args.targetuser,
    args.targetpwd,
    args.targetemail
  )
  
  def upstream_image(tag):
    return Image(
      group=args.upstreamgroup,
      app=args.upstreamapp,
      registry=args.upstreamregistry,
      tag=tag
      )

  def target_image(tag):
    return Image(
      group=args.targetgroup,
      app=args.targetapp,
      registry=args.targetregistry,
      tag=tag
      )
  
  all_tags = [
    "ubuntu_trusty",
    "ubuntu_xenial",
    "fedora_23",
    "fedora_24",
    "fedora_25",
    "centos_7",
    "alpine_3.3",
    "alpine_3.4",
    "alpine_3.5",
    "alpine_edge",
    "debian_jessie",
  ]

  if (args.pullall) :
    map(lambda tag : pull(upstream_image(tag)), all_tags)

  if (args.pull):
    pull(upstream_image(args.pull))
    
  if (args.writeall) :
    map(lambda tag : write(upstream_image(tag), args.writesubdirs), all_tags)

  if (args.write):
    write(upstream_image(args.write), args.writesubdirs)

  if (args.buildall) :
    map(lambda tag: build(target_image(tag), args.buildenv, args.writesubdirs), all_tags)

  if (args.build):
    build(target_image(args.build), args.buildenv, args.writesubdirs)
    
  if (args.pushall) :
    map(lambda tag: push(target_image(tag)), all_tags)

  if (args.push) :
    push(target_image(args.push))

if __name__ == '__main__' :
    logging.basicConfig(
      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
      level=logging.INFO
    )

    log = logging.getLogger("dcb.__main__")
    log.info("welcome to the dcb...")
    main()
    log.info("exiting the dcb!")


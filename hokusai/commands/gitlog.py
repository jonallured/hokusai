from hokusai.lib.command import command
from hokusai.lib.common import print_red, print_green, shout
from hokusai.services.deployment import Deployment
from hokusai.services.ecr import ECR

@command()
def gitlog():
  ecr = ECR()

  staging_tag = ecr.find_git_sha1_image_tag('staging')
  if staging_tag is None:
    raise HokusaiError("Could not find a tag for staging.  Aborting.")

  production_tag = ecr.find_git_sha1_image_tag('production')
  if production_tag is None:
    raise HokusaiError("Could not find a git SHA1 tag for production.  Aborting.")

  print_green("Comparing %s to %s" % (production_tag, staging_tag))
  for remote in shout('git remote').splitlines():
    shout("git fetch %s" % remote)
  shout("git log --right-only %s..%s" % (production_tag, staging_tag), print_output=True)

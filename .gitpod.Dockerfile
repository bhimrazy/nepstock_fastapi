FROM gitpod/workspace-full

RUN sudo apt-get update  && sudo apt-get install -y curl  && curl -fsSL https://get.deta.dev/cli.sh | sh   
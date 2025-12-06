FROM jenkins/inbound-agent:jdk21

USER root

RUN apt-get update && apt-get install -y docker.io ca-certificates curl

RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

RUN usermod -aG docker jenkins

USER jenkins

WORKDIR /home/jenkins


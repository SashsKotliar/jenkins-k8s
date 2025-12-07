FROM jenkins/inbound-agent:jdk21

USER root

# Install required packages
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
    && rm kubectl

# Install Kaniko executor
RUN curl -L https://github.com/GoogleContainerTools/kaniko/releases/latest/download/executor \
    -o /kaniko-executor \
    && chmod +x /kaniko-executor

WORKDIR /home/jenkins

USER jenkins

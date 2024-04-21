###
# Registry DNS specific parameters
# This is deprecated and should be done in hadoop-env.sh
###
# For privileged registry DNS, user to run as after dropping privileges
# This will replace the hadoop.id.str Java property in secure mode.
# export YARN_REGISTRYDNS_SECURE_USER=yarn

# Supplemental options for privileged registry DNS
# By default, Hadoop uses jsvc which needs to know to launch a
# server jvm.
# export YARN_REGISTRYDNS_SECURE_EXTRA_OPTS="-jvm server"

###
# YARN Services parameters
###
# Directory containing service examples
# export YARN_SERVICE_EXAMPLES_DIR = $HADOOP_YARN_HOME/share/hadoop/yarn/yarn-service-examples
# export YARN_CONTAINER_RUNTIME_DOCKER_RUN_OVERRIDE_DISABLE=true

export JAVA_HOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64
                                                                                                                                                                                                    200,55        Bot

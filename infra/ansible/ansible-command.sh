#!/bin/bash
export ANSIBLE_HOST_KEY_CHECKING=false

die () {
    echo >&2 "$@"
	  echo -e "\nUsage:"
    echo -e "./ansible-command.sh -g GROUP_NAME [command]\n"
    exit 1
}

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -g|--group)
    GROUP="$2"
    shift # past argument
    shift # past value
    ;;
    *) # command
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

[ ! -z "${GROUP}" ] || GROUP="all"

echo -e "Running command on GROUP=${GROUP}"

cd ../terraform
ansible --vault-id ../ansible/vault-password --inventory-file=$(which terraform-inventory) -u root -f 10 -m raw -a "$(printf '%s ' "${POSITIONAL[@]}")" $GROUP

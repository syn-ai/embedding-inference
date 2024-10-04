#!/bin/bash

# Check if the dot_env_dir is provided as an argument, if not, use the current directory
dot_env_dir=$1

if [ -d "$dot_env_dir" ]; then
    source $dot_env_dir/bin/activate
else
    if [ -d ".embedding" ]; then
            source .embedding/bin/activate
    else
        python -m venv .embedding
        source .embedding/bin/activate
    fi
fi

echo "$(cat modules/embedding/.env.example)" >> .env

pip install -e modules/embedding
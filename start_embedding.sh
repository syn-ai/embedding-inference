if [ ! command -v pm2 &> /dev/null ]; then
    echo "pm2 not found, installing pm2"
    if [ ! command -v npm &> /dev/null ]; then
        echo "npm not found, installing npm"
        if [ ! command -v nvm &> /dev/null ]; then
            echo 'nvm not found, installing nvm'
            curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
            [ -s "$HOME/.nvm/nvm.sh" ] && . "$HOME/.nvm/nvm.sh" # This loads nvm
        fi
        nvm install 20
        nvm use 20
        npm install -g npm@latest
    fi
    npm install -g pm2
fi

pm2 start 'python modules/embedding/api.py' --name "embedding"
# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
    # The most common configuration options are documented and commented below.
    # For a complete reference, please see the online documentation at
    # https://docs.vagrantup.com.

    # Every Vagrant development environment requires a box. You can search for
    # boxes at https://vagrantcloud.com/search.
    config.vm.box = "ubuntu/xenial64"

    # Disable automatic box update checking. If you disable this, then
    # boxes will only be checked for updates when the user runs
    # `vagrant box outdated`. This is not recommended.
    # config.vm.box_check_update = false

    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine. In the example below,
    # accessing "localhost:8080" will access port 80 on the guest machine.
    # NOTE: This will enable public access to the opened port
    # config.vm.network "forwarded_port", guest: 80, host: 8080

    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine and only allow access
    # via 127.0.0.1 to disable public access
    config.vm.network "forwarded_port", guest: 5000, host: 5000
    config.vm.network "forwarded_port", guest: 8080, host: 8080

    # Create a private network, which allows host-only access to the machine
    # using a specific IP.
    # config.vm.network "private_network", ip: "192.168.33.10"

    # Create a public network, which generally matched to bridged network.
    # Bridged networks make the machine appear as another physical device on
    # your network.
    # config.vm.network "public_network"

    # Share an additional folder to the guest VM. The first argument is
    # the path on the host to the actual folder. The second argument is
    # the path on the guest to mount the folder. And the optional third
    # argument is a set of non-required options.
    # config.vm.synced_folder "../data", "/vagrant_data"

    # Provider-specific configuration so you can fine-tune various
    # backing providers for Vagrant. These expose provider-specific options.
    # Example for VirtualBox:
    #
    # config.vm.provider "virtualbox" do |vb|
    #   # Display the VirtualBox GUI when booting the machine
    #   vb.gui = true
    #
    #   # Customize the amount of memory on the VM:
    #   vb.memory = "1024"
    # end
    #
    # View the documentation for the provider you are using for more
    # information on available options.
    config.vm.provider "virtualbox"

    # Enable provisioning with a shell script. Additional provisioners such as
    # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
    # documentation for more information about their specific syntax and use.
    # config.vm.provision "shell", inline: <<-SHELL
    #   apt-get update
    #   apt-get install -y apache2
    # SHELL
    config.vm.provision :shell, inline: <<-SHELL
        # Install dependencies
        curl -sL https://deb.nodesource.com/setup_8.x | bash -
        add-apt-repository -y ppa:jonathonf/python-3.6
        apt update
        apt install -y python3.6 python3.6-dev build-essential python3-pip nodejs redis-server postgresql
        pip3 install pipenv

        # Replace credentials
        if [ ! -f /vagrant/.env ]; then
            cd /vagrant
            sed 's/\r$//' .env.example > .env # Change CRLF to LF and copy file
            POSTGRES_PASSWORD=$(echo $RANDOM | sha256sum | base64 | head -c 32 ; echo)
            EZ_ROOT_PASSWORD=$(echo $RANDOM | sha256sum | base64 | head -c 32 ; echo)
            sed -i "s/POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=${POSTGRES_PASSWORD}/" .env
            sed -i "s/EZ_ROOT_PASSWORD=.*/EZ_ROOT_PASSWORD=${EZ_ROOT_PASSWORD}/" .env
            sed -i "s/SENTRY_DSN=.*/SENTRY_DSN=/" .env
        fi

        source /vagrant/.env

        # set up database
        su postgres << EOT
            psql -c "CREATE ROLE ${POSTGRES_USER} WITH SUPERUSER CREATEDB CREATEROLE LOGIN ENCRYPTED PASSWORD '${POSTGRES_PASSWORD}';"
            createdb $POSTGRES_USER
            psql -d $POSTGRES_USER -f /vagrant/api/init.sql
EOT


        # Set up API server and frontend server
        su vagrant << EOT
            cd /vagrant/api
            pipenv --python python3.6
            pipenv install

            # create ezsetup root user
            echo -e "from manage import create_root\\ncreate_root('${EZ_ROOT_EMAIL}', '${EZ_ROOT_PASSWORD}', 'Admin')" | pipenv run python

            cd /vagrant/frontend
            npm install
EOT
    SHELL
    config.vm.provision :shell, run: "always", inline: <<-SHELL
        source /vagrant/.env
        su vagrant << EOT
            cd /vagrant/api
            pipenv run python app.py >> /vagrant/api-server.log 2>&1 &
            cd /vagrant/frontend
            npm run dev >> /vagrant/frontend.log 2>&1 &
EOT
        echo "[INFO] ezsetup login email: ${EZ_ROOT_EMAIL}, password: ${EZ_ROOT_PASSWORD}"
        echo "[INFO] postgresql root username: ${POSTGRES_USER}, password: ${POSTGRES_PASSWORD}"
    SHELL
end

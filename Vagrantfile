Vagrant.configure("2") do |config|

  # Devbox Configuration
  config.vm.define "devbox" do |devbox|
    # Basic Configuration
    devbox.vm.box="generic/ubuntu1804"
    devbox.vm.hostname="controller"
    devbox.vm.network :private_network, ip: "192.168.11.100"
    devbox.vm.synced_folder "../discordbot", "/home/vagrant/vagrant", fsnotify: true
    
    # Start provisioning shell
    devbox.vm.provision :shell, path: "scripts/bootstrap.sh"

    # Virtualbox Configuration
    config.vm.provider "virtualbox" do |v|
      v.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
      v.customize [ "setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
    end
  end
  
end

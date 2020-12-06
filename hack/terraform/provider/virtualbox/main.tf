resource "virtualbox_vm" "bastion" {
  count     = var.bastion_count
  name      = format(var.bastion_name + "%02d", count.index + 1)
  image     = var.bastion_image
  cpus      = var.bastion_cpu
  memory    = var.bastion_memory + " mib"
  user_data = file("../../../cloud-init/nocloud-net/user-data_bastion.yaml")

  network_adapter {
    type           = "hostonly"
    host_interface = "vboxnet1"
  }
}

resource "virtualbox_vm" "database" {
  count     = var.databse_count
  name      = format(var.database_name + "%02d", count.index + 1)
  image     = var.database_image
  cpus      = var.database_cpu
  memory    = var.database_memory + " mib"
  user_data = file("../../../cloud-init/nocloud-net/user-data_database.yaml")

  network_adapter {
    type           = "hostonly"
    host_interface = "vboxnet1"
  }
}


module "provider" {
    source = "./provider/virtualbox/"

    bastion_cpu = var.vbox_bastion_cpu
    bastion_memory = var.vox_bastion_memory

    database_cpu = var.vbox_database_cpu
    database_memory = var.vbox_database_memory
}
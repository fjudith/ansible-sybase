variable "vbox_bastion_cpu" {
    type = number
    default = 1
    description = "Amount of CPU for Virtualbox based Bastion"
}

variable "vbox_bastion_memory" {
    type = number
    default = 1024
    description = "Amount of RAM for Virtualbox based Bastion"
}

variable "vbox_database_cpu" {
    type = number
    default = 2
    description = "Amount of CPU for Virtualbox based Sybase database"
}

variable "vbox_database_memory" {
    type = number
    default = 2048
    description = "Amount of RAM for Virtualbox based Sybase database"
}

variable "bation_count" {
    type = number
    default = 1
}

variable "bastion_cpu" {
    type = number
    default = 1
}

variable "bastion_memory" {
    type = number
    default = 1024
}

variable "bastion_name" {
    type = string
    default = "bastion"
}


variable "database_count" {
    default = 1
}

variable "database_cpu" {
    type = number
    default = 2
}

variable "database_memory" {
    type = number
    default = 2048
}

variable "database_name" {
    type = string
    default = "datbase"
}

variable "image" {
    type = string
    default = "http://cloud.centos.org/centos/7/vagrant/x86_64/images/CentOS-7-x86_64-Vagrant-2004_01.VirtualBox.box"
}

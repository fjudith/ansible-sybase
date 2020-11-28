output "bastion_ipv4_0" {
    value = element(virtualbox_vm.bastion.*.network_adapter.0.ipv4_address, 1)
}

output "bastion_ipv4_2" {
    value = element(virtualbox_vm.bastion.*.network_adapter.0.ipv4_address, 2)
}

output "bastion_hosts" {
    value = element(virtualbox_vm.bastion.*.name)
}

output "database_ipv4_0" {
    value = element(virtualbox_vm.database.*.network_adapter.0.ipv4_address, 1)
}

output "database_ipv4_2" {
    value = element(virtualbox_vm.database.*.network_adapter.0.ipv4_address, 2)
}

output "database_hosts" {
    value = element(virtualbox_vm.database.*.name)
}
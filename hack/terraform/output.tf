output "bastion_hosts" {
    value = module.povider.bastion_hosts
}

output "database_hosts" {
    value = module.povider.database_hosts
}

output "bastion_ipv4" {
    value = module.povider.bastion_ipv4_0
}

output "database_ipv4" {
    value = module.povider.database_ipv4_0
}
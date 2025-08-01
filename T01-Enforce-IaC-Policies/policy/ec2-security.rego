package main

deny[msg] {
    resource := input.planned_values.root_module.resources[_]
    resource.type == "aws_security_group"
    ingress := resource.values.ingress[_]
    ingress.from_port == 22
    ingress.cidr_blocks[_] == "0.0.0.0/0"
    msg := sprintf("Security group '%s' allows SSH from anywhere - security violation", [resource.name])
}

deny[msg] {
    resource := input.planned_values.root_module.resources[_]
    resource.type == "aws_instance"
    not resource.values.monitoring
    msg := sprintf("EC2 instance '%s' should have detailed monitoring enabled", [resource.name])
}

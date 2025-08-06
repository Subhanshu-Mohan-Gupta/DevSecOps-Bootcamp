package main

import future.keywords.contains
import future.keywords.if

# EC2: Monitoring enabled
deny contains msg if {
  resource := input.planned_values.root_module.resources[_]
  resource.type == "aws_instance"
  resource.values.monitoring == false
  msg := sprintf("EC2 instance '%s' should have monitoring enabled", [resource.name])
}

# EC2: Allowed instance type (t3.* or t4g.*)
deny contains msg if {
  resource := input.planned_values.root_module.resources[_]
  resource.type == "aws_instance"
  instance_type := resource.values.instance_type
  not startswith(instance_type, "t3.")
  not startswith(instance_type, "t4g.")
  msg := sprintf("EC2 instance '%s' must use only t3.* or t4g.* instance types, got '%s'", [resource.name, instance_type])
}

# EC2: Required tags
required_tags := {"Environment", "Owner", "Project"}

deny contains msg if {
  resource := input.planned_values.root_module.resources[_]
  resource.type == "aws_instance"
  tags := object.get(resource.values, "tags", {})
  missing := [tag | tag := required_tags[_]; not object.get(tags, tag, null)]
  count(missing) > 0
  msg := sprintf("EC2 instance '%s' is missing required tags: %v", [resource.name, missing])
}

# EC2: Root volume encryption
deny contains msg if {
  resource := input.planned_values.root_module.resources[_]
  resource.type == "aws_instance"
  root := resource.values.root_block_device[0]
  root.encrypted == false
  msg := sprintf("EC2 instance '%s' has unencrypted root volume", [resource.name])
}

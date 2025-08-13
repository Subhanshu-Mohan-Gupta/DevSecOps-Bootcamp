package main

deny[msg] {
  resource := input.planned_values.root_module.resources[_]
  resource.type == "azurerm_storage_account"

  # 🚫 Rule 1: HTTPS traffic only must be enabled
  not resource.values.https_traffic_only_enabled
  msg := "Storage account must enforce HTTPS traffic only"
}

deny[msg] {
  resource := input.planned_values.root_module.resources[_]
  resource.type == "azurerm_storage_account"

  # 🚫 Rule 2: Public blob access must be disabled
  resource.values.allow_nested_items_to_be_public == true
  msg := "Storage account must not allow public blob access"
}

**Combined instructions:** The following combines multiple actions. Perform them one after another.

## Scope

**Scope:** Show All (entire story graph)

Please only work on the following scope.

Scope Filter: "Show All (entire story graph)"

Scope:

{
  "path": "C:\\dev\\vouchers\\docs\\story\\story-graph.json",
  "has_epics": true,
  "has_increments": true,
  "has_domain_concepts": true,
  "epic_count": 1,
  "content": {
    "epics": [
      {
        "name": "Manage Campaigns",
        "sub_epics": [
          {
            "name": "Manage Vouchers",
            "sub_epics": [],
            "story_groups": [
              {
                "name": null,
                "stories": [
                  {
                    "name": "Create Vouchers via JSON API",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN client sends POST /campaigns/{id}/vouchers with JSON body containing voucher list (code, redemption_limit, metadata) THEN voucher service creates vouchers AND persists vouchers AND returns created vouchers",
                        "text": "WHEN client sends POST /campaigns/{id}/vouchers with JSON body containing voucher list (code, redemption_limit, metadata) THEN voucher service creates vouchers AND persists vouchers AND returns created vouchers",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN JSON contains vouchers with codes THEN each voucher is created with provided code AND linked to campaign",
                        "text": "WHEN JSON contains vouchers with codes THEN each voucher is created with provided code AND linked to campaign",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN client sends duplicate voucher code THEN API returns validation error for that voucher AND does not create duplicate",
                        "text": "WHEN client sends duplicate voucher code THEN API returns validation error for that voucher AND does not create duplicate",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN client sends invalid campaign reference THEN API returns error AND does not create vouchers",
                        "text": "WHEN client sends invalid campaign reference THEN API returns error AND does not create vouchers",
                        "sequential_order": 4.0
                      },
                      {
                        "name": "WHEN vouchers are created THEN vouchers inherit campaign metadata AND can override at voucher level",
                        "text": "WHEN vouchers are created THEN vouchers inherit campaign metadata AND can override at voucher level",
                        "sequential_order": 5.0
                      }
                    ]
                  },
                  {
                    "name": "View Voucher List",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN administrator opens campaign vouchers THEN admin UI displays voucher list (code, redemptions, status)",
                        "text": "WHEN administrator opens campaign vouchers THEN admin UI displays voucher list (code, redemptions, status)",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN administrator selects vouchers THEN admin UI allows bulk delete",
                        "text": "WHEN administrator selects vouchers THEN admin UI allows bulk delete",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN administrator clicks voucher THEN admin UI navigates to voucher details",
                        "text": "WHEN administrator clicks voucher THEN admin UI navigates to voucher details",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN campaign has no vouchers THEN admin UI shows empty state AND Add Voucher button",
                        "text": "WHEN campaign has no vouchers THEN admin UI shows empty state AND Add Voucher button",
                        "sequential_order": 4.0
                      }
                    ]
                  },
                  {
                    "name": "View Voucher Details",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN administrator views voucher details THEN display shows campaign, discount type, value, redemption limit, metadata",
                        "text": "WHEN administrator views voucher details THEN display shows campaign, discount type, value, redemption limit, metadata",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN voucher has barcode/QR THEN admin UI displays barcode and QR code with toggle",
                        "text": "WHEN voucher has barcode/QR THEN admin UI displays barcode and QR code with toggle",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN administrator views voucher details THEN display shows redemption count",
                        "text": "WHEN administrator views voucher details THEN display shows redemption count",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN voucher is fully redeemed THEN admin UI indicates exhausted status AND validate returns invalid",
                        "text": "WHEN voucher is fully redeemed THEN admin UI indicates exhausted status AND validate returns invalid",
                        "sequential_order": 4.0
                      }
                    ]
                  },
                  {
                    "name": "Edit Voucher Metadata",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN administrator edits voucher metadata THEN form displays key-value pairs (add, delete, override)",
                        "text": "WHEN administrator edits voucher metadata THEN form displays key-value pairs (add, delete, override)",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN administrator adds metadata key-value THEN voucher stores entry",
                        "text": "WHEN administrator adds metadata key-value THEN voucher stores entry",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN metadata key was used in campaign or other vouchers THEN form auto-populates key for selection",
                        "text": "WHEN metadata key was used in campaign or other vouchers THEN form auto-populates key for selection",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN administrator removes or overrides metadata entry THEN voucher updates accordingly",
                        "text": "WHEN administrator removes or overrides metadata entry THEN voucher updates accordingly",
                        "sequential_order": 4.0
                      }
                    ]
                  },
                  {
                    "name": "Edit Voucher Redemption Limit",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN administrator edits voucher redemption limit THEN form displays integer field (per-voucher override of campaign default)",
                        "text": "WHEN administrator edits voucher redemption limit THEN form displays integer field (per-voucher override of campaign default)",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN administrator submits valid positive integer THEN voucher stores redemption limit",
                        "text": "WHEN administrator submits valid positive integer THEN voucher stores redemption limit",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN administrator submits invalid value (e.g. negative) THEN form shows validation error AND does not update voucher",
                        "text": "WHEN administrator submits invalid value (e.g. negative) THEN form shows validation error AND does not update voucher",
                        "sequential_order": 3.0
                      }
                    ]
                  },
                  {
                    "name": "Add Voucher to Campaign",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN administrator clicks Add Voucher in campaign THEN voucher form displays AND administrator enters code and redemption limit",
                        "text": "WHEN administrator clicks Add Voucher in campaign THEN voucher form displays AND administrator enters code and redemption limit",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN administrator submits voucher form with valid data THEN voucher service creates voucher AND persists AND shows success",
                        "text": "WHEN administrator submits voucher form with valid data THEN voucher service creates voucher AND persists AND shows success",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN administrator submits with duplicate code THEN voucher form shows validation error BUT does not create voucher",
                        "text": "WHEN administrator submits with duplicate code THEN voucher form shows validation error BUT does not create voucher",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN administrator cancels add THEN voucher form closes AND no voucher is created",
                        "text": "WHEN administrator cancels add THEN voucher form closes AND no voucher is created",
                        "sequential_order": 4.0
                      }
                    ]
                  },
                  {
                    "name": "Delete Voucher",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN administrator selects voucher and clicks Delete THEN voucher service removes voucher AND shows confirmation",
                        "text": "WHEN administrator selects voucher and clicks Delete THEN voucher service removes voucher AND shows confirmation",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN administrator selects multiple vouchers and clicks Delete THEN voucher service removes selected vouchers",
                        "text": "WHEN administrator selects multiple vouchers and clicks Delete THEN voucher service removes selected vouchers",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN voucher is deleted THEN voucher no longer appears in list AND validate returns invalid for that code",
                        "text": "WHEN voucher is deleted THEN voucher no longer appears in list AND validate returns invalid for that code",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN administrator cancels delete THEN no vouchers are removed AND list remains unchanged",
                        "text": "WHEN administrator cancels delete THEN no vouchers are removed AND list remains unchanged",
                        "sequential_order": 4.0
                      }
                    ]
                  },
                  {
                    "name": "Generate Vouchers",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN administrator requests bulk voucher generation THEN form displays quantity and uses campaign code generation settings",
                        "text": "WHEN administrator requests bulk voucher generation THEN form displays quantity and uses campaign code generation settings",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN administrator submits valid quantity THEN voucher service generates vouchers with unique codes AND persists AND shows success",
                        "text": "WHEN administrator submits valid quantity THEN voucher service generates vouchers with unique codes AND persists AND shows success",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN campaign has auto-increase off and size exceeded THEN generation returns error",
                        "text": "WHEN campaign has auto-increase off and size exceeded THEN generation returns error",
                        "sequential_order": 3.0
                      }
                    ]
                  },
                  {
                    "name": "Request Voucher from Campaign",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN campaign has auto-increase on AND administrator requests one voucher THEN system generates voucher using code generation settings AND campaign size increases",
                        "text": "WHEN campaign has auto-increase on AND administrator requests one voucher THEN system generates voucher using code generation settings AND campaign size increases",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN campaign has auto-increase off AND no vouchers available THEN request returns error",
                        "text": "WHEN campaign has auto-increase off AND no vouchers available THEN request returns error",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN administrator requests voucher THEN admin UI shows generated code AND voucher appears in list",
                        "text": "WHEN administrator requests voucher THEN admin UI shows generated code AND voucher appears in list",
                        "sequential_order": 3.0
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "name": "Manage Campaigns",
            "sub_epics": [],
            "story_groups": [
              {
                "name": null,
                "stories": [
                  {
                    "name": "Create Campaign via JSON API",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN client sends POST /campaigns with JSON body (name, size, auto_increase, time_frame, discount_type, discount_value, metadata) THEN campaign service creates campaign AND persists campaign AND returns created campaign",
                        "text": "WHEN client sends POST /campaigns with JSON body (name, size, auto_increase, time_frame, discount_type, discount_value, metadata) THEN campaign service creates campaign AND persists campaign AND returns created campaign",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN client sends valid JSON with amount discount THEN campaign stores discount type amount AND discount value",
                        "text": "WHEN client sends valid JSON with amount discount THEN campaign stores discount type amount AND discount value",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN client sends valid JSON with percent discount THEN campaign stores discount type percent AND discount value",
                        "text": "WHEN client sends valid JSON with percent discount THEN campaign stores discount type percent AND discount value",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN client sends invalid JSON (missing name or discount) THEN API returns validation error AND does not create campaign",
                        "text": "WHEN client sends invalid JSON (missing name or discount) THEN API returns validation error AND does not create campaign",
                        "sequential_order": 4.0
                      },
                      {
                        "name": "WHEN campaign is created THEN campaign is available for voucher creation via API",
                        "text": "WHEN campaign is created THEN campaign is available for voucher creation via API",
                        "sequential_order": 5.0
                      }
                    ]
                  },
                  {
                    "name": "View Campaign Summary",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN administrator opens campaign list THEN admin UI displays campaigns with search and filters",
                        "text": "WHEN administrator opens campaign list THEN admin UI displays campaigns with search and filters",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN administrator views campaign summary THEN display shows discount type, amount, time frame, vouchers left, published, redeemed, active status",
                        "text": "WHEN administrator views campaign summary THEN display shows discount type, amount, time frame, vouchers left, published, redeemed, active status",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN administrator selects campaign THEN admin UI navigates to campaign details",
                        "text": "WHEN administrator selects campaign THEN admin UI navigates to campaign details",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN no campaigns match search or filter THEN admin UI shows empty state AND clear filter option",
                        "text": "WHEN no campaigns match search or filter THEN admin UI shows empty state AND clear filter option",
                        "sequential_order": 4.0
                      }
                    ]
                  },
                  {
                    "name": "View Campaign Details",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN administrator selects campaign THEN campaign details display (discount type, value, time frame, metadata)",
                        "text": "WHEN administrator selects campaign THEN campaign details display (discount type, value, time frame, metadata)",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN administrator views campaign details THEN admin UI shows Add Voucher button AND Edit button",
                        "text": "WHEN administrator views campaign details THEN admin UI shows Add Voucher button AND Edit button",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN administrator views campaign details THEN admin UI shows Enable/Disable toggle for campaign",
                        "text": "WHEN administrator views campaign details THEN admin UI shows Enable/Disable toggle for campaign",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN campaign has no vouchers THEN admin UI shows empty voucher list AND Add Voucher is primary action",
                        "text": "WHEN campaign has no vouchers THEN admin UI shows empty voucher list AND Add Voucher is primary action",
                        "sequential_order": 4.0
                      }
                    ]
                  },
                  {
                    "name": "Edit Campaign Details",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN administrator edits campaign details THEN form displays size, auto-increase, redemption limit",
                        "text": "WHEN administrator edits campaign details THEN form displays size, auto-increase, redemption limit",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN administrator submits valid size (fixed amount) THEN campaign stores size",
                        "text": "WHEN administrator submits valid size (fixed amount) THEN campaign stores size",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN administrator toggles auto-increase THEN campaign stores on/off AND when off voucher requests beyond size return invalid",
                        "text": "WHEN administrator toggles auto-increase THEN campaign stores on/off AND when off voucher requests beyond size return invalid",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN administrator sets redemption limit (integer per voucher) THEN campaign stores limit",
                        "text": "WHEN administrator sets redemption limit (integer per voucher) THEN campaign stores limit",
                        "sequential_order": 4.0
                      }
                    ]
                  },
                  {
                    "name": "Edit Campaign Time Frame",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN administrator edits campaign time frame THEN form displays valid-from (creation date or specific date) and expires (never or specific date)",
                        "text": "WHEN administrator edits campaign time frame THEN form displays valid-from (creation date or specific date) and expires (never or specific date)",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN administrator sets valid from creation date THEN campaign valid from creation",
                        "text": "WHEN administrator sets valid from creation date THEN campaign valid from creation",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN administrator sets valid from specific date THEN campaign valid from that date",
                        "text": "WHEN administrator sets valid from specific date THEN campaign valid from that date",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN administrator sets expires never THEN campaign has no expiration",
                        "text": "WHEN administrator sets expires never THEN campaign has no expiration",
                        "sequential_order": 4.0
                      },
                      {
                        "name": "WHEN administrator sets expires on specific date THEN campaign expires on that date",
                        "text": "WHEN administrator sets expires on specific date THEN campaign expires on that date",
                        "sequential_order": 5.0
                      }
                    ]
                  },
                  {
                    "name": "Edit Campaign Discount",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN administrator edits campaign discount THEN form displays discount type (amount or percent) and value",
                        "text": "WHEN administrator edits campaign discount THEN form displays discount type (amount or percent) and value",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN administrator selects amount discount and value THEN campaign stores discount_type amount AND discount_value",
                        "text": "WHEN administrator selects amount discount and value THEN campaign stores discount_type amount AND discount_value",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN administrator selects percent discount and value THEN campaign stores discount_type percent AND discount_value",
                        "text": "WHEN administrator selects percent discount and value THEN campaign stores discount_type percent AND discount_value",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN administrator submits invalid discount (e.g. negative value) THEN form shows validation error AND does not update",
                        "text": "WHEN administrator submits invalid discount (e.g. negative value) THEN form shows validation error AND does not update",
                        "sequential_order": 4.0
                      }
                    ]
                  },
                  {
                    "name": "Edit Campaign Metadata",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN administrator edits campaign metadata THEN form displays key-value pairs (optional)",
                        "text": "WHEN administrator edits campaign metadata THEN form displays key-value pairs (optional)",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN administrator adds metadata key-value THEN campaign stores entry",
                        "text": "WHEN administrator adds metadata key-value THEN campaign stores entry",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN metadata key was used in previous campaign THEN form auto-populates key for selection",
                        "text": "WHEN metadata key was used in previous campaign THEN form auto-populates key for selection",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN administrator removes metadata entry THEN campaign no longer stores that key",
                        "text": "WHEN administrator removes metadata entry THEN campaign no longer stores that key",
                        "sequential_order": 4.0
                      }
                    ]
                  },
                  {
                    "name": "Activate Campaign",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN administrator enables campaign THEN campaign becomes active AND vouchers available for validation and redemption",
                        "text": "WHEN administrator enables campaign THEN campaign becomes active AND vouchers available for validation and redemption",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN administrator disables campaign THEN campaign becomes inactive AND vouchers return invalid on validate",
                        "text": "WHEN administrator disables campaign THEN campaign becomes inactive AND vouchers return invalid on validate",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN administrator toggles enable/disable THEN campaign state persists AND admin UI reflects status",
                        "text": "WHEN administrator toggles enable/disable THEN campaign state persists AND admin UI reflects status",
                        "sequential_order": 3.0
                      }
                    ]
                  },
                  {
                    "name": "Edit Campaign Code Generation",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN administrator edits campaign code generation THEN form displays character set, code length, prefix, suffix",
                        "text": "WHEN administrator edits campaign code generation THEN form displays character set, code length, prefix, suffix",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN administrator sets code length (integer) THEN campaign stores value for voucher generation",
                        "text": "WHEN administrator sets code length (integer) THEN campaign stores value for voucher generation",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN administrator sets optional prefix or suffix THEN campaign stores for voucher generation",
                        "text": "WHEN administrator sets optional prefix or suffix THEN campaign stores for voucher generation",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN vouchers are generated THEN system uses campaign code generation settings",
                        "text": "WHEN vouchers are generated THEN system uses campaign code generation settings",
                        "sequential_order": 4.0
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "name": "Redeem Voucher",
            "sub_epics": [],
            "story_groups": [
              {
                "name": null,
                "stories": [
                  {
                    "name": "Redeem Voucher via API",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN client sends POST /redeem with voucher code, customer name, year, amount THEN redemption service runs validate again AND returns error if invalid BUT does not record redemption",
                        "text": "WHEN client sends POST /redeem with voucher code, customer name, year, amount THEN redemption service runs validate again AND returns error if invalid BUT does not record redemption",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN voucher is locked by another client THEN redemption service returns error AND reason voucher-locked BUT does not record redemption",
                        "text": "WHEN voucher is locked by another client THEN redemption service returns error AND reason voucher-locked BUT does not record redemption",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN validation passes THEN redemption service records redemption AND persists AND returns confirmation",
                        "text": "WHEN validation passes THEN redemption service records redemption AND persists AND returns confirmation",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN validation fails on redeem THEN redemption service returns error AND reason BUT does not record redemption",
                        "text": "WHEN validation fails on redeem THEN redemption service returns error AND reason BUT does not record redemption",
                        "sequential_order": 4.0
                      },
                      {
                        "name": "WHEN redemption is recorded THEN record includes voucher code AND customer identity AND amount AND timestamp",
                        "text": "WHEN redemption is recorded THEN record includes voucher code AND customer identity AND amount AND timestamp",
                        "sequential_order": 5.0
                      }
                    ]
                  },
                  {
                    "name": "Review Suspicious Activity",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN administrator opens Review Suspicious Activity THEN RedemptionAudit displays flagged redemptions AND flag reason",
                        "text": "WHEN administrator opens Review Suspicious Activity THEN RedemptionAudit displays flagged redemptions AND flag reason",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN administrator reviews flagged redemption THEN administrator can view full context AND take action (e.g. disable voucher)",
                        "text": "WHEN administrator reviews flagged redemption THEN administrator can view full context AND take action (e.g. disable voucher)",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN administrator dismisses flag THEN RedemptionAudit updates flag status AND redemption remains in history",
                        "text": "WHEN administrator dismisses flag THEN RedemptionAudit updates flag status AND redemption remains in history",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN no redemptions are flagged THEN admin UI shows empty state AND explains no suspicious activity",
                        "text": "WHEN no redemptions are flagged THEN admin UI shows empty state AND explains no suspicious activity",
                        "sequential_order": 4.0
                      }
                    ]
                  },
                  {
                    "name": "View Redemptions",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN administrator opens Redemptions in admin UI THEN RedemptionAudit displays redemption history (voucher code, customer, amount, timestamp)",
                        "text": "WHEN administrator opens Redemptions in admin UI THEN RedemptionAudit displays redemption history (voucher code, customer, amount, timestamp)",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN administrator filters by voucher or customer THEN list shows matching redemptions",
                        "text": "WHEN administrator filters by voucher or customer THEN list shows matching redemptions",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN administrator selects redemption row THEN detail view shows full redemption record AND associated voucher and campaign info",
                        "text": "WHEN administrator selects redemption row THEN detail view shows full redemption record AND associated voucher and campaign info",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN no redemptions match filter THEN admin UI shows empty state AND clear filter option",
                        "text": "WHEN no redemptions match filter THEN admin UI shows empty state AND clear filter option",
                        "sequential_order": 4.0
                      }
                    ]
                  },
                  {
                    "name": "Lock Voucher Redemption through API",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN client sends POST /lock with voucher code and customer context THEN lock service acquires lock for voucher AND returns lock token AND prevents concurrent redemption of same voucher",
                        "text": "WHEN client sends POST /lock with voucher code and customer context THEN lock service acquires lock for voucher AND returns lock token AND prevents concurrent redemption of same voucher",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN voucher code is invalid or missing THEN lock service returns error AND reason BUT does not acquire lock",
                        "text": "WHEN voucher code is invalid or missing THEN lock service returns error AND reason BUT does not acquire lock",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN lock request fails (voucher already locked) THEN lock service returns lock-failed AND reason BUT does not allow redemption to proceed",
                        "text": "WHEN lock request fails (voucher already locked) THEN lock service returns lock-failed AND reason BUT does not allow redemption to proceed",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN voucher is locked by another client THEN validate returns invalid for that voucher AND redeem returns error AND does not record redemption",
                        "text": "WHEN voucher is locked by another client THEN validate returns invalid for that voucher AND redeem returns error AND does not record redemption",
                        "sequential_order": 4.0
                      },
                      {
                        "name": "WHEN lock is acquired THEN lock service holds lock until redemption completes or timeout AND second concurrent request receives lock-failed or must wait",
                        "text": "WHEN lock is acquired THEN lock service holds lock until redemption completes or timeout AND second concurrent request receives lock-failed or must wait",
                        "sequential_order": 5.0
                      },
                      {
                        "name": "WHEN client sends POST /unlock with lock token OR redemption completes OR timeout expires THEN lock service releases lock AND allows subsequent lock requests",
                        "text": "WHEN client sends POST /unlock with lock token OR redemption completes OR timeout expires THEN lock service releases lock AND allows subsequent lock requests",
                        "sequential_order": 6.0
                      }
                    ]
                  },
                  {
                    "name": "Validate Voucher via API",
                    "acceptance_criteria": [
                      {
                        "name": "WHEN client sends POST /validate with voucher code and customer context THEN validation service returns valid yes/no AND reason AND discount amount",
                        "text": "WHEN client sends POST /validate with voucher code and customer context THEN validation service returns valid yes/no AND reason AND discount amount",
                        "sequential_order": 1.0
                      },
                      {
                        "name": "WHEN voucher code is invalid or missing THEN validation service returns invalid AND reason BUT does not return discount amount",
                        "text": "WHEN voucher code is invalid or missing THEN validation service returns invalid AND reason BUT does not return discount amount",
                        "sequential_order": 2.0
                      },
                      {
                        "name": "WHEN campaign is disabled THEN validation service returns invalid for campaign vouchers",
                        "text": "WHEN campaign is disabled THEN validation service returns invalid for campaign vouchers",
                        "sequential_order": 3.0
                      },
                      {
                        "name": "WHEN voucher is locked by another client THEN validation service returns invalid AND reason voucher-locked BUT does not return discount amount",
                        "text": "WHEN voucher is locked by another client THEN validation service returns invalid AND reason voucher-locked BUT does not return discount amount",
                        "sequential_order": 4.0
                      },
                      {
                        "name": "WHEN redemption limit exceeded THEN validation service returns invalid AND reason",
                        "text": "WHEN redemption limit exceeded THEN validation service returns invalid AND reason",
                        "sequential_order": 5.0
                      },
                      {
                        "name": "WHEN all checks pass THEN validation service returns valid AND discount amount AND metadata for client to validate",
                        "text": "WHEN all checks pass THEN validation service returns valid AND discount amount AND metadata for client to validate",
                        "sequential_order": 6.0
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ],
        "domain_concepts": [
          {
            "name": "Campaign",
            "responsibilities": [
              {
                "name": "Hold campaign definition",
                "collaborators": []
              },
              {
                "name": "Hold size and auto-increase",
                "collaborators": []
              },
              {
                "name": "Hold time frame and validity",
                "collaborators": []
              },
              {
                "name": "Hold discount (amount or percent)",
                "collaborators": []
              },
              {
                "name": "Hold metadata (key-value)",
                "collaborators": []
              }
            ],
            "module": "Manage Campaigns"
          }
        ]
      }
    ],
    "increments": [
      {
        "name": "API-Only Foundation",
        "priority": 0,
        "stories": [
          "Create Campaign via JSON API",
          "Create Vouchers via JSON API",
          "Validate Voucher via API",
          "Lock Voucher Redemption through API",
          "Redeem Voucher via API"
        ],
        "description": "JSON API for campaigns, vouchers, validate, redeem. No auto-generation; vouchers provided in request.",
        "behavior_needed": "shape"
      },
      {
        "name": "Voucher Generation and Admin UI",
        "priority": 0,
        "stories": [
          "Request Voucher from Campaign",
          "View Campaign Summary",
          "View Campaign Details",
          "Edit Campaign Details",
          "Edit Campaign Time Frame",
          "Edit Campaign Discount",
          "Edit Campaign Metadata",
          "Activate Campaign",
          "Edit Campaign Code Generation",
          "View Voucher List",
          "View Voucher Details",
          "Edit Voucher Metadata",
          "Edit Voucher Redemption Limit",
          "Add Voucher to Campaign",
          "Delete Voucher",
          "Generate Vouchers",
          "Request Voucher from Campaign",
          "View Redemptions",
          "Review Suspicious Activity"
        ],
        "description": "Automatic voucher generation when requested (if auto-increase on). Admin UI for view/edit campaigns, vouchers, redemptions.",
        "behavior_needed": "shape"
      }
    ]
  }
}

---

# Behavior: domain

## Behavior Instructions - domain

The purpose of this behavior is to model the business domain by extracting and refining crc concepts from stories in the story-graph. organize concepts into modules matching source code folder structure.

Synthesize context into CRC cards and build a CRC model that connects business and solution language

## Action Instructions - build

The purpose of this action is to build story graph from content area and render using story graph renderer

Extract context from story-graph.json
Refine CRC card definitions, responsibilities, and collaborators
Assign each domain concept to a module matching its source code folder structure (use dot notation for nesting)
Apply CRC rules when defining responsibilities and collaborators
Use CRC rules to guide the creation of the CRC model
Update story-graph.json with the new / updated domain concepts, responsibilities, collaborators, and modules

---

**Look for context in the following locations:**
- in this message and chat history
- `C:/dev/vouchers/docs/story/story-graph.json` - the story graph and related  knowledge built so far
- `C:/dev/vouchers/docs/story/strategy.json` - strategy decisions made
- `C:/dev/vouchers/docs/story/clarification.json` - clarification answers
- `C:/dev/vouchers/test/` and `C:/dev/vouchers/src/` - existing code and tests
- any folder named `context/` anywhere in `C:/dev/vouchers/` - additional context files

IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

@build-instructions.txt

**BUILD PROCESS:**

**1. Load Context**
Load clarification.json, planning.json, and source material from context sources (listed above).

**2. Load Build Configs**
From `c:\dev\agile_bots\bots\crc_bot/behaviors/domain/content/`, each folder contains:
- `build_*.json` - Config (name, path, template, output)
- `instructions.json` - Build instructions
- `template-file.json` - Output schema/structure

**3. Execute Build**
1. Load config, instructions, and template (injected as 'story_graph_template')
2. Check if output file exists - read it FIRST
3. Follow instructions.json - match template structure exactly (check '_explanation' section)
4. Apply context from Step 1
5. If file exists: ADD/EXTEND only, never overwrite/delete
6. Validate against template schema
7. Write to `C:\dev\vouchers/{config.path}/{config.output}`
- Read existing files before changes - preserve all content
- Match template structure exactly - don't invent schemas
- Trace all knowledge to clarification/planning data
- Process builds sequentially - validate each

**4. SOURCE TRACEABILITY**
Knowledge artifacts should include source references when available:
- `context_source` field on epics, sub_epics, story_groups, stories, and domain concepts
- Format: `{"file": "filename.pdf", "page": "12", "section": "3.2.1 Payment Flow"}`
- For multiple sources: use array of source objects
- If source is chat/conversation: `{"type": "chat", "description": "User clarification on approval workflow"}`
- If source is code: `{"file": "path/to/file.py", "lines": "45-67", "function": "process_payment"}`
- Prefer tracing knowledge to a source when possible
- When source is unclear, mark as `{"type": "inferred", "basis": "description of inference basis"}`
Extract context from story-graph.json
Refine CRC card definitions, responsibilities, and collaborators
Assign each domain concept to a module matching its source code folder structure (use dot notation for nesting)
Apply CRC rules when defining responsibilities and collaborators
Use CRC rules to guide the creation of the CRC model
Update story-graph.json with the new / updated domain concepts, responsibilities, collaborators, and modules

When building or adding to the story graph follow these rules,
Rules to follow:

- **integrate_and_organize_concepts**: Integrate related capabilities under parent concepts and organize by business domain. Avoid noun redundancy by nesting related capabilities together, group by business capabilities not technical layers.
  DO: Integrate related capabilities under parent concepts, organize by business domain
  DON'T: Don't create redundant/fragmented concepts or group by technical layers

- **use_module_for_folder_structure**: Use module field to map domain concepts to source code folder structure. Module names MUST exactly match folder paths where they exist using dot notation for nesting.
  DO: Module names follow same conventions as classes and match actual folder structure
  DON'T: Don't use generic module names, don't omit module field, don't use slash notation

- **use_domain_language**: Use domain-specific language rooted in core business concepts. Avoid generic terms, technical patterns (Manager, Service, Handler, Factory), and capability verbs (Exposes, Provides, Contains). Name concepts and responsibilities using the ubiquitous language of the business domain.
  DO: Use concrete domain language with specific behaviors and actions
  DON'T: Don't use generic terms, technical patterns, or capability verbs

- **favor_code_representation**: Keep domain model tightly aligned to code it represents, use actual class names and method signatures, not prose descriptions. Show collaborators as types, not descriptions. Avoid over conceptualization.
  DO: Keep code and domain model tightly aligned
  DON'T: Don't use prose descriptions or vague terms

- **scope_concepts_correctly**: Scope domain concepts correctly - place at the most specific level where relevant and ensure they represent complete functional capabilities. Use 'local' scope for single sub-epic concepts, 'global' for shared concepts. Concepts should be complete functional units, not fragments.
  DO: Place concepts at correct scope level and ensure functional completeness
  DON'T: Don't place concepts at wrong scope level or create incomplete fragments

- **use_natural_english**: Use natural English for responsibility names. Responsibilities should read like natural language method calls, using proper grammar and clear intent.
  DO: Write responsibilities in natural English that clearly express intent
  DON'T: Don't use awkward phrasing or overly technical grammar

- **use_resource_oriented_design**: Use resource-oriented design where concepts represent resources with properties and behaviors. Focus on what the resource IS and HAS, not implementation operations.
  DO: Model concepts as resources with properties and contained resources
  DON'T: Don't violate encapsulation - objects should own their data, hide implementation details, and handle their own responsibilities

- **shape_relationships_from_story_map**: Shape domain concept relationships from the story map. Collaborators should come from stories showing how concepts work together to accomplish user goals.
  DO: Derive collaborators from story interactions
  DON'T: Don't invent collaborators not present in stories

### Key Questions

- **Who are the distinct types of users (e.g., operational users, power users, compliance consumers, content creators, producers)?**: (1) Campaign/voucher creators — use native UI to create campaigns and vouchers; (2) Mid-tier (API consumer) — sends redemption requests to the API; (3) Administrators — review redemptions, manage vouchers (enable/disable), review suspicious activity via native UI. End customers redeem via mid-tier, not directly in this system.
- **What are the key goals, behaviors, or decisions each group is trying to accomplish using this capability?**: Creators: Create campaigns and vouchers via native UI. Mid-tier: Validate and redeem vouchers via API, persist results. Administrators: Review redemptions, manage vouchers, spot suspicious activity (manual process).
- **Who are the primary users or stakeholder groups impacted?**: Campaign/voucher creators, administrators (native UI), and mid-tier (API consumer).
- **What is the first thing users will try to do with this new capability or system?**: Create a campaign or voucher via the native UI. Alternatively, mid-tier will send a redemption request via the API.
- **What problems, inefficiencies, or workarounds is this request trying to eliminate?**: [!] NOT ENOUGH INFORMATION - REQUIRES USER INPUT.
- **Where are users currently struggling, getting stuck, or experiencing delays in the process we're aiming to improve?**: [!] NOT ENOUGH INFORMATION - REQUIRES USER INPUT.
- **What are the key drivers for customer value or business value that this capability addresses?**: Stand-alone voucher creation and redemption; native UI for creation and admin; API for mid-tier redemption; admin visibility into redemptions and fraud.
- **What specific customer or business outcomes are we trying to achieve?**: [!] NOT ENOUGH INFORMATION - REQUIRES USER INPUT.
- **What is the user journey from start to finish for the primary use case?**: (1) Create campaign with voucher definition → (2) Create/add vouchers → (3) Publish voucher to customer (optional) → (4) Validate (eligibility, order rules) → (5) Redeem. Rollback is out of scope for the primary use case.
- **What are the key stages or steps in the user journey?**: (1) Campaign creation, (2) Voucher creation/import, (3) Publication (assign to customer, optional), (4) Validation, (5) Redemption. Rollback/management is out of scope.
- **Where in the user journey are users experiencing frustration, friction, or unhappiness?**: [!] NOT ENOUGH INFORMATION - REQUIRES USER INPUT.
- **What moments of delight or value should users experience during their journey?**: [!] NOT ENOUGH INFORMATION - REQUIRES USER INPUT.
- **What are the critical pain points that prevent users from achieving their goals?**: [!] NOT ENOUGH INFORMATION - REQUIRES USER INPUT.
- **What other systems, data sources, or tools does this capability need to interact with in order to deliver value?**: Stand-alone capability. (1) Native UI (within this system) for creating vouchers and campaigns. (2) Redemption API exposed to mid-tier; mid-tier sends redemption requests to the API, which persist in our backend. (3) Admin UI (within this system) for manual review: view redemptions, manage vouchers (enable/disable as needed), and review suspicious activity. No external CDP, CEP, POS, or e-commerce platform integrations.
- **What are the key behaviors or integration points that define how these systems support or depend on one another?**: Mid-tier calls redemption API with redemption requests; API validates, redeems, and persists results to backend. Admin uses native UI to create campaigns/vouchers and to review redemptions and manage vouchers manually. No outbound integrations to external systems.
- **What is the business domain we are modeling?**: Promotional/coupon management — voucher creation, redemption, and dynamic discount logic.
- **What are the core business concepts and their relationships?**: Campaign (1) → Vouchers (many); Customer (1) → Publications (many) ↔ Voucher (1); Voucher types: DISCOUNT_VOUCHER, GIFT_VOUCHER, LOYALTY_CARD; Redemption links voucher + customer + order; Validation ensures eligibility before redemption.
- **What are the distinct sub-domains or business capabilities?**: Voucher creation (standalone, campaign, bulk import via native UI); Redemption (validate, redeem via API; rollback out of scope); Targeting (segments, order rules); Governance (stacking, exclusions, fraud limits); Publication (assign voucher to customer, optional); Admin (review redemptions, manage vouchers, fraud review).
- **What are the boundaries between different parts of the domain?**: Native UI (creation, admin) vs redemption API (mid-tier); no external system integrations; rollback out of scope.
- **What domain events occur in this business domain?**: Voucher created, Campaign created, Voucher published, Voucher validated, Voucher redeemed, Voucher disabled/enabled. (Redemption rolled back is out of scope.)
- **What are the key business rules and constraints?**: Validate before redeem; stacking rules per project; redemption limits (per-voucher quantity); validity (start/end dates, days, hours); segment and order rules must match; formula fallback when evaluation fails. Rollback is out of scope.
- **What domain language do business experts use to describe this domain?**: Voucher, campaign, redemption, publication, holder, segment, stacking, discount (amount, percent, unit, fixed), dynamic coupon, formula, validation, rollback, channel.

### Evidence

- **voucherify_research**: context/initial_nico_chat.md
- **shape_clarification**: clarification.json (shape section)

### Decisions

**bounded_context_strategy:** How should domain concepts be grouped into bounded contexts?

- By sub-epic - Each sub-epic represents a bounded context
- By epic - Each epic represents a bounded context
- By business capability - Group concepts by business function
- Explicit contexts - Manually define context boundaries
- Single context - All concepts in one unified model
- Discover naturally - Let contexts emerge from concept relationships

**concept_discovery_source:** Where should domain concepts be discovered from?

- Story map only - Extract concepts from stories and epics
- Story map + interviews - Add concepts from domain expert conversations
- Story map + existing docs - Include concepts from current documentation
- Story map + code - Extract concepts from existing codebase
- Comprehensive - All sources including story map, interviews, docs, and code

**domain_detail_level:** How much detail should be captured for each domain concept?

- Minimal - Just concept names and high-level purpose
- Moderate - Concept names, responsibilities, key relationships
- Detailed - Full responsibilities, all collaborators, relationship types
- Comprehensive - Everything plus business rules, invariants, lifecycle

**domain_modeling_approach:** What approach should be used for domain modeling?

- Domain-Driven Design (DDD) - Rich domain model with entities, value objects, aggregates
- Resource-Oriented - Focus on nouns and resources from the business domain
- Event-Driven - Model domain events and event flows
- Service-Oriented - Model domain services and their interactions
- Lightweight - Simple concept identification with responsibilities
- Hybrid - Mix of approaches based on subdomain complexity

**relationship_depth:** How deeply should relationships between domain concepts be modeled?

- No relationships - Just list concepts independently
- Collaborators only - List which concepts work together
- Basic relationships - Collaborators with relationship types (has-a, uses, contains)
- Detailed relationships - Include cardinality, directionality, lifecycle dependencies
- Full relationship model - Everything including invariants and business rules


### Assumptions

- Domain concepts emerge from stories and business language, not technical implementation
- Use ubiquitous language from domain experts and business stakeholders
- Model domain concepts, not technical classes or database tables
- Focus on core domain concepts first, supporting concepts later
- Concepts are placed at the most specific level (sub-epic) and elevated to parent level only if shared
- Each bounded context has its own view of domain concepts with specific meanings
- Domain concepts capture WHAT exists in the business domain, not HOW it's implemented
- Responsibilities describe what a concept does in the business domain
- Collaborators show which concepts work together to accomplish business goals
- Relationships between concepts should reflect business rules and constraints
- Domain language should be understood by both business and technical teams
- Avoid generic technical terms (Manager, Handler, Service, Controller) in concept names
- Favor nouns and resources over verbs and actions
- Domain concepts should be technology-agnostic and implementation-independent
- Start lightweight - concept names and responsibilities - then add detail as needed
- Domain model refinement happens iteratively as understanding deepens
- Existing code and documentation are sources for concept discovery, not the definition
- Sub-epics typically represent bounded contexts with cohesive domain concepts

---
## Next action: validate
**Next:** Perform the following action. Fix any errors found in the Violation.

## Action Instructions - validate

The purpose of this action is to validate story graph and/or artifacts against behavior-specific rules, checking for violations and compliance

validate CRC model against CRC rules
Ensure CRC cards use ubiquitous language
Verify collaborators and responsibilities are clear
Verify every domain concept has a module field matching source folder structure

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

## Step 1: Run Scanners Then Review Violations

**Scanners you must run (with params below). Do not assume pre-run results.**

| Rule | Rule file | Scanner module |
|------|-----------|----------------|
| Integrate And Organize Concepts | `crc_bot/behaviors/domain/rules/integrate_and_organize_concepts.json` | `scanners.noun_redundancy_scanner.NounRedundancyScanner` |
| Use Module For Folder Structure | `crc_bot/behaviors/domain/rules/use_module_for_folder_structure.json` | `[Manual check - no scanner]` |
| Use Domain Language | `crc_bot/behaviors/domain/rules/use_domain_language.json` | `scanners.domain_language_scanner.DomainLanguageScanner` |
| Favor Code Representation | `crc_bot/behaviors/domain/rules/favor_code_representation.json` | `scanners.code_representation_scanner.CodeRepresentationScanner` |
| Scope Concepts Correctly | `crc_bot/behaviors/domain/rules/scope_concepts_correctly.json` | `[Manual check - no scanner]` |
| Use Natural English | `crc_bot/behaviors/domain/rules/use_natural_english.json` | `scanners.natural_english_scanner.NaturalEnglishScanner` |
| Use Resource Oriented Design | `crc_bot/behaviors/domain/rules/use_resource_oriented_design.json` | `scanners.resource_oriented_design_scanner.ResourceOrientedDesignScanner` |
| Shape Relationships From Story Map | `crc_bot/behaviors/domain/rules/shape_relationships_from_story_map.json` | `[Manual check - no scanner]` |

**Params to pass when running scanners:**
- **Scope:** all epics, sub-epics, stories, and domain concepts in the story graph
- **Workspace:** `C:\dev\vouchers`
- **Story graph path:** `docs/story/story-graph.json` (or behavior-specific path)

Run each scanner with the above scope and workspace; then report violations and fix the story graph as needed.

Run each scanner with the params above, then review the violations they report as follows:
1. For each violation message, locate the corresponding element in the story graph.
2. Open the relevant rule file and read all DO and DON'T examples thoroughly.
3. Decide if the violation is **Valid** (truly a rule breach per examples) or a **False Positive** (explain why if so).
4. Determine the **Root Cause** (e.g., 'incorrect concept naming', 'missing actor', etc.).
5. Assign a **Theme** grouping based on the type of issue (e.g., 'noun-only naming', 'incomplete acceptance criteria').
6. Extract an **Example** from the actual code/content showing the problem.
7. Suggest a clear, concrete **Fix** with a code example informed by DO examples in the rule.

## Step 2: Manual Rule Review

**Rules to validate against (read each file for full DO/DON'T examples):**

### Rule: Integrate And Organize Concepts (Priority 1) [Scanner]
**File:** `crc_bot/behaviors/domain/rules/integrate_and_organize_concepts.json`
**Description:** Integrate related capabilities under parent concepts and organize by business domain. Avoid noun redundancy by nesting related capabilities together, group by business capabilities not technical layers.
**DO:** Integrate related capabilities under parent concepts, organize by business domain
**DON'T:** Don't create redundant/fragmented concepts or group by technical layers

### Rule: Use Module For Folder Structure (Priority 1) [Scanner]
**File:** `crc_bot/behaviors/domain/rules/use_module_for_folder_structure.json`
**Description:** Use module field to map domain concepts to source code folder structure. Module names MUST exactly match folder paths where they exist using dot notation for nesting.
**DO:** Module names follow same conventions as classes and match actual folder structure
**DON'T:** Don't use generic module names, don't omit module field, don't use slash notation

### Rule: Use Domain Language (Priority 2) [Scanner]
**File:** `crc_bot/behaviors/domain/rules/use_domain_language.json`
**Description:** Use domain-specific language rooted in core business concepts. Avoid generic terms, technical patterns (Manager, Service, Handler, Factory), and capability verbs (Exposes, Provides, Contains). Name concepts and responsibilities using the ubiquitous language of the business domain.
**DO:** Use concrete domain language with specific behaviors and actions
**DON'T:** Don't use generic terms, technical patterns, or capability verbs

### Rule: Favor Code Representation (Priority 3) [Scanner]
**File:** `crc_bot/behaviors/domain/rules/favor_code_representation.json`
**Description:** Keep domain model tightly aligned to code it represents, use actual class names and method signatures, not prose descriptions. Show collaborators as types, not descriptions. Avoid over conceptualization.
**DO:** Keep code and domain model tightly aligned
**DON'T:** Don't use prose descriptions or vague terms

### Rule: Scope Concepts Correctly (Priority 3) [Scanner]
**File:** `crc_bot/behaviors/domain/rules/scope_concepts_correctly.json`
**Description:** Scope domain concepts correctly - place at the most specific level where relevant and ensure they represent complete functional capabilities. Use 'local' scope for single sub-epic concepts, 'global' for shared concepts. Concepts should be complete functional units, not fragments.
**DO:** Place concepts at correct scope level and ensure functional completeness
**DON'T:** Don't place concepts at wrong scope level or create incomplete fragments

### Rule: Use Natural English (Priority 6) [Scanner]
**File:** `crc_bot/behaviors/domain/rules/use_natural_english.json`
**Description:** Use natural English for responsibility names. Responsibilities should read like natural language method calls, using proper grammar and clear intent.
**DO:** Write responsibilities in natural English that clearly express intent
**DON'T:** Don't use awkward phrasing or overly technical grammar

### Rule: Use Resource Oriented Design (Priority 7) [Scanner]
**File:** `crc_bot/behaviors/domain/rules/use_resource_oriented_design.json`
**Description:** Use resource-oriented design where concepts represent resources with properties and behaviors. Focus on what the resource IS and HAS, not implementation operations.
**DO:** Model concepts as resources with properties and contained resources
**DON'T:** Don't violate encapsulation - objects should own their data, hide implementation details, and handle their own responsibilities

### Rule: Shape Relationships From Story Map (Priority 11) [Scanner]
**File:** `crc_bot/behaviors/domain/rules/shape_relationships_from_story_map.json`
**Description:** Shape domain concept relationships from the story map. Collaborators should come from stories showing how concepts work together to accomplish user goals.
**DO:** Derive collaborators from story interactions
**DON'T:** Don't invent collaborators not present in stories


Scanner tools don't cover or catch every rule violation. Do a second pass:
1. Carefully read each rule file, fully reviewing DO and DON'T sections, and every provided example.
2. Inspect all epics, sub-epics, stories, and domain concepts in the story graph for compliance.
3. Compare the properties and content of each element against the rule's requirements.
4. Document any violations the scanner could not find.
5. For each violation, extract an **Example** showing the problem and provide a **Fix** with code example.

## Violations Found

Record ALL findings (scanner + manual) using this readable format. Group by theme for narrow IDE chat panels:

### [Theme Name] (X violations)

**1. [Rule Name]**
- Location: `path.to.element`
- Status: Valid / False Positive
- Source: Scanner / Manual / Both
- Problem: `"actual problematic text"`
- Fix: `"corrected text"`
- Root Cause: Brief explanation

**2. [Rule Name]**
- Location: `path.to.element`
- ...

---

### [Next Theme] (Y violations)
...

Use this list format instead of tables - tables are unreadable in narrow IDE side chat panels.

## Step 3: Summarize Findings & Recommendations

Provide a concise summary:
- Report how many **scanner violations** were valid vs false positives.
- Enumerate any **additional manual findings** not caught by scanners.
- Group all violations by recurring theme or pattern.
- Split violations into **Priority Fixes** (must resolve before continuing) and **Optional Improvements**.

Present your summary and await user confirmation before automatically applying or proposing corrections.
validate CRC model against CRC rules
Ensure CRC cards use ubiquitous language
Verify collaborators and responsibilities are clear
Verify every domain concept has a module field matching source folder structure

---
## Next action: render
**Next:** Perform the following action.

## Action Instructions - render

The purpose of this action is to render output documents and artifacts from story graph using templates and synchronizers

render CRC model documents from story-graph.json

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

Please follow the instructions below in order to manually render output documents using templates

All render configurations are automatically loaded and injected below. Process ALL configs - do not skip any.



**Final Steps:**
- Process ALL configs above - do not skip any
- Priority order: synchronizer > template
- Verify each output file exists after execution
- If execution fails, report the error and continue with other outputs
- After completing all renders, pause and wait for human confirmation before proceeding to next behavior

**Creating New Render Outputs:**
If you need to create code to render a new output format:
1. Create a new synchronizer file in {workspace}/synchronizers/ (create folder if it doesn't exist)
2. Follow this signature pattern: output_file = synchronizer.render(story_graph_file)
3. The synchronizer should read the story-graph.json and produce the desired output file
4. Add the new synchronizer to the behavior's render config to include it in future renders
render CRC model documents from story-graph.json
IMPORTANT: After completing all template-based rendering, you MUST execute the synchronizer-based render specs by running: domain.render.renderAll
This will render the following outputs: render_crc_model_description, render_crc_model_diagram, render_crc_model_outline

---
## Next action: design.rules
**Next:** Perform the following action.

## Action Instructions - rules

The purpose of this action is to load behavior-specific rules into ai context for guidance on writing compliant content

Display design rules for this behavior as AI context

---


CRITICAL: This is the rules action - it loads rules for AI context. DO NOT run validation.
CRITICAL: You MUST systematically read each rule file listed below using the read_file tool BEFORE acting on the user's message.
Read ALL rule files first, then apply them to the user's request.
Each rule file path is provided - use read_file to load the complete rule content including examples.
After reading all rules, act on the user's message following ALL the rules you just read.

CRITICAL: When reporting validation results, use this EXACT format:
For each rule checked, report: Rule Name | PASS or FAIL | If FAIL, explain why in one sentence
Example: prefer_object_model_over_config | PASS
Example: eliminate_duplication | FAIL | Same logic repeated in lines 45-50 and 78-83
Keep it simple: just tell the user what passed, what failed, and if it failed, why.
Display design rules for this behavior as AI context

---
## Next action: design.clarify
**Next:** Perform the following action.

## Action Instructions - clarify

The purpose of this action is to gather context by asking required questions and collecting evidence in order to increase understanding

Gather context for technical design - understand architecture patterns and implementation constraints

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

Review all provided context, then for each required question below, thoughtfully answer it by thoroughly examining the context provided.

**Answer format:**
**Question:** [question text]
**Answer:** [your answer based on context]

If you can't answer from context, state: "[!] NOT ENOUGH INFORMATION - REQUIRES USER INPUT"
If a choice is needed, list available options and ask user to choose.
Don't guess or infer - be explicit when information is missing.

IMMEDIATELY after displaying your answers, save them to clarification.json WITHOUT WAITING for user confirmation.

IMPORTANT: Do NOT include decisions in clarification.json - decisions are made in the strategy action and saved to strategy.json.

Use this EXACT template format:
{
  "[behavior_name]": {
    "key_questions": {
      "answers": {
        "[Question 1 text]": "[Your answer to question 1]",
        "[Question 2 text]": "[Your answer to question 2]",
        "[Question 3 text]": "[Your answer to question 3]"
      }
    },
    "evidence": {
      "required": [
        "Requirements doc",
        "User interviews",
        "Product roadmap"
      ],
      "provided": {
        "requirements_doc": "path/to/doc",
        "other_source": "path/to/source"
      }
    },
    "context": [
      "Context item 1",
      "Context item 2"
    ]
  }
}

The user can then review and edit the clarification.json in the panel UI.
Gather context for technical design - understand architecture patterns and implementation constraints

---
## Next action: design.strategy
**Next:** Perform the following action.

## Action Instructions - strategy

The purpose of this action is to decide approach by capturing assumptions and decision criteria

Make strategic decisions about design patterns, object responsibilities, and dependency management

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

Review context then make all decisions and compile assumptions. Present analysis with your reasoning.

- For each assumption, state whether you accept it or propose a modification with justification.
- For each strategic decision, select the most appropriate option from available choices.
- Compile text-based assumptions as a list.
- Explain your reasoning based on context.

If context is insufficient, state: "[!] NOT ENOUGH INFORMATION" and ask for guidance.

IMMEDIATELY after presenting your analysis, save the decisions and assumptions to strategy.json WITHOUT WAITING for user confirmation.

Use this EXACT template format:
{
  "[behavior_name]": {
    "decisions": {
      "[Decision 1 key]": "[Selected option/value]",
      "[Decision 2 key]": "[Selected option/value]",
      "[Decision 3 key]": "[Selected option/value]"
    },
    "assumptions": [
      "Assumption 1 text",
      "Assumption 2 text",
      "Assumption 3 text"
    ]
  }
}

The user can then review and edit the strategy.json in the panel UI.
Make strategic decisions about design patterns, object responsibilities, and dependency management

---
## Next action: design.build
**Next:** Perform the following action.

## Action Instructions - build

The purpose of this action is to build story graph from content area and render using story graph renderer

design: refine CRC cards with OOP design patterns and detailed responsibilities
Apply encapsulation, delegation, and dependency injection patterns to CRC cards
Define clear object responsibilities and collaborations on each CRC card
Preserve module field from domain phase, update only if class location changed
Update story-graph.json domain_concepts with detailed design patterns and object interactions

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

@build-instructions.txt

**BUILD PROCESS:**

**1. Load Context**
Load clarification.json, planning.json, and source material from context sources (listed above).

**2. Load Build Configs**
From `c:\dev\agile_bots\bots\crc_bot/behaviors/design/content/`, each folder contains:
- `build_*.json` - Config (name, path, template, output)
- `instructions.json` - Build instructions
- `template-file.json` - Output schema/structure

**3. Execute Build**
1. Load config, instructions, and template (injected as 'story_graph_template')
2. Check if output file exists - read it FIRST
3. Follow instructions.json - match template structure exactly (check '_explanation' section)
4. Apply context from Step 1
5. If file exists: ADD/EXTEND only, never overwrite/delete
6. Validate against template schema
7. Write to `C:\dev\vouchers/{config.path}/{config.output}`
- Read existing files before changes - preserve all content
- Match template structure exactly - don't invent schemas
- Trace all knowledge to clarification/planning data
- Process builds sequentially - validate each

**4. SOURCE TRACEABILITY**
Knowledge artifacts should include source references when available:
- `context_source` field on epics, sub_epics, story_groups, stories, and domain concepts
- Format: `{"file": "filename.pdf", "page": "12", "section": "3.2.1 Payment Flow"}`
- For multiple sources: use array of source objects
- If source is chat/conversation: `{"type": "chat", "description": "User clarification on approval workflow"}`
- If source is code: `{"file": "path/to/file.py", "lines": "45-67", "function": "process_payment"}`
- Prefer tracing knowledge to a source when possible
- When source is unclear, mark as `{"type": "inferred", "basis": "description of inference basis"}`
design: refine CRC cards with OOP design patterns and detailed responsibilities
Apply encapsulation, delegation, and dependency injection patterns to CRC cards
Define clear object responsibilities and collaborations on each CRC card
Preserve module field from domain phase, update only if class location changed
Update story-graph.json domain_concepts with detailed design patterns and object interactions

When building or adding to the story graph follow these rules,
Rules to follow:

- **apply_exhaustive_decomposition**: Apply exhaustive logic decomposition. Cover all validation paths, calculation branches, and edge cases explicitly. Use inheritance for variations, not enumeration. Example: Order -> Creates, Validates, Calculates total, Submits (complete flow); ShippingCalculator base, InternationalShippingCalculator : ShippingCalculator (inheritance for variations).
  DO: Cover all logic paths, use inheritance for variations. Example: Order -> Creates, Validates, Calculates, Submits (complete flow); ShippingCalculator base with InternationalShippingCalculator : ShippingCalculator subclass (inheritance)
  DON'T: Don't enumerate permutations or skip logic steps. Example: ShippingCalculator with Calculates standard/express/overnight domestic/international (wrong - enumerate) vs base + subclass (right)

- **preserve_module_from_domain**: Preserve module field from domain phase and verify accuracy. Module MUST match source code folder structure using dot notation.
  DO: Preserve module field and verify it matches actual file locations after design refinements
  DON'T: Don't remove module field, don't change it without reason, don't use incorrect paths

- **assign_base_class_responsibilities**: When classes share responsibilities and collaborators, lift them into a base class. Use ': BaseClass' notation for inheritance. Reference base type in relationships instead of enumerating subtypes. Example: Scanner base with Scans/Reports; ImportPlacementScanner : Scanner adds Validates import ordering.
  DO: Abstract shared responsibilities into base class, subclasses add specific ones. Example: Scanner base with Scans/Reports; ImportPlacementScanner : Scanner adds specific validation
  DON'T: Don't duplicate responsibilities or enumerate all subtypes. Example: Each scanner duplicating Scans/Reports (wrong) vs inheriting from Scanner base (right)

- **respect_existing_delegation**: DO NOT add responsibilities that are already fulfilled through delegation to existing collaborators. If a class has a collaborator whose domain already covers an operation, the class orchestrates through that collaborator - it doesn't duplicate the work. Example: StoryNode has StoryNodeChildren collaborator, so Add child/Remove child/Find child are already handled - don't add them again.
  DO: Add ONLY responsibilities that are NEW business rules, coordinate multiple collaborators, or introduce NEW capabilities not covered by existing collaborators
  DON'T: Don't add responsibilities that restate what existing collaborators already do. Don't add child operations when you have a Children collection. Don't add serialization when you have a Serializer. Don't add navigation when you have a Navigator.

- **assign_helper_ownership**: Decompose large domain objects into focused assistants to maintain single responsibility and smaller surface area. Use Doer patterns (Helper, Calculator, Analyzer) when a concept has too many distinct responsibility areas. Assistants must be subordinate to and owned by the domain concept they serve. Example: Portfolio delegates to RiskAnalyzer, RebalanceCalculator, PerformanceAnalyzer.
  DO: Decompose large domain objects into assistants to maintain single responsibility. Example: Portfolio delegates to RiskAnalyzer, RebalanceCalculator, PerformanceAnalyzer (focused assistants)
  DON'T: Don't create unnecessary Doers or leave them without clear ownership. Example: OrderCalculator, OrderSubmitter (wrong - premature extraction) vs Order with Calculates/Submits (right)

- **place_at_lowest_level**: Place state and responsibilities at the lowest-level object that owns them. Delegate to lowest-level objects, chain dependencies through hierarchy. Example: Holding owns Symbol/Quantity and Calculates market value; Portfolio Has holdings and delegates to them.
  DO: Place state and responsibilities at lowest owner, chain dependencies through hierarchy. Example: Holding owns Symbol/Quantity and Calculates market value; Portfolio Has holdings and delegates
  DON'T: Don't place state/responsibilities too high, don't skip hierarchy levels. Example: Portfolio Calculates holding market value (wrong - doing Holding's work) vs Holding Calculates (right)

- **encapsulate_through_properties**: Objects internalize their own state and functionality, accessed through properties. Avoid methods that receive external state the object should already own. Example: LineItem owns Product/Quantity, so Calculates extended price: Money, Discount (not Money, Product, Quantity, Discount).
  DO: Objects own their state and expose it through properties. Example: LineItem owns Product/Quantity, Calculates extended price: Money, Discount (uses internal state)
  DON'T: Don't pass state to objects that should already own it. Example: LineItem Calculates: Money, Product, Quantity, Discount (wrong - passing owned state) vs Money, Discount (right)

- **object_creation_and_selection**: Objects create themselves from their context. Factory/registry selects which implementation to use, but creation logic belongs to the object being created. Example: Order Creates from shopping cart: Order, Cart, Customer; ScannerRegistry Finds scanner for rule: Scanner, Rule.
  DO: Objects create themselves, factory/registry selects implementations. Example: Order Creates from cart: Order, Cart, Customer (self-creation); ScannerRegistry Finds scanner: Scanner, Rule (selection)
  DON'T: Don't delegate creation to other objects, don't hardcode type selection. Example: Cart Creates order (wrong) vs Order Creates from cart (right); Factory Creates scanner (wrong) vs Registry Finds scanner (right)

- **ensure_unidirectional_ownership**: Ownership relationships must be unidirectional. If A owns B, B should not own A. References can be bidirectional, but ownership is one-way. Example: File Has blocks: Block (ownership down); Block References file: File (reference up).
  DO: Ownership flows one-way down hierarchy, references can point any direction. Example: File Has blocks (ownership down); Block References file (reference up)
  DON'T: Don't create circular ownership or confuse ownership with references. Example: File Has blocks + Block Has file (wrong - circular) vs Block References file (right)

---
## Next action: design.validate
**Next:** Perform the following action. Fix any errors found in the Violation.

## Action Instructions - validate

The purpose of this action is to validate story graph and/or artifacts against behavior-specific rules, checking for violations and compliance

design: validate OOP design against design principles
Ensure proper encapsulation, delegation, and dependency management
Verify object responsibilities follow SOLID principles
Verify module field preserved from domain phase and matches current source location

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

## Step 1: Run Scanners Then Review Violations

**Scanners you must run (with params below). Do not assume pre-run results.**

| Rule | Rule file | Scanner module |
|------|-----------|----------------|
| Apply Exhaustive Decomposition | `crc_bot/behaviors/design/rules/apply_exhaustive_decomposition.json` | `scanners.exhaustive_decomposition_scanner.ExhaustiveDecompositionScanner` |
| Preserve Module From Domain | `crc_bot/behaviors/design/rules/preserve_module_from_domain.json` | `[Manual check - no scanner]` |
| Assign Base Class Responsibilities | `crc_bot/behaviors/design/rules/assign_base_class_responsibilities.json` | `scanners.base_class_responsibilities_scanner.BaseClassResponsibilitiesScanner` |
| Respect Existing Delegation | `crc_bot/behaviors/design/rules/respect_existing_delegation.json` | `scanners.delegation_violation_scanner.DelegationViolationScanner` |
| Assign Helper Ownership | `crc_bot/behaviors/design/rules/assign_helper_ownership.json` | `scanners.helper_ownership_scanner.HelperOwnershipScanner` |
| Place At Lowest Level | `crc_bot/behaviors/design/rules/place_at_lowest_level.json` | `scanners.delegation_scanner.DelegationScanner` |
| Encapsulate Through Properties | `crc_bot/behaviors/design/rules/encapsulate_through_properties.json` | `scanners.property_encapsulation_scanner.PropertyEncapsulationScanner` |
| Object Creation And Selection | `crc_bot/behaviors/design/rules/object_creation_and_selection.json` | `scanners.self_creating_objects_scanner.SelfCreatingObjectsScanner` |
| Ensure Unidirectional Ownership | `crc_bot/behaviors/design/rules/ensure_unidirectional_ownership.json` | `scanners.unidirectional_ownership_scanner.UnidirectionalOwnershipScanner` |

**Params to pass when running scanners:**
- **Scope:** all epics, sub-epics, stories, and domain concepts in the story graph
- **Workspace:** `C:\dev\vouchers`
- **Story graph path:** `docs/story/story-graph.json` (or behavior-specific path)

Run each scanner with the above scope and workspace; then report violations and fix the story graph as needed.

Run each scanner with the params above, then review the violations they report as follows:
1. For each violation message, locate the corresponding element in the story graph.
2. Open the relevant rule file and read all DO and DON'T examples thoroughly.
3. Decide if the violation is **Valid** (truly a rule breach per examples) or a **False Positive** (explain why if so).
4. Determine the **Root Cause** (e.g., 'incorrect concept naming', 'missing actor', etc.).
5. Assign a **Theme** grouping based on the type of issue (e.g., 'noun-only naming', 'incomplete acceptance criteria').
6. Extract an **Example** from the actual code/content showing the problem.
7. Suggest a clear, concrete **Fix** with a code example informed by DO examples in the rule.

## Step 2: Manual Rule Review

**Rules to validate against (read each file for full DO/DON'T examples):**

### Rule: Apply Exhaustive Decomposition (Priority 1) [Scanner]
**File:** `crc_bot/behaviors/design/rules/apply_exhaustive_decomposition.json`
**Description:** Apply exhaustive logic decomposition. Cover all validation paths, calculation branches, and edge cases explicitly. Use inheritance for variations, not enumeration. Example: Order -> Creates, Validates, Calculates total, Submits (complete flow); ShippingCalculator base, InternationalShippingCalculator : ShippingCalculator (inheritance for variations).
**DO:** Cover all logic paths, use inheritance for variations. Example: Order -> Creates, Validates, Calculates, Submits (complete flow); ShippingCalculator base with InternationalShippingCalculator : ShippingCalculator subclass (inheritance)
**DON'T:** Don't enumerate permutations or skip logic steps. Example: ShippingCalculator with Calculates standard/express/overnight domestic/international (wrong - enumerate) vs base + subclass (right)

### Rule: Preserve Module From Domain (Priority 1) [Scanner]
**File:** `crc_bot/behaviors/design/rules/preserve_module_from_domain.json`
**Description:** Preserve module field from domain phase and verify accuracy. Module MUST match source code folder structure using dot notation.
**DO:** Preserve module field and verify it matches actual file locations after design refinements
**DON'T:** Don't remove module field, don't change it without reason, don't use incorrect paths

### Rule: Assign Base Class Responsibilities (Priority 2) [Scanner]
**File:** `crc_bot/behaviors/design/rules/assign_base_class_responsibilities.json`
**Description:** When classes share responsibilities and collaborators, lift them into a base class. Use ': BaseClass' notation for inheritance. Reference base type in relationships instead of enumerating subtypes. Example: Scanner base with Scans/Reports; ImportPlacementScanner : Scanner adds Validates import ordering.
**DO:** Abstract shared responsibilities into base class, subclasses add specific ones. Example: Scanner base with Scans/Reports; ImportPlacementScanner : Scanner adds specific validation
**DON'T:** Don't duplicate responsibilities or enumerate all subtypes. Example: Each scanner duplicating Scans/Reports (wrong) vs inheriting from Scanner base (right)

### Rule: Respect Existing Delegation (Priority 2) [Scanner]
**File:** `crc_bot/behaviors/design/rules/respect_existing_delegation.json`
**Description:** DO NOT add responsibilities that are already fulfilled through delegation to existing collaborators. If a class has a collaborator whose domain already covers an operation, the class orchestrates through that collaborator - it doesn't duplicate the work. Example: StoryNode has StoryNodeChildren collaborator, so Add child/Remove child/Find child are already handled - don't add them again.
**DO:** Add ONLY responsibilities that are NEW business rules, coordinate multiple collaborators, or introduce NEW capabilities not covered by existing collaborators
**DON'T:** Don't add responsibilities that restate what existing collaborators already do. Don't add child operations when you have a Children collection. Don't add serialization when you have a Serializer. Don't add navigation when you have a Navigator.

### Rule: Assign Helper Ownership (Priority 3) [Scanner]
**File:** `crc_bot/behaviors/design/rules/assign_helper_ownership.json`
**Description:** Decompose large domain objects into focused assistants to maintain single responsibility and smaller surface area. Use Doer patterns (Helper, Calculator, Analyzer) when a concept has too many distinct responsibility areas. Assistants must be subordinate to and owned by the domain concept they serve. Example: Portfolio delegates to RiskAnalyzer, RebalanceCalculator, PerformanceAnalyzer.
**DO:** Decompose large domain objects into assistants to maintain single responsibility. Example: Portfolio delegates to RiskAnalyzer, RebalanceCalculator, PerformanceAnalyzer (focused assistants)
**DON'T:** Don't create unnecessary Doers or leave them without clear ownership. Example: OrderCalculator, OrderSubmitter (wrong - premature extraction) vs Order with Calculates/Submits (right)

### Rule: Place At Lowest Level (Priority 4) [Scanner]
**File:** `crc_bot/behaviors/design/rules/place_at_lowest_level.json`
**Description:** Place state and responsibilities at the lowest-level object that owns them. Delegate to lowest-level objects, chain dependencies through hierarchy. Example: Holding owns Symbol/Quantity and Calculates market value; Portfolio Has holdings and delegates to them.
**DO:** Place state and responsibilities at lowest owner, chain dependencies through hierarchy. Example: Holding owns Symbol/Quantity and Calculates market value; Portfolio Has holdings and delegates
**DON'T:** Don't place state/responsibilities too high, don't skip hierarchy levels. Example: Portfolio Calculates holding market value (wrong - doing Holding's work) vs Holding Calculates (right)

### Rule: Encapsulate Through Properties (Priority 5) [Scanner]
**File:** `crc_bot/behaviors/design/rules/encapsulate_through_properties.json`
**Description:** Objects internalize their own state and functionality, accessed through properties. Avoid methods that receive external state the object should already own. Example: LineItem owns Product/Quantity, so Calculates extended price: Money, Discount (not Money, Product, Quantity, Discount).
**DO:** Objects own their state and expose it through properties. Example: LineItem owns Product/Quantity, Calculates extended price: Money, Discount (uses internal state)
**DON'T:** Don't pass state to objects that should already own it. Example: LineItem Calculates: Money, Product, Quantity, Discount (wrong - passing owned state) vs Money, Discount (right)

### Rule: Object Creation And Selection (Priority 8) [Scanner]
**File:** `crc_bot/behaviors/design/rules/object_creation_and_selection.json`
**Description:** Objects create themselves from their context. Factory/registry selects which implementation to use, but creation logic belongs to the object being created. Example: Order Creates from shopping cart: Order, Cart, Customer; ScannerRegistry Finds scanner for rule: Scanner, Rule.
**DO:** Objects create themselves, factory/registry selects implementations. Example: Order Creates from cart: Order, Cart, Customer (self-creation); ScannerRegistry Finds scanner: Scanner, Rule (selection)
**DON'T:** Don't delegate creation to other objects, don't hardcode type selection. Example: Cart Creates order (wrong) vs Order Creates from cart (right); Factory Creates scanner (wrong) vs Registry Finds scanner (right)

### Rule: Ensure Unidirectional Ownership (Priority 9) [Scanner]
**File:** `crc_bot/behaviors/design/rules/ensure_unidirectional_ownership.json`
**Description:** Ownership relationships must be unidirectional. If A owns B, B should not own A. References can be bidirectional, but ownership is one-way. Example: File Has blocks: Block (ownership down); Block References file: File (reference up).
**DO:** Ownership flows one-way down hierarchy, references can point any direction. Example: File Has blocks (ownership down); Block References file (reference up)
**DON'T:** Don't create circular ownership or confuse ownership with references. Example: File Has blocks + Block Has file (wrong - circular) vs Block References file (right)


Scanner tools don't cover or catch every rule violation. Do a second pass:
1. Carefully read each rule file, fully reviewing DO and DON'T sections, and every provided example.
2. Inspect all epics, sub-epics, stories, and domain concepts in the story graph for compliance.
3. Compare the properties and content of each element against the rule's requirements.
4. Document any violations the scanner could not find.
5. For each violation, extract an **Example** showing the problem and provide a **Fix** with code example.

## Violations Found

Record ALL findings (scanner + manual) using this readable format. Group by theme for narrow IDE chat panels:

### [Theme Name] (X violations)

**1. [Rule Name]**
- Location: `path.to.element`
- Status: Valid / False Positive
- Source: Scanner / Manual / Both
- Problem: `"actual problematic text"`
- Fix: `"corrected text"`
- Root Cause: Brief explanation

**2. [Rule Name]**
- Location: `path.to.element`
- ...

---

### [Next Theme] (Y violations)
...

Use this list format instead of tables - tables are unreadable in narrow IDE side chat panels.

## Step 3: Summarize Findings & Recommendations

Provide a concise summary:
- Report how many **scanner violations** were valid vs false positives.
- Enumerate any **additional manual findings** not caught by scanners.
- Group all violations by recurring theme or pattern.
- Split violations into **Priority Fixes** (must resolve before continuing) and **Optional Improvements**.

Present your summary and await user confirmation before automatically applying or proposing corrections.
design: validate OOP design against design principles
Ensure proper encapsulation, delegation, and dependency management
Verify object responsibilities follow SOLID principles
Verify module field preserved from domain phase and matches current source location

---
## Next action: design.render
**Next:** Perform the following action.

## Action Instructions - render

The purpose of this action is to render output documents and artifacts from story graph using templates and synchronizers

design: render design model documents and class diagrams

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

Please follow the instructions below in order to manually render output documents using templates

All render configurations are automatically loaded and injected below. Process ALL configs - do not skip any.

1. render_crc_class_diagram > manually generate C:\dev\vouchers\docs\crc\design\crc-class-diagram.mmd by taking C:\dev\vouchers\docs\crc\design\story-graph.json and transform using c:\dev\agile_bots\bots\crc_bot\behaviors\design\content\render\templates\class-diagram.mmd

2. render_crc_design_model > manually generate C:\dev\vouchers\docs\crc\design\crc-design-model.md by taking C:\dev\vouchers\docs\crc\design\story-graph.json and transform using c:\dev\agile_bots\bots\crc_bot\behaviors\design\content\render\templates\design-model.md


**Final Steps:**
- Process ALL configs above - do not skip any
- Priority order: synchronizer > template
- Verify each output file exists after execution
- If execution fails, report the error and continue with other outputs
- After completing all renders, pause and wait for human confirmation before proceeding to next behavior

**Creating New Render Outputs:**
If you need to create code to render a new output format:
1. Create a new synchronizer file in {workspace}/synchronizers/ (create folder if it doesn't exist)
2. Follow this signature pattern: output_file = synchronizer.render(story_graph_file)
3. The synchronizer should read the story-graph.json and produce the desired output file
4. Add the new synchronizer to the behavior's render config to include it in future renders
design: render design model documents and class diagrams
IMPORTANT: After completing all template-based rendering, you MUST execute the synchronizer-based render specs by running: design.render.renderAll
This will render the following outputs: render_crc_model_outline
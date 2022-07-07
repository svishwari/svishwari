export default {
  components: {
    alerts: {
      label: "Alerts",
      actions: [
        {
          type: "get_all",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_one",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "delete",
          admin: true,
          editor: false,
          viewer: false,
        },
      ],
    },
    destinations: {
      label: "Destinations",
      actions: [
        {
          type: "get_constants",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "validate",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_all",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_data_extensions",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "create_data_extensions",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "set_authentication_credentials",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "get_one",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "request_unsupported_destination",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "create_one",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "delete",
          admin: true,
          editor: false,
          viewer: false,
        },
      ],
    },
    audience: {
      label: "Audience",
      actions: [
        {
          type: "get_rules",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "create_lookalike",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "edit_lookalike",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "get_all",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "create",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "get_insights",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_countries",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_states",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_cities",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "download",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "get_one",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "update_one",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "delete_one",
          admin: true,
          editor: true,
          viewer: false,
        },
      ],
    },
    user: {
      label: "User",
      actions: [
        {
          type: "contact_us",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_profile",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_all",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "update_one",
          admin: true,
          editor: false,
          viewer: false,
        },
        {
          type: "create_favorite",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "delete_favorite",
          admin: true,
          editor: true,
          viewer: true,
        },
      ],
    },
    data_source: {
      label: "Data Source",
      actions: [
        {
          type: "get_all",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "request_new",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "delete_one",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "request_existing",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "get_datafeeds",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_one",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "update_list_of_data_sources",
          admin: true,
          editor: true,
          viewer: false,
        },
      ],
    },
    engagements: {
      label: "Engagements",
      actions: [
        {
          type: "get_all",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "create_one",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "get_ad_metrics",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_email_metrics",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "download_email_metrics",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "add_destination_to_engagement",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "remove_destination_from_engagement",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "add_audience_to_engagement",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "remove_audience_from_engagement",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "get_one",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "update_one",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "delete_one",
          admin: true,
          editor: true,
          viewer: false,
        },
      ],
    },
    models: {
      label: "Models",
      actions: [
        {
          type: "get_all",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "request_one",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "get_features",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_versions_history",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_overview",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_top_features",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_drift",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_lift",
          admin: true,
          editor: true,
          viewer: true,
        },
      ],
    },
    campaigns: {
      label: "Campaigns",
      actions: [
        {
          type: "get_list_of_campaigns",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "update_campaign_for_engagement",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "get_campaign_mappings",
          admin: true,
          editor: true,
          viewer: true,
        },
      ],
    },
    delivery: {
      label: "Delivery",
      actions: [
        {
          type: "schedule_delivery",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "delete_delivery",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "deliver",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "deliver_audience",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "deliver_engagement",
          admin: true,
          editor: true,
          viewer: false,
        },
        {
          type: "get_engagement_history",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_audience_history",
          admin: true,
          editor: true,
          viewer: true,
        },
      ],
    },
    customers: {
      label: "Customers",
      actions: [
        {
          type: "country_insights",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "revenue_insights",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "state_insights",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "city_insights",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "total_customer_insights",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "demographic_insights",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "customer_data_overview",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "list_of_customers",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "events_for_customer",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_customer_profile",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "filtered_customer_data_overview",
          admin: true,
          editor: true,
          viewer: true,
        },
      ],
    },
    idr: {
      label: "IDR",
      actions: [
        {
          type: "matching_trends",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "get_single_datafeed",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "data_feeds",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "idr_overview",
          admin: true,
          editor: true,
          viewer: true,
        },
      ],
    },
    trustid: {
      label: "Trust ID",
      actions: [
        {
          type: "trustid_overview",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "trustid_comparison",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "trustid_attributes",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "trustid_add_segment",
          admin: true,
          editor: true,
          viewer: true,
        },
        {
          type: "trustid_user_filters",
          admin: true,
          editor: true,
          viewer: true,
        },
      ],
    },
    client_config: {
      label: "Client Settings",
      actions: [
        {
          type: "client_settings",
          admin: true,
          editor: true,
          viewer: true,
        }
      ]
    },
  },
}

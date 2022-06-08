export default {
  settings: [
    {
      icon: "home",
      enabled: true,
      label: "Home",
      name: "Home"
    },
    {
      icon: "configuration",
      enabled: true,
      label: "Configuration",
      name: "Configuration"
    },
    {
      enabled: true,
      name: "Data Management",

      children: [
        {
          enabled: true,
          label: "Data Sources",
          icon: "datasource",
          name: "Data Sources"
        },
        {
          enabled: true,
          label: "Identity Resolution",
          icon: "identity-resolution",
          name: "Identity Resolution"
        },
      ],
    },
    {
      enabled: true,
      name: "Decisioning",
      children: [
        {
          enabled: true,
          label: "Models",
          icon: "models",
          name: "Models"
        },
      ],
    },
    {
      enabled: true,
      name: "Orchestration",
      children: [
        {
          enabled: true,
          label: "Destinations",
          icon: "multiple_map_pins",
          name: "Destinations"
        },
        {
          enabled: true,
          label: "Segment Playground",
          icon: "playground",
          name: "Segment Playground"
        },
        {
          enabled: true,
          label: "Audiences",
          icon: "audiences",
          name: "Audiences"
        },
        {
          enabled: true,
          label: "Engagements",
          icon: "speaker_up",
          name: "Engagements"
        },
      ],
    },
    {
      enabled: true,
      name: "Insights",
      children: [
        {
          enabled: true,
          label: "Customers",
          icon: "customer-profiles",
          name: "Customers"
        },
        {
          name: "HX TrustID",
          icon: "hx-trustid",
          superscript: "TM",
          label: "HX TrustID",
          enabled: true,
        },
        {
          enabled: true,
          label: "Email Deliverability",
          icon: "email_deliverability",
          name: "Email Deliverability"
        },
      ],
    },
  ],
}

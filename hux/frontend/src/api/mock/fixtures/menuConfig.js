export default {
  settings: [
    {
      enabled: true,
      name: "Home",
    },
    {
      enabled: true,
      name: "Configuration",
    },
    {
      enabled: true,
      name: "Data Management",
      children: [
        {
          name: "Data Sources",
          icon: "datasource",
          enabled: true,
        },
        {
          name: "Identity Resolution",
          icon: "identity-resolution",
          enabled: true,
        },
      ],
    },
    {
      enabled: true,
      name: "Decisioning",
      children: [
        {
          name: "Models",
          icon: "models",
          enabled: true,
        },
      ],
    },
    {
      enabled: true,
      name: "Orchestration",
      children: [
        {
          name: "Destinations",
          icon: "multiple_map_pins",
          enabled: true,
        },
        {
          name: "Segment Playground",
          icon: "playground",
          enabled: true,
        },
        {
          name: "Audiences",
          icon: "audiences",
          enabled: true,
        },
        {
          name: "Engagements",
          icon: "speaker_up",
          enabled: true,
        },
      ],
    },
    {
      enabled: true,
      name: "Insights",
      children: [
        {
          name: "Customers",
          icon: "customer-profiles",
          enabled: true,
        },
        {
          name: "HX TrustID",
          icon: "hx-trustid",
          superscript: "TM",
          enabled: true,
        },
        {
          name: "Email Deliverability",
          icon: "email_deliverability",
          enabled: true,
        },
      ],
    },
  ],
}

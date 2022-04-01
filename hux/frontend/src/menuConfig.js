import defaultState from "./store/defaultState"

const sideMenuOptions = {
  menu: [
    {
      label: null,
      icon: "home",
      title: "Home",
      link: {
        name: "Home",
      },
      display: true,
    },
    {
      label: null,
      icon: "configuration",
      title: "Configuration",
      link: {
        name: "Configuration",
      },
      display: true,
      defaultState: defaultState.configuration,
    },
    {
      label: "Data Management",
      menu: [
        {
          icon: "datasource",
          title: "Data Sources",
          link: {
            name: "DataSources",
          },
          size: 14,
          display: true,
          defaultState: defaultState.datasources,
        },
        {
          icon: "identity-resolution",
          title: "Identity Resolution",
          link: {
            name: "Identity",
          },
          size: 14,
          display: true,
          defaultState: defaultState.identityresolution,
        },
      ],
      display: true,
    },
    {
      label: "Decisioning",
      menu: [
        {
          icon: "models",
          title: "Models",
          link: {
            name: "Models",
          },
          size: 14,
          display: true,
          defaultState: defaultState.models,
        },
      ],
      display: true,
    },
    {
      label: "Orchestration",
      menu: [
        {
          icon: "multiple_map_pins",
          title: "Destinations",
          link: {
            name: "Destinations",
          },
          size: 16,
          display: true,
          defaultState: defaultState.destinations,
        },
        {
          icon: "playground",
          title: "Segment Playground",
          link: {
            name: "SegmentPlayground",
          },
          size: 14,
          display: true,
        },
        {
          icon: "audiences",
          title: "Audiences",
          link: {
            name: "Audiences",
          },
          size: 18,
          display: true,
          defaultState: defaultState.audiences,
        },
        {
          icon: "speaker_up",
          title: "Engagements",
          link: {
            name: "Engagements",
          },
          size: 16,
          display: true,
          defaultState: defaultState.engagements,
        },
      ],
      display: true,
    },
    {
      label: "Insights",
      menu: [
        {
          icon: "customer-profiles",
          title: "Customers",
          link: {
            name: "Customers",
          },
          size: 14,
          display: true,
          defaultState: defaultState.customerprofiles,
        },
        {
          icon: "hx-trustid",
          title: "HX TrustID",
          superscript: "TM",
          link: {
            name: "HXTrustID",
          },
          size: 14,
          display: true,
        },
        {
          icon: "email_deliverability",
          title: "Email Deliverability",
          link: {
            name: "EmailDeliverability",
          },
          size: 28,
          display: true,
          defaultState: defaultState.emaildeliverability,
        },
      ],
      display: true,
    },
  ],
}

export default sideMenuOptions

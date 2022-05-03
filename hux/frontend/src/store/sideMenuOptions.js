const sideMenuOptions = {
  home: {
    link: {
      name: "Home",
    },
  },

  configuration: {
    defaultState: {
      configurationModels: [],
    },
    link: {
      name: "Configuration",
    },
  },

  datasources: {
    defaultState: {
      items: {},
      dataFeedsDetails: [],
    },
    link: {
      name: "DataSources",
    },
  },

  identityresolution: {
    defaultState: {
      overview: {},

      timeFrame: {},

      dataFeeds: {},

      dataFeedReports: {},

      matchingTrends: [],
    },
    link: {
      name: "Identity",
    },
  },

  models: {
    defaultState: {
      items: {},
      overview: {},
      history: {},
      lift: [],
      features: [],
      drift: [],
      modelFeatures: [],
      pipelinePreformance: {},
    },
    link: {
      name: "Models",
    },
  },

  destinations: {
    defaultState: {
      items: {},
      constants: {},
      dataExtensions: [],
    },
    link: {
      name: "Destinations",
    },
  },

  segmentplayground: {
    link: {
      name: "SegmentPlayground",
    },
  },

  audiences: {
    defaultState: {
      audiences: [],

      newAudience: {
        name: "",
        engagements: [],
        attributeRules: [],
        destinations: [],
      },

      constants: {},

      deliveries: {},

      filteredDeliveries: [],

      demographics: {},

      geoCities: [],

      geoCountries: [],

      geoStates: [],
    },
    link: {
      name: "Audiences",
    },
  },

  engagements: {
    defaultState: {
      items: {},

      audiencePerformance: {
        ads: {},
        email: {},
      },

      deliveries: {},

      filteredDeliveries: [],

      campaignMappingOptions: {},
      campaignMappings: [],
    },
    link: {
      name: "Engagements",
    },
  },

  customers: {
    defaultState: {
      items: {},

      overview: {},

      // TODO: to be integrated with HUS-226
      insights: null,

      totalCustomers: [],

      totalCustomerSpend: [],

      geoOverview: [],

      geoCities: [],

      geoCountries: [],

      geoStates: [],

      demographics: {},

      events: [],
    },
    link: {
      name: "Customers",
    },
  },

  hxtrustid: {
    defaultState: {
      trustIdOverview: null,
      segmentComparison: [],
      addSegment: [],
      trustIdAttributes: [],
    },
    link: {
      name: "HXTrustID",
    },
  },

  emaildeliverability: {
    defaultState: {
      domain: {
        sent: [],
        open_Rate: [],
        delivered_rate: [],
        click_rate: [],
        unsubscribe_rate: [],
        complaints_rate: [],
      },
      overview: {},
    },
    link: {
      name: "EmailDeliverability",
    },
  },
}

export default sideMenuOptions

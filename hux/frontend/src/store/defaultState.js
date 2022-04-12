const defaultState = {
  configuration: {
    configurationModels: [],
  },

  datasources: {
    items: {},
    dataFeedsDetails: [],
  },

  identityresolution: {
    overview: {},

    timeFrame: {},

    dataFeeds: {},

    dataFeedReports: {},

    matchingTrends: [],
  },

  models: {
    items: {},
    overview: {},
    history: {},
    lift: [],
    features: [],
    drift: [],
    modelFeatures: [],
    pipelinePreformance: {},
  },

  destinations: {
    items: {},
    constants: {},
    dataExtensions: [],
  },

  audiences: {
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

  engagements: {
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

  customerprofiles: {
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

  emaildeliverability: {
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
  trustId: {
    trustIdOverview: null,
    segmentComparison: [],
    addSegment: [],
    trustIdAttributes: [],
  },
}

export default defaultState

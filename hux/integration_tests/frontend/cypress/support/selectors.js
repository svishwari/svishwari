/**
 * Selectors for DOM elements in the application.
 */
export default {
  home: {
    signin: "[data-e2e='signin']",
  },

  login: {
    email: "[id=okta-signin-username]",
    password: "[id=okta-signin-password]",
    remember: "[data-se-for-name=remember]",
    submit: "[id=okta-signin-submit]",
  },

  // common components
  card: {
    title: "[data-e2e='card-title']",
    description: "[data-e2e='card-description']",
  },

  // navigation
  nav: {
    models: "[data-e2e='nav-models']",
  },

  // overview
  overview: {
    header: "[data-e2e='overview-header']",
    list: "[data-e2e='configuration-list']",
    item: "[data-e2e='configuration-item']",
    chart: "[data-e2e='overview-chart']",
  },

  // connections
  datasources: "[data-e2e='dataSourcesList']",
  destinations: "[data-e2e='destinationsList']",
  dataSourcesAdd: "[data-e2e='dataSourcesAddList']",
  connections: "a[href='/connections']",
  addDataSource: "[data-e2e='addDataSource']",

  //destinations
  destination: {
    drawerToggle: "[data-e2e='drawerToggle']",
    addDestination: "[data-e2e='addDestination']",
    destinationsList: "[tabindex='0'][data-e2e='destinationsDrawer']",
    destinationConfigDetails: "[data-e2e='destinationConfigDetails']",
    validateDestination: "[data-e2e='validateDestination']",
    footer: "[data-e2e='footer']",
  },

  // decisioning
  models: {
    header: "[data-e2e='models-header']",
    list: "[data-e2e='models-list']",
    item: "[data-e2e='model-item']",
    models: "a[href='/models']",
    lifttable: "[data-e2e='table-lift']",
    featuretable: "[data-e2e='table-feature']",
    performancemetric: "[data-e2e='performancemetric']",
    driftchart: "[data-e2e='drift-chart']",
    featurechart: "[data-e2e='feature-chart']",
    versionhistorybutton: "[data-e2e='version-history-button']",
    versionhistory: "[data-e2e='version-history']",
  },

  // engagements
  engagement: {
    addEngagement: "[data-e2e='add-engagement']",
    addEngagements: "a[href='/engagements/add']",
    enagagementName: "[data-e2e='engagement-name']",
    enagagementDescription: "[data-e2e='engagement-description']",
    dataExtensionName: "[data-e2e='new-data-extension']",
    addAudience: "[data-e2e='add-audience']",
    addDestination: "[data-e2e='add-destination']",
    selectAudience: "[data-e2e='audience-select-button']",
    selectDestination: "[data-e2e='destination-select-button']",
    exitDrawer: "[data-e2e='click-outside']",
    exitDataExtensionDrawer: "[data-e2e='destination-added']",
    list: {
      engagementTable: "[data-e2e='engagement-table']",
      engagementTableHeaders: "table thead tr",
      engagementTableExpand: "[data-e2e='expand-engagement']",
      audienceTable: "[data-e2e='audience-table']",
      lastDeliveredColumn: "[data-e2e='last-delivered']",
      audienceTableExpand: "[data-e2e='expand-audience']",
    },
  },

  //Customer Profiles
  customerProfile: {
    customers: "a[href='/customers']",
    overview: "[data-e2e='overviewList']",
    customeroverview: "[data-e2e='customeroverview']",
    chart: "[data-e2e='overview-chart']",
    mapchart: "[data-e2e='map-chart']",
    mapStateList: "[data-e2e='map-state-list']",
    incomeChart: "[data-e2e='income-chart']",
    genderSpendChart: "[data-e2e='gender-spend-chart']",
    genderChart: "[data-e2e='gender-chart']",
    customerID: "[data-e2e='customerID']",
    customerlength: "[data-e2e='customer-length']",
    matchConfidence: "[data-e2e='match-confidence']",
    lifeTimeValue: "[data-e2e='life-time-value']",
    conversionTime: "[data-e2e='conversion-time']",
    churnScore: "[data-e2e='churn-score']",
    lastClick: "[data-e2e='last-click']",
    lastPurchaseDate: "[data-e2e='last-purchase-date']",
    lastOpen: "[data-e2e='last-open']",
    customerInsights: "[data-e2e='customer-insights']",
    contactPreferencecs: "[data-e2e='contact-preferencecs']",
    chord: "[data-e2e='chord']",
    loader: "[data-e2e='loader']",
    viewAllCustomers: "[data-e2e='view-all-customers']",
  },

  //IDR
  idr: {
    identityResolution: "a[href='/identity-resolution']",
    overview: "[data-e2e='overviewList']",
    datafeed: "[data-e2e='datafeedtable']",
    lastrun: "[data-e2e='lastrun']",
    pinning: "[data-e2e='Pinning']",
    stitched: "[data-e2e='Stitched']",
  },
  //notification
  notification: {
    notificationicon: "[data-e2e='notification-bell']",
    notificationReturnButton: "[data-e2e='notification-return']",
    notifications: "a[href='/notifications']",
    notificationlistmenu: "[data-e2e='notification-item']",
  },
  // navigation
  navigation: {
    profiledropdown: "[data-e2e='profile-dropdown']",
    profile: "[data-e2e='profile']",
    logout: "[data-e2e='logout']",
    help: "[data-e2e='help-dropdown']",
    contactus: "[data-e2e='contactus']",
    add: "[data-e2e='addicon']",
  },
  audience: {
    audiencelist: "[data-e2e='audiencelist']",
    audiencenameclick: "[data-e2e='audiencename']",
    audiencehistory: "[data-e2e='audience-history']",
    engagementdelivery: "[data-e2e='status-list']",
    deliveryhistory: "[data-e2e='delivery-history']",
    deliveryhistorydrawer: "[data-e2e='delivery-history-drawer']",
    overview: "[data-e2e='audience-overview']",
    mapchart: "[data-e2e='map-chart']",
    mapStateList: "[data-e2e='map-state-list']",
    incomeChart: "[data-e2e='income-chart']",
    genderSpendChart: "[data-e2e='gender-spend-chart']",
    genderChart: "[data-e2e='gender-chart']",
  },

  customers: "a[href='/customers']",
  engagements: "a[href='/engagements']",
  audiences: "a[href='/audiences']",
}

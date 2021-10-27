/**
 * Selectors for DOM elements in the application.
 */
export default {
  app: {
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

  // side navigation
  nav: {
    // app:
    home: "[data-e2e='nav-home']",
    configuration: "[data-e2e='nav-configuration']",

    // data management:
    dataSources: "[data-e2e='nav-datasource']",
    identityResolution: "[data-e2e='nav-identity-resolution']",

    // decisioning:
    models: "[data-e2e='nav-models']",

    // customer insights:
    customerProfiles: "[data-e2e='nav-customer-profiles']",
    segmentPlayground: "[data-e2e='nav-playground']",

    // orchestration:
    destinations: "[data-e2e='nav-destinations']",
    engagements: "[data-e2e='nav-speaker_up']",
    audiences: "[data-e2e='nav-audiences']",
  },

  // top navigation
  topNav: {
    profiledropdown: "[data-e2e='profile-dropdown']",
    profile: "[data-e2e='profile']",
    logout: "[data-e2e='logout']",
    help: "[data-e2e='help-dropdown']",
    contactus: "[data-e2e='contactus']",
    add: "[data-e2e='addicon']",
    dataSourceButton: "[data-e2e='Data Source']",
  },

  // home
  home: {
    welcomeBanner: "[data-e2e='welcome-banner']",
    totalCustomersChart: "[data-e2e='total-customers-chart']",
    latestNotifications: "[data-e2e='latest-notifications']",
    allNotificationsLink: "[data-e2e='all-notifications-link']",
  },

  // data sources
  datasources: "[data-e2e='dataSourcesList']",
  destinations: "[data-e2e='destination-list']",
  dataSourcesAdd: "[data-e2e='dataSourcesAddList']",
  addDataSource: "[data-e2e='addDataSource']",
  pendingDataSource: "[data-e2e='data-source-list-pending-button']",
  pendingDataSourceRemove: "[data-e2e='data-source-list-pending-remove']",
  removeDataSourceConfirmation: "[data-e2e='remove-data-source-confirmation']",

  //destinations
  destination: {
    drawerToggle: "[data-e2e='drawerToggle']",
    addDestination: "[data-e2e='addDestination']",
    destinationsList: "[tabindex='0'][data-e2e='destinationsDrawer']",
    destinationConfigDetails: "[data-e2e='destinationConfigDetails']",
    validateDestination: "[data-e2e='validateDestination']",
    footer: "[data-e2e='footer']",
    destinationRemove: "[data-e2e='destination-list-remove']",
    destinationRemoveConfirmFooter: ".confirm-modal-footer",
    destinationRemoveConfirmBody: ".confirm-modal-body",
    removeDestinationText: "[data-e2e='remove-destination-text']",
  },

  // decisioning
  models: {
    header: "[data-e2e='models-header']",
    list: "[data-e2e='models-list']",
    item: "[data-e2e='model-item']",
    lifttable: "[data-e2e='table-lift']",
    featuretable: "[data-e2e='table-feature']",
    performancemetric: "[data-e2e='performancemetric']",
    driftchart: "[data-e2e='drift-chart']",
    featurechart: "[data-e2e='feature-chart']",
    versionhistorybutton: "[data-e2e='version-history-button']",
    modelDashboardOptions: "[data-e2e='model-dashboard-options']",
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
    selectDestination: "[data-e2e='destination-select-button-qualtrics']",
    salesForceAddButton: "[data-e2e='destination-select-button-sfmc']",
    exitDrawer: "[data-e2e='click-outside']",
    exitDataExtensionDrawer: "[data-e2e='destination-added']",
    activeEngagement: "[data-e2e='enagement-active']",
    overviewSummary: "[data-e2e='overview-summary']",
    deliveryScheduleMetric: "[data-e2e='delivery-schedule-metric']",
    updatedMetric: "[data-e2e='updated-metric']",
    createdMetric: "[data-e2e='created-metric']",
    deliveryHistory: "[data-e2e='deliver-history']",
    deliveryHistoryItems: "[data-e2e='delivery-list-items']",
    adsData: "[data-e2e='ads-data']",
    emailData: "[data-e2e='email-data']",
    emailMarketing: "[data-e2e='email-marketing']",
    engagementAudienceList: "[data-e2e='status-list']",
    list: {
      engagementTable: "[data-e2e='engagement-table']",
      engagementTableHeaders: "table thead tr",
      engagementTableExpand: "[data-e2e='expand-engagement']",
      audienceTable: "[data-e2e='audience-table']",
      lastDeliveredColumn: "[data-e2e='last-delivered']",
      audienceTableExpand: "[data-e2e='expand-audience']",
    },
    destinationRows: '[data-e2e="destination-rows"]',
  },

  //Customer Profiles
  customerProfile: {
    customers: "a[href='/customers']",
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
    list: {
      geoDrawerTableCountry: "[data-e2e='geo-drawer-table-countries']",
      geoDrawerTableState: "[data-e2e='geo-drawer-table-states']",
      geoDrawerTableCity: "[data-e2e='geo-drawer-table-cities']",
      geoDrawerTableHeaders: "table thead tr",
      geoDrawerTableItems: "table tbody tr",
    },
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
    list: {
      audienceTable: "[data-e2e='audience-table']",
      audienceTableHeaders: "table thead tr",
      lastDeliveredColumn: "[data-e2e='last-delivered']",
    },
    addAudiences: "a[href='/audiences/add']",
    audienceName: "[data-e2e='audience-name']",
    addEngagement: "[data-e2e='add-engagement']",
    selectEngagement: "[data-e2e='engagement-list']",
    addDestination: "[data-e2e='add-destination-audience']",
    createAudience: "[data-e2e='create-audience']",
    salesForceAddButton: "[data-e2e='destination-select-button-sfmc']",
    newEngagementFirst: "[data-e2e='first-engagement-create']",
    newEngagementFirstName: "[data-e2e='new-engagement-name']",
    createNewEngagement: "[data-e2e='create-engagement-new']",
    cancelAudience: "[data-e2e='cancel-audience']",
    removeAudience: "[data-e2e='remove-audience-confirmation']",
  },
}

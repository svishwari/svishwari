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

  filter: {
    clear: "[data-e2e='clearFilter']",
    close: "[data-e2e='closeFilter']",
    apply: "[data-e2e='applyFilter']",
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
    destinations: "[data-e2e='nav-multiple_map_pins']",
    engagements: "[data-e2e='nav-speaker_up']",
    audiences: "[data-e2e='nav-audiences']",
  },

  // top navigation
  topNav: {
    profiledropdown: "[data-e2e='profile-dropdown']",
    profile: "[data-e2e='profile']",
    logout: "[data-e2e='logout']",
    help: "[data-e2e='help-dropdown']",
    myIssues: "[data-e2e='myIssues']",
    contactus: "[data-e2e='contactus']",
    add: "[data-e2e='addicon']",
    dataSourceButton: "[data-e2e='Data Source']",
    application: "[data-e2e='application-dropdown']",
    applicationOptions: "[data-e2e='application-options']",
  },

  // home
  home: {
    welcomeBanner: "[data-e2e='welcome-banner']",
    totalCustomersChart: "[data-e2e='total-customers-chart']",
    latestNotifications: "[data-e2e='latest-notifications']",
    allNotificationsLink: "[data-e2e='all-notifications-link']",
  },

  //client
  client: {
    clientDropdown: "[data-e2e='client_panel_dropdown']",
    clientPanelOpen: "[data-e2e='client_panel']",
    clientHeader: "[data-e2e='client-header']",
    clientLists: "[data-e2e='clients-list']",
    client: "[data-e2e='client']",
  },

  // my issues
  myIssues: {
    header: "[data-e2e='issues-header']",
    table: "[data-e2e='issues-table']",
    key: "[data-e2e='issues-key']",
    status: "[data-e2e='issues-status']",
    summary: "[data-e2e='issues-summary']",
    time: "[data-e2e='issues-time']",
    return: "[data-e2e='issues-return']",
    wrapper: "[data-e2e='issue-table-wrapper']",
  },

  // contact US
  contactUS: {
    contactUsOptions: "[data-e2e='contact-us-list']",
    reportBugSubject: "[data-e2e='report-bug-subject']",
    reportBugDescription: "[data-e2e='report-bug-description']",
  },

  // configuration
  configuration: {
    moduleSolution: "[data-e2e='moduleSolution']",
    teamMembers: "[data-e2e='teamMembers']",
    activeItem: "[data-e2e='activeItem']",
    tipsMenu: "[data-e2e='tips-menu']",
    list: {
      teamMembersTable: "[data-e2e='team-members-table']",
      teamMembersTableHeaders: "table thead tr",
    },
    teamMemberDrawer: {
      teamMemberRequest: "[data-e2e='teamMemberRequest']",
      firstName: "[data-e2e='firstName']",
      lastName: "[data-e2e='lastName']",
      email: "[data-e2e='email']",
      accessLevel: "[data-e2e='accessLevel']",
      togglePii: "[data-e2e='togglePii']",
      requestText: "[data-e2e='requestText']",
      request: "[data-e2e='request']",
    },
  },

  // data sources
  datasource: {
    datasources: "[data-e2e='dataSourcesList']",
    destinations: "[data-e2e='destination-list']",
    dataSourcesAdd: "[data-e2e='dataSourcesAddList']",
    dataSourcesRequest: "[data-e2e='dataSourcesRequestList']",
    addDataSource: "[data-e2e='addDataSource']",
    pendingDataSourceRemove: "[data-e2e='data-source-list-Pending-remove']",
    removeDataSourceConfirmation:
      "[data-e2e='remove-data-source-confirmation']",
    pendingStatus: "[data-e2e='model-status-Pending']",
    dataFeedDetailsTable: "[data-e2e='data-feed-details-table']",
    dataFilesWrapper: "[data-e2e='data-files-wrapper']",
    datasourceDatafeedsTable: "[data-e2e='datasource-datafeeds-table']",
    datasourceFilesTableFilter: "[data-e2e='filesTableFilter']",
    datasourceFilesTableFilterDrawer: "[data-e2e='dataFeedsFilters']",
    datasourceFilesTableFilterDrawerStatusPanel:
      "[data-e2e='dataFeedsFiltersStatusPanel']",
    datasourceFilesTableFilterDrawerTimePanel:
      "[data-e2e='dataFeedsFiltersTimePanel']",
    datasourceFilesTableFilterDrawerTimePanelToday:
      "[data-e2e='dataFeedsFiltersTimePanelToday']",
    datasourceFilesTableFilterDrawerTimePanelYesterday:
      "[data-e2e='dataFeedsFiltersTimePanelYesterday']",
    datasourceFilesStatus: "[data-e2e='filesStatusTooltip']",
    datasourceGroupedFilesExpand: "[data-e2e='expand-date-group']",
  },

  //destinations
  destination: {
    drawerToggle: "[data-e2e='drawerToggle']",
    addDestination: "[data-e2e='addDestination']",
    destinationsList: "[data-e2e='destinationsDrawer']",
    requestableDestinationsList: "[data-e2e='requestDestinationDrawer']",
    destinationConfigDetails: "[data-e2e='destinationConfigDetails']",
    validateDestination: "[data-e2e='validateDestination']",
    footer: "[data-e2e='footer']",
    destinationRemove: "[data-e2e='destination-list-remove']",
    destinationRemoveConfirmFooter: ".confirm-modal-footer",
    destinationRemoveConfirmBody: ".confirm-modal-body",
    removeDestinationText: "[data-e2e='remove-destination-text']",
    cancelRequestDestination: "[data-e2e='cancel-destination-request']",
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
    prevVersion: "[data-e2e='previous-versions']",
    status: "[data-e2e='model-status']",
    activeStatus: "[data-e2e='model-status-Active']",
    pendingStatus: "[data-e2e='model-status-Requested']",
    addModel: "[data-e2e='addModel']",
    requestModels: "[data-e2e='dataSourcesRequestList']",
    removeModel: "[data-e2e='remove-model']",
    removeModelConfirmation: "[data-e2e='remove-modal-confirmation']",
    pipelinePerformanceTab: "[data-e2e='pipeline-performance']",
  },

  // engagements
  engagement: {
    nextStep: "[data-e2e='next-step']",
    addEngagement: "[data-e2e='add-engagement']",
    addEngagements: "a[href='/engagements/add']",
    enagagementName: "[data-e2e='engagement-name']",
    enagagementDescription: "[data-e2e='engagement-description']",
    dataExtensionName: "[data-e2e='new-data-extension']",
    addAudience: "[data-e2e='add-audience']",
    addDestination: "[data-e2e='add-destination']",
    selectAudience: "[data-e2e='audience-select-button']",
    selectDestination: "[data-e2e='destination-select-button-facebook']",
    salesForceAddButton: "[data-e2e='destination-select-button-sfmc']",
    exitDrawer: "[data-e2e='click-outside']",
    exitDataExtensionDrawer: "[data-e2e='destination-added']",
    activeEngagement: "[data-e2e='enagement-active']",
    overviewSummary: "[data-e2e='overview-summary']",
    deliveryScheduleMetric: "[data-e2e='delivery-schedule-metric']",
    updatedMetric: "[data-e2e='updated-metric']",
    createdMetric: "[data-e2e='created-metric']",
    deliveryHistory: "[data-e2e='delivery-history']",
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
    createEngagement: '[data-e2e="create-engagement"]',
    allEngagements: '[data-e2e="engagement-breadcrumb"]',
    engagementTabs: '[data-e2e="engagement-tabs"]',
    overviewMetrics: '[data-e2e="overview-metrics"]',
    overviewAudiences: '[data-e2e="overview-audiences"]',
    advertisingOverview: '[data-e2e="advertising-overview"]',
    emailOverview: '[data-e2e="email-overview"]',
    accessActions: '[data-e2e="access-actions"]',
    actions: '[data-e2e="actions"]',
  },

  //Customer Profiles
  customerProfile: {
    customers: "a[href='/customers']",
    customeroverview: "[data-e2e='customeroverview']",
    customerListTab: "[data-e2e='customer-list-tab']",
    totalCustomerchart: "[data-e2e='total-customer-chart']",
    customerSpendchart: "[data-e2e='customer-spend-chart']",
    mapchart: "[data-e2e='map-chart']",
    mapStateList: "[data-e2e='map-state-list']",
    incomeChart: "[data-e2e='income-chart']",
    genderSpendChart: "[data-e2e='gender-spend-chart']",
    genderChart: "[data-e2e='gender-chart']",
    customerID: "[data-e2e='customerID']",
    customerlength: "[data-e2e='customer-length']",
    matchConfidence: "[data-e2e='match-confidence']",
    conversionTime: "[data-e2e='conversion-time']",
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
    eventsDrawerButton: "[data-e2e='eventsDrawerButton']",
    customerEventRow: "[data-e2e='customerEventRow']",
    customerEventchart: "[data-e2e='customer-event-chart']",
  },

  //IDR
  idr: {
    identityResolution: "a[href='/identity-resolution']",
    overview: "[data-e2e='overviewList']",
    datafeed: "[data-e2e='datafeedtable']",
    lastrun: "[data-e2e='lastrun']",
    pinning: "[data-e2e='tab-pinning']",
    stitched: "[data-e2e='tab-stitched']",
  },
  // notification
  notification: {
    notificationicon: "[data-e2e='notification-bell']",
    notificationReturnButton: "[data-e2e='notification-return']",
    viewAllNotifications: "[data-e2e='notifications-view-all']",
    notificationlistmenu: "[data-e2e='notification-item']",
  },
  audience: {
    audienceFilterToggle: "[data-e2e='audienceFilterToggle']",
    audienceFilters: "[data-e2e='audienceFilters']",
    audiencelist: "[data-e2e='audiencelist']",
    audiencenameclick: "[data-e2e='audiencename']",
    audiencehistory: "[data-e2e='audience-history']",
    engagementdelivery: "[data-e2e='status-list']",
    deliveryhistory: "[data-e2e='delivery-history']",
    deliveryhistorydrawer: "[data-e2e='delivery-history-drawer']",
    overview: "[data-e2e='audience-overview']",
    audienceChart: "[data-e2e='total-audience-chart']",
    spendChart: "[data-e2e='audience-spend-chart']",
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
    addAudiences: "a[href='/segment-playground']",
    audienceName: "[data-e2e='audience-name']",
    actionAudience: "[data-e2e='action-audience']",
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
    addNewAudience: "[data-e2e='add-audience']",
    editAudienceName: "[data-e2e='edit-audience-name']",
    engagementDeliveryDetails: "[data-e2e='engagement-delivery-details']",
    standaloneDelivery: "[data-e2e='standalone-delivery']",
    deliveryTab: "[data-e2e='delivery-tab']",
    insightsTab: "[data-e2e='insights-tab']",
    matchRateTable: "[data-e2e='audience-matchrates']",
    lookalikes: "[data-e2e='lookalike-audiences']",
    allAudiences: "[data-e2e='audience-breadcrumb']",
  },

  segmentPlayground: {
    addNewAttr: "[data-e2e='add-new-attr']",
    removeAttr: "[data-e2e='remove-attr']",
    selectAttrBtn: "[data-e2e='select-attr-btn']",
    selectOperatorBtn: "[data-e2e='select-operator-btn']",
    autoCompleteBtn: "[data-e2e='auto-complete-btn']",
  },

  //applications
  application: {
    addDrawer: "[data-e2e='drawerToggle']",
    cancel: "[data-e2e='cancel-application-request']",
    applications: "[data-e2e='applicationsDrawer']",
  },

  // email deliverability
  emailDeliverability: {
    overview: "[data-e2e='deliverability-overview']",
    deliveredChart: "[data-e2e='delivered-count-open-rate-chart']",
    sendingDomainOverview: {
      domainOverviewTable: "[data-e2e='sending-domain-overview']",
      overviewTableHeaders: "table thead tr",
      overviewTableItems: "table tbody tr",
    },
    sentDomain: "[data-e2e='sent-domain-chart']",
    deliveredRateDomain: "[data-e2e='delivered-rate-domain-chart']",
    openRateDomain: "[data-e2e='open-rate-domain-chart']",
    clickRateDomain: "[data-e2e='click-rate-domain-chart']",
    unsubscribeRateDomain: "[data-e2e='unsubscribe-rate-domain-chart']",
    complainsRateDomain: "[data-e2e='complaints-rate-domain-chart']",
  },
}

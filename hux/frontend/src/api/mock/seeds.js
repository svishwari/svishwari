// data sources

const bluecore = {
  name: "Bluecore",
  type: "bluecore",
  is_enabled: true,
  is_added: true,
  status: "Active",
}

const netsuite = {
  name: "Netsuite",
  type: "netsuite",
  is_enabled: true,
}

const aqfer = {
  name: "Aqfer",
  type: "aqfer",
  is_enabled: true,
  is_added: true,
  status: "Active",
}

const amazonAdvertising = {
  name: "Amazon Advertising",
  type: "amazon-advertising",
  is_enabled: false,
}

const amazonS3 = {
  name: "Amazon S3",
  type: "amazon-s3",
  is_enabled: false,
}

const aol = {
  name: "Aol",
  type: "aol",
  is_enabled: false,
}

const apacheHive = {
  name: "Apache Hive",
  type: "apache-hive",
  is_enabled: false,
}

const azureBlob = {
  name: "Azure Blob",
  type: "azure-blob",
  is_enabled: false,
}

const googleAds = {
  name: "Google Ads",
  type: "google-ads",
  is_enabled: false,
}

const GA360 = {
  name: "GA360",
  type: "GA360",
  is_enabled: false,
}

const gmail = {
  name: "Gmail",
  type: "gmail",
  is_enabled: false,
}

const googleAnalytics = {
  name: "Google Analytics",
  type: "google-analytics",
  is_enabled: false,
}

const IBMDB2 = {
  name: "IBMDB2",
  type: "IBMDB2",
  is_enabled: false,
}

const insightIQ = {
  name: "InsightIQ",
  type: "insightIQ",
  is_enabled: false,
}

const jira = {
  name: "Jira",
  type: "jira",
  is_enabled: false,
}

const mailchimpDS = {
  name: "Mailchimp",
  type: "mailchimp",
  is_enabled: false,
}

const mandrill = {
  name: "Mandrill",
  type: "mandrill",
  is_enabled: false,
}

const mariaDB = {
  name: "Maria DB",
  type: "mariaDB",
  is_enabled: false,
}

const medallia = {
  name: "Medallia",
  type: "medallia",
  is_enabled: false,
}

const microsoftAzureSQL = {
  name: "Microsoft Azure SQL",
  type: "microsoftAzureSQL",
  is_enabled: false,
}

const qualtrics = {
  name: "Qualtrics",
  type: "qualtrics",
  is_enabled: true,
}

const tableauDS = {
  name: "Tableau",
  type: "tableau",
  is_enabled: false,
}

const twilioDS = {
  name: "Twilio",
  type: "twilio",
  is_enabled: false,
}

// destinations
const facebook = {
  name: "Facebook",
  type: "facebook",
  is_enabled: true,
  is_added: true,
}

const sfmc = {
  name: "Salesforce Marketing Cloud",
  type: "sfmc",
  is_enabled: true,
  is_added: true,
}

const adobe = {
  name: "Adobe Experience",
  type: "adobe-experience",
}

const google = {
  name: "Google Ads",
  type: "google-ads",
}

const sendgrid = {
  name: "SendGrid by Twilio",
  type: "sendgrid",
}

const tableau = {
  name: "Tableau",
  type: "tableau",
}

const mailchimp = {
  name: "Mailchimp",
  type: "mailchimp",
}

const qualtricsDS = {
  name: "Qualtrics",
  type: "qualtrics",
}

// engagements
const defaultEngagement = ({ audiences = [] }) => {
  return {
    name: "Default engagement",
    description: null,
    delivery_schedule: null,
    status: "Delivered",
    audiences: audiences,
  }
}

// models
export const unsubscribeModel = {
  name: "Propensity to Unsubscribe",
  status: "Active",
  type: "unsubscribe",
  id: "2",
}

export const ltvModel = {
  name: "LTV",
  status: "Pending",
  type: "ltv",
  id: "1",
}

// audiences
const defaultAudience = ({ destinations = [], engagements = [] }) => {
  return {
    destinations: destinations,
    engagements: engagements,
    filters: [
      {
        section_aggregator: "ALL",
        section_filters: [
          {
            field: "filter_field",
            type: "type",
            value: "value",
          },
        ],
      },
    ],
    name: "My Audience",
  }
}

const multipleSectionFilters = () => {
  return {
    updated_by: "Rahul Goel",
    created_by: "Rahul Goel",
    audience_insights: {
      total_customers: 121321321,
      total_countries: 2,
      total_us_states: 28,
      total_cities: 246,
      min_age: 34,
      max_age: 100,
      gender_women: 0.4651031,
      gender_men: 0.481924,
      gender_other: 0.25219,
    },
    destinations: [],
    filters: [
      {
        section_aggregator: "ALL",
        section_filters: [
          {
            field: "propensity_to_unsubscribe",
            type: "range",
            value: [0.3, 0.5],
          },
          {
            field: "age",
            type: "range",
            value: [18, 30],
          },
          {
            field: "gender",
            type: "equals",
            value: "female",
          },
        ],
      },
      {
        section_aggregator: "ALL",
        section_filters: [
          {
            field: "propensity_to_purchase",
            type: "range",
            value: [0.55, 0.75],
          },
          {
            field: "age",
            type: "range",
            value: [30, 60],
          },
          {
            field: "gender",
            type: "equals",
            value: "male",
          },
        ],
      },
      {
        section_aggregator: "ALL",
        section_filters: [
          {
            field: "predicted_lifetime_value",
            type: "range",
            value: [3500, 6000],
          },
          {
            field: "City",
            type: "contains",
            value: "New York",
          },
          {
            field: "Zip code",
            type: "contains",
            value: "26H12219",
          },
        ],
      },
    ],
    name: "Audience with multiple filters",
    last_delivered: "2019-04-28T06:39:31.659551",
    create_time: "2021-06-24T18:44:00.381000",
    size: 3022188,
    update_time: "2021-06-24T18:44:00.381000",
  }
}

const likelyCustomer = () => {
  return {
    updated_by: "Rahul Goel",
    created_by: "Rahul Goel",
    is_lookalike: true,
    audience_insights: {
      total_customers: 121321321,
      total_countries: 2,
      total_us_states: 28,
      total_cities: 246,
      min_age: 34,
      max_age: 100,
      gender_women: 0.4651031,
      gender_men: 0.481924,
      gender_other: 0.25219,
    },
    destinations: [],
    filters: [
      {
        section_aggregator: "ALL",
        section_filters: [
          {
            field: "propensity_to_unsubscribe",
            type: "range",
            value: [0.7, 1],
          },
        ],
      },
    ],
    name: "Customers likely to unsubscribe",
    last_delivered: "2019-04-28T06:39:31.659551",
    create_time: "2021-06-24T18:44:00.381000",
    size: 3022188,
    id: "60d4d270d364622dd6cc9a7",
    update_time: "2021-06-24T18:44:00.381000",
  }
}
const sampleEng = {
  create_time: "2021-07-15T19:13:26.281Z",
  update_time: "2021-07-15T19:13:26.281Z",
  audiences: [
    {
      id: "2",
      destinations: [
        {
          latest_delivery: {
            status: "Not Delivered",
            size: 1000,
          },
        },
      ],
      status: "Not Delivered",
    },
  ],
  id: "60f088d6c297e84b3a9e7514",
  created_by: "Rahul Goel",
  updated_by: "",
  status: "Not Delivered",
  description: "Pre-Demo Test Engagement",
  name: "Pre-Demo Test Engagement",
}

export default function (server) {
  // seed data sources
  server.create("dataSource", bluecore)
  server.create("dataSource", netsuite)
  server.create("dataSource", aqfer)
  server.create("dataSource", amazonAdvertising)
  server.create("dataSource", amazonS3)
  server.create("dataSource", aol)
  server.create("dataSource", apacheHive)
  server.create("dataSource", azureBlob)
  server.create("dataSource", googleAds)
  server.create("dataSource", GA360)
  server.create("dataSource", gmail)
  server.create("dataSource", googleAnalytics)
  server.create("dataSource", IBMDB2)
  server.create("dataSource", insightIQ)
  server.create("dataSource", jira)
  server.create("dataSource", mailchimpDS)
  server.create("dataSource", mandrill)
  server.create("dataSource", mariaDB)
  server.create("dataSource", medallia)
  server.create("dataSource", microsoftAzureSQL)
  server.create("dataSource", qualtricsDS)
  server.create("dataSource", tableauDS)
  server.create("dataSource", twilioDS)

  // seed destinations
  server.create("destination", sendgrid)
  server.create("destination", google)
  server.create("destination", tableau)
  server.create("destination", sfmc)
  server.create("destination", adobe)
  server.create("destination", mailchimp)
  server.create("destination", qualtrics)
  const facebookSeed = server.create("destination", facebook)

  // seed audiences
  const defaultAudienceSeed = server.create(
    "audience",
    defaultAudience({
      destinations: [facebookSeed],
      // engagements: [engagementSeed],
    })
  )
  server.create("audience", multipleSectionFilters())
  // look alike audiences
  server.create("audience", likelyCustomer())
  server.createList("audience", 10)
  server.create("audience", { created_by: null, updated_by: null })

  // seed engagements
  server.createList("engagement", 5)

  // TODO: define relationships in model, for now use the attrs from HUS-579
  server.create(
    "engagement",
    defaultEngagement({
      audiences: [
        {
          id: defaultAudienceSeed.id,
          name: defaultAudienceSeed.name,
          size: defaultAudienceSeed.size,
          create_time: defaultAudienceSeed.create_time,
          created_by: defaultAudienceSeed.created_by,
          update_time: defaultAudienceSeed.update_time,
          updated_by: defaultAudienceSeed.updated_by,
          status: "Delivered",
          destinations: defaultAudienceSeed.destinations.models.map(
            (destination) => {
              return {
                id: destination.id,
                name: "Facebook",
                type: "facebook",
                latest_delivery: {
                  id: "60ae035b6c5bf45da27f17e5",
                  status: "Delivered",
                  update_time: "2021-06-14T18:07:18.415",
                  size: 1000,
                },
              }
            }
          ),
        },
      ],
    })
  )

  // seed Engagement Audience Performance
  server.createList("audiencePerformance", 10)
  server.create("engagement", sampleEng)

  // seed models
  server.create("model", unsubscribeModel)
  server.create("model", ltvModel)

  // seed customers
  server.createList("customer", 5000)

  // seed data-extensions
  server.createList("dataExtension", 5)

  // seed campaigns
  server.createList("campaignOption", 1)

  // seed notifications
  server.createList("notification", 1000)

  // seed idr datafeeds
  server.createList("idrDataFeed", 10)

  // seed geo states, countries, cities
  server.createList("geoCity", 14659)
  server.create("geoCountry", { country: "United States" })
  server.createList("geoState", 52)
}

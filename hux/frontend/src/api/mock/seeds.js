// data sources

const bluecore = {
  name: "Bluecore",
  type: "bluecore",
  is_enabled: true,
  is_added: true,
  status: "active",
}

const facebookDS = {
  name: "Facebook",
  type: "facebook",
  is_enabled: true,
}

const sfmcDS = {
  name: "Salesforce Marketing Cloud",
  type: "salesforce",
  is_enabled: true,
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
  is_enabled: false,
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
  authentication_details: {
    ad_account_id: {
      name: "Ad Account ID",
      type: "text",
      required: true,
      description: "Placeholder information text for 'Ad Account ID'",
    },
    app_id: {
      name: "App ID",
      type: "text",
      required: true,
      description: "Placeholder information text for 'App ID'",
    },
    access_token: {
      name: "Access Token",
      type: "password",
      required: true,
      description: "Placeholder information text for 'Access Token'",
    },
    app_secret: {
      name: "App Secret",
      type: "password",
      required: true,
      description: "Placeholder information text for 'App Secret'",
    },
  },
}

const salesforce = {
  name: "Salesforce Marketing Cloud",
  type: "salesforce",
  is_enabled: true,
  authentication_details: {
    sfmc_account_id: {
      name: "Account ID",
      type: "text",
      required: true,
      description: "Placeholder information text for 'Account ID'",
    },
    sfmc_auth_base_uri: {
      name: "Auth Base URI",
      type: "text",
      required: true,
      description: "Placeholder information text for 'Auth Base URI'",
    },
    sfmc_client_id: {
      name: "Client ID",
      type: "text",
      required: true,
      description: "Placeholder information text for 'Client ID'",
    },
    sfmc_client_secret: {
      name: "Client Secret",
      type: "password",
      required: true,
      description: "Placeholder information text for 'Client Secret'",
    },
    sfmc_rest_base_uri: {
      name: "REST Base URI",
      type: "text",
      required: true,
      description: "Placeholder information text for 'REST Base URI'",
    },
    sfmc_soap_base_uri: {
      name: "Soap Base URI",
      type: "text",
      required: true,
      description: "Placeholder information text for 'Soap Base URI",
    },
  },
}

const adobe = {
  name: "Adobe Experience",
  type: "adobe-experience",
}

const google = {
  name: "Google Ads",
  type: "google-ads",
}

const twilio = {
  name: "Twilio",
  type: "twilio",
}

const tableau = {
  name: "Tableau",
  type: "tableau",
}

const mailchimp = {
  name: "Mailchimp",
  type: "mailchimp",
}

// engagements
const defaultEngagement = {
  name: "Default engagement",
  description: "Default Description",
  delivery_schedule: {
    schedule_type: "recurring",
    start_date: "01/05/2021",
    end_date: "01/14/2021",
  },
}

// models
const unsubscribeModel = {
  name: "Propensity to Unsubscribe",
  status: "pending",
}

export default function (server) {
  // seed data sources
  server.create("dataSource", bluecore)
  server.create("dataSource", facebookDS)
  server.create("dataSource", sfmcDS)
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
  server.create("dataSource", qualtrics)
  server.create("dataSource", tableauDS)
  server.create("dataSource", twilioDS)

  // seed destinations
  server.create("destination", facebook)
  server.create("destination", salesforce)
  server.create("destination", twilio)
  server.create("destination", google)
  server.create("destination", tableau)
  server.create("destination", adobe)
  server.create("destination", mailchimp)

  // seed engagements
  server.create("engagement", defaultEngagement)

  // seed models
  server.create("model", unsubscribeModel)

  //seed audiences
  server.createList("audience", 10)
}

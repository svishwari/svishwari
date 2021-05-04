const facebook = {
  name: "Facebook",
  type: "facebook",
  is_enabled: true,
  auth_details: {
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
  auth_details: {
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

export default function (server) {
  // seed destinations
  server.create("destination", facebook)
  server.create("destination", salesforce)
  server.create("destination", twilio)
  server.create("destination", google)
  server.create("destination", tableau)
  server.create("destination", adobe)
  server.create("destination", mailchimp)
}

import faker from "faker"

/**
 * Destination schema
 */
export const destination = {
  name: "Facebook",
  type: "facebook",
  status: "Active",
  category: "Advertising",

  is_enabled: false,
  is_added: false,

  create_time: () => faker.date.recent(),
  created_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
  update_time: () => faker.date.recent(),
  updated_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),

  engagements: () => faker.datatype.number({ min: 0, max: 10 }),

  // request destination fields
  contact_email: null,
  client_request: null,
  client_account: null,
  use_case: null,
}

/**
 * Destination field schema
 *
 * @param {object} field field configuration
 * @param {string} field.name field name
 * @param {string} field.type field type
 * @param {boolean} field.required flag whether field is required
 * @param {string} field.description field's description
 * @returns {object} the field object
 */
const field = ({
  name,
  type = "text",
  required = true,
  description = null,
}) => {
  return {
    name: name,
    type: type,
    required: required,
    description: description,
  }
}

/**
 * Destination constants schema
 */
export const destinationsConstants = {
  facebook: {
    facebook_ad_account_id: field({ name: "Ad Account ID" }),
    facebook_app_id: field({ name: "App ID" }),
    facebook_app_secret: field({
      name: "App Secret",
      type: "password",
    }),
    facebook_access_token: field({
      name: "Access Token",
      type: "password",
    }),
  },

  sendgrid: {
    sendgrid_auth_token: {
      name: "Auth Token",
      type: "password",
      required: true,
      description: null,
    },
  },

  sfmc: {
    sfmc_account_id: field({ name: "Account ID" }),
    sfmc_auth_base_uri: field({ name: "Auth Base URI" }),
    sfmc_client_id: field({ name: "Client ID" }),
    sfmc_client_secret: field({ name: "Client Secret", type: "password" }),
    sfmc_rest_base_uri: field({ name: "REST Base URI" }),
    sfmc_soap_base_uri: field({ name: "Soap Base URI" }),
  },

  qualtrics: {
    qualtrics_data_center: field({ name: "Data Center" }),
    qualtrics_owner_id: field({ name: "Owner ID" }),
    qualtrics_directory_id: field({ name: "Directory ID" }),
    qualtrics_api_token: field({ name: "API Token", type: "password" }),
  },
}

/**
 * Destination data extensions
 *
 * @returns {Array} list of data extensions
 */
export const destinationsDataExtensions = () => {
  let dataExtensions = []
  for (let i = 0; i < 10; i++) {
    dataExtensions.push({
      name: faker.company.companyName(),
      data_extension_id: faker.datatype.uuid(),
      create_time: faker.date.past(),
    })
  }
  return dataExtensions
}

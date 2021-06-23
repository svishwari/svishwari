import faker from "faker"

/**
 * Destination schema
 */
export const destination = {
  name: "Facebook",
  type: "facebook",
  is_enabled: false,
  is_added: false,
  create_time: () => faker.date.recent(),
  created_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
  update_time: () => faker.date.recent(),
  updated_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
  engagements: () => faker.datatype.number({ min: 0, max: 10 }),
}

/**
 * Destination field schema
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
    facebook_access_token: field({
      name: "Access Token",
      type: "password",
    }),
    facebook_app_secret: field({
      name: "App Secret",
      type: "password",
    }),
  },

  salesforce: {
    sfmc_account_id: field({ name: "Account ID" }),
    sfmc_auth_base_uri: field({ name: "Auth Base URI" }),
    sfmc_client_id: field({ name: "Client ID" }),
    sfmc_client_secret: field({ name: "Client Secret", type: "password" }),
    sfmc_rest_base_uri: field({ name: "REST Base URI" }),
    sfmc_soap_base_uri: field({ name: "Soap Base URI" }),
  },
}

/**
 * Destination data extensions
 */
export const destinationsDataExtensions = () => {
  let dataExtensions = []
  for (let i = 0; i < 10; i++) {
    dataExtensions.push({
      data_extension_name: faker.company.companyName(),
      data_extension_id: faker.datatype.uuid(),
    })
  }
  return dataExtensions
}

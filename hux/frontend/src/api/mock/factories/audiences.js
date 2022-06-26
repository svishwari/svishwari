import faker from "faker"

import { pick } from "lodash"
import { customersOverview } from "./customers"

/**
 * Audience insights schema
 */
export const audienceInsights = pick(customersOverview, [
  "gender_men",
  "gender_women",
  "gender_other",
  "min_age",
  "max_age",
  "total_countries",
  "total_us_states",
  "total_cities",
  "total_customers",
])

const destinationData = () => {
  return {
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
}

const engagementData = () => {
  return {
    id: `${faker.datatype.number({ min: 1, max: 10 })}`,
    name: `Engagement ${faker.datatype.number({ min: 1, max: 10 })}`,
    status: "Delivered",
    description: `Engagement description for ${faker.address.state()}`,
    deliveries: [
      {
        id: "7",
        delivery_platform_id: "7",
        name: "Facebook",
        delivery_platform_type: "facebook",
        size: 20901,
        update_time: "2021-07-13T15:38:42.629Z",
        status: "Delivered",
        next_delivery: "2021-07-28T15:38:42.629Z",
        delivery_schedule_type: "Daily",
        match_rate: faker.datatype.number({ min: 0, max: 1, precision: 0.001 }),
        is_ad_platform: faker.datatype.boolean(),
        replace_audience: false,
      },
    ],
  }
}

const lookalikeAudience = () => {
  return {
    id: faker.datatype.number({ min: 1, max: 10 }),
    delivery_platform_id: "60b9601a6021710aa146df30",
    country: "US",
    audience_size_percentage: faker.datatype.float({
      min: 100,
      max: 1000,
      precision: 0.01,
    }),
    create_time: faker.date.recent(),
    update_time: faker.date.recent(),
    name: faker.fake("{{name.firstName}} {{name.lastName}}"),
    size: faker.datatype.number({ min: 10000000, max: 999999999 }),
    is_lookalike: true,
    delivery_platform_type: "facebook",
    delivery_platform_name: "Facebook",
    delivery_platform_link: "https://business.facebook.com/",
    status: () =>
      faker.random.arrayElement([
        "Delivered",
        "Delivering",
        "Not Delivered",
        "Error",
      ]),
    created_by: faker.fake("{{name.firstName}} {{name.lastName}}"),
    updated_by: faker.fake("{{name.firstName}} {{name.lastName}}"),
  }
}

const matchRate = () => {
  return {
    destination: faker.random.arrayElement([
      "facebook",
      "sendgrid",
      "google-ads",
      "aqfer",
    ]),
    match_rate: `${faker.datatype.number({ min: 0, max: 99 })}`,
    last_delivery: faker.date.recent(),
  }
}

const mockEngagements = (num = 3) => {
  return Array.from({ length: num }, engagementData)
}

const mockDestinations = (num = 3) => {
  return Array.from({ length: num }, destinationData)
}

const mockLookalikeAudiences = (num = 3) => {
  return Array.from({ length: num }, lookalikeAudience)
}

const mockMatchRates = (num = 3) => {
  return Array.from({ length: num }, matchRate)
}
/**
 * Audience schema
 */
export const audience = {
  name: (index) => `My audience ${index + 1}`,
  size: () => faker.datatype.number({ min: 10000000, max: 999999999 }),
  source_id: () => faker.datatype.number({ min: 1, max: 10 }),
  source_name: (index) => `My audience ${index + 1}`,
  source_size: () => faker.datatype.number({ min: 10000000, max: 999999999 }),
  status: () =>
    faker.random.arrayElement([
      "Delivered",
      "Delivering",
      "Not Delivered",
      "Error",
    ]),
  last_delivered: () => faker.date.recent(),
  create_time: () => faker.date.recent(),
  created_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
  update_time: () => faker.date.recent(),
  updated_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
  engagements: () => mockEngagements(faker.datatype.number({ min: 0, max: 5 })),
  destinations: () =>
    mockDestinations(faker.datatype.number({ min: 0, max: 5 })),
  is_lookalike: () => false,
  lookalikeable: () => faker.random.arrayElement(["Active"]),
  lookalike_audiences: () => mockLookalikeAudiences(5),
  digital_advertising: {
    match_rates: () =>
      mockMatchRates(faker.datatype.number({ min: 0, max: 3 })),
  },
  deliveries: [
    {
      delivery_platform_type: "sendgrid",
      delivery_platform_id: "2",
      status: "Delivered",
      last_delivered: faker.date.recent(),
      delivery_platform_name: "Sendgrid by Twilio",
    },
    {
      delivery_platform_type: "facebook",
      delivery_platform_id: "7",
      status: "Delivered",
      last_delivered: faker.date.recent(),
      delivery_platform_name: "Facebook",
    },
  ],
  standalone_deliveries: [
    {
      status: "Delivered",
      delivery_platform_id: "2",
      last_delivered: () => faker.date.recent(),
      delivery_platform_type: "sendgrid",
      delivery_platform_name: "Sendgrid by Twilio",
      size: 0,
      link: null,
      is_ad_platform: false,
      replace_audience: false,
    },
    {
      status: "Delivering",
      delivery_platform_id: "7",
      last_delivered: () => faker.date.recent(),
      delivery_platform_type: "facebook",
      delivery_platform_name: "Facebook",
      size: 0,
      link: "https://business.facebook.com/",
      is_ad_platform: true,
      replace_audience: false,
    },
  ],
  tags: {
    industry: ["automotive", "financial_services", "healthcare", "hospitality", "retail"],
  },
}

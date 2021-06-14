import faker from "faker"

const REDACTED = "++REDACTED++"

const somePercentage = () => {
  return faker.datatype.float({ min: 0.51, max: 0.99, precision: 0.000000001 })
}

const someScore = () => {
  return faker.datatype.float({ min: 0, max: 1, precision: 0.000000001 })
}

const someValue = () => {
  return faker.datatype.float({ min: 100, max: 1000, precision: 0.01 })
}

const idrBreakdown = (percentage) => {
  return {
    data_sources: [
      {
        id: "1",
        name: "Bluecore",
        percentage: percentage,
        type: "bluecore",
      },
    ],
    percentage: percentage,
  }
}

/**
 * Customer schema
 */
export const customer = {
  first_name: () => faker.name.firstName(),
  last_name: () => faker.name.lastName(),
  match_confidence: () => somePercentage(),
}

/**
 * Customer profile schema
 */
export const customerProfile = {
  first_name: () => customer.first_name(),
  last_name: () => customer.last_name(),
  match_confidence: () => customer.match_confidence(),

  address: REDACTED,
  age: REDACTED,
  churn_rate: () => someScore(),
  city: REDACTED,
  conversion_time: () => faker.datatype.number(365),
  email: REDACTED,
  gender: REDACTED,
  identity_resolution: {
    address: idrBreakdown(0.4),
    cookie: idrBreakdown(0.1),
    email: idrBreakdown(0.2),
    name: idrBreakdown(0.2),
    phone: idrBreakdown(0.1),
  },
  last_click: () => faker.date.recent(30),
  last_email_open: () => faker.date.recent(30),
  last_purchase: () => faker.date.recent(30),
  ltv_actual: someValue(),
  ltv_predicted: someValue(),
  phone: REDACTED,
  preference_email: faker.datatype.boolean(),
  preference_in_app: faker.datatype.boolean(),
  preference_push: faker.datatype.boolean(),
  preference_sms: faker.datatype.boolean(),
  propensity_to_purchase: someScore(),
  propensity_to_unsubscribe: someScore(),
  since: () => faker.date.past(20),
  state: REDACTED,
  zip: REDACTED,
}

/**
 * Customers overview schema
 */
export const customersOverview = {
  gender_men: 0.67621,
  gender_other: 0.8935,
  gender_women: 0.30828,
  match_rate: 0.5972,
  max_age: 35,
  max_ltv_actual: 90.4685,
  max_ltv_predicted: 94.574,
  min_age: 7,
  min_ltv_actual: 77.9244,
  min_ltv_predicted: 52.0197,
  total_cities: 48,
  total_countries: 3,
  total_customers: 23905153,
  total_household_ids: 33311636,
  total_individual_ids: 54080052,
  total_known_ids: 15270332,
  total_records: 20372628,
  total_unique_ids: 73374722,
  total_unknown_ids: 30637984,
  total_us_states: 16,
  updated: faker.date.recent(7),
}

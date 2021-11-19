import faker from "faker"
import { startCase } from "lodash"
import mapData from "@/components/common/MapChart/mapData.js"

const REDACTED = "++REDACTED++"

const someLastName = () => {
  const howLong = Math.floor(Math.random() * 4) + 1

  const lastName = Array(howLong)
    .fill()
    .reduce((prev) => prev + faker.name.lastName().toLowerCase(), "")

  return startCase(lastName)
}

const somePercentage = () => {
  return faker.datatype.float({ min: 0, max: 1, precision: 0.000000001 })
}

const someValue = () => {
  return faker.datatype.float({ min: 100, max: 1000, precision: 0.01 })
}

// Examples:
//              co-occurrences:
// identifier:  name address email phone cookie
//       name      0    5871  8916  2689  11975
//    address   7124       0  8241  5021   5202
//      email    912   6251      0  9150   4002
//      phone   4231   2104   5699     0   1924
//     cookie  11975   1324   1555  5929      0

const identifiers = ["name", "address", "email", "phone", "cookie"]

const cooccurrenceMatrix = [
  [0, 5871, 8916, 2689, 11975],
  [7124, 0, 8241, 5021, 5202],
  [912, 6251, 0, 9150, 4002],
  [4231, 2104, 5699, 0, 1924],
  [11975, 1324, 1555, 5929, 0],
]

const cooccurrencesTotal = cooccurrenceMatrix.flat().reduce((a, b) => a + b, 0)

const cooccurrenceItem = (identifier, cooccurence) => {
  const identifierIndex = identifiers.findIndex((val) => val === identifier)
  const cooccurenceIndex = identifiers.findIndex((val) => val === cooccurence)
  const count = cooccurrenceMatrix[identifierIndex][cooccurenceIndex]
  return {
    identifier: cooccurence,
    count: count,
    percentage: count / cooccurrencesTotal,
  }
}

const idrBreakdown = (identifier, percentage) => {
  return {
    cooccurrences: identifiers.map((cooccurence) => {
      return cooccurrenceItem(identifier, cooccurence)
    }),
    count: Math.round(percentage * cooccurrencesTotal),
    data_sources: [
      {
        id: "1",
        name: "Bluecore",
        type: "bluecore",
        percentage: 0.45,
      },
      {
        id: "2",
        name: "Netsuite",
        type: "netsuite",
        percentage: 0.65,
      },
    ],
    icon: identifier,
    percentage: percentage,
    prop: startCase(identifier),
  }
}

/**
 * Customer schema
 */
export const customer = {
  hux_id: (index) => `HUX${index + 1000000000000001}`,
  first_name: () => faker.name.firstName(),
  last_name: () => someLastName(),
  match_confidence: () => somePercentage(),
}

/**
 * Customer profile schema
 */
export const customerProfile = {
  insights: {
    address: REDACTED,
    age: REDACTED,
    city: REDACTED,
    email: REDACTED,
    gender: REDACTED,
    phone: REDACTED,
    state: REDACTED,
    zip: REDACTED,
  },

  contact_preferences: {
    preference_email: faker.datatype.boolean(),
    preference_in_app: faker.datatype.boolean(),
    preference_push: faker.datatype.boolean(),
    preference_sms: faker.datatype.boolean(),
  },

  overview: {
    ...customer, // extends base customer
    churn_rate: () => faker.datatype.number(1, 10),
    conversion_time: () =>
      faker.datatype.float({ min: 1, max: 24, precision: 0.01 }),
    last_click: () => faker.date.recent(30),
    last_email_open: () => faker.date.recent(30),
    last_purchase: () => faker.date.recent(30),
    ltv_actual: someValue(),
    ltv_predicted: someValue(),
    since: () => faker.date.past(20),
  },

  identity_resolution: {
    name: idrBreakdown("name", 0.2),
    address: idrBreakdown("address", 0.4),
    email: idrBreakdown("email", 0.2),
    phone: idrBreakdown("phone", 0.1),
    cookie: idrBreakdown("cookie", 0.1),
  },

  pii_access: () =>
  faker.random.arrayElement([
    true,
    false,
  ]),
}

/**
 * Customers overview schema
 */
export const customersOverview = {
  gender_men: 0.67621,
  gender_other: 0,
  gender_women: 0.30828,
  gender_men_count: 16016452,
  gender_women_count: 7171545,
  gender_other_count: 0,
  match_rate: 0.5972,
  max_age: 35,
  max_ltv_actual: 90.4685,
  max_ltv_predicted: 94.574,
  min_age: 7,
  min_ltv_actual: 77.9244,
  min_ltv_predicted: 52.0197,
  total_cities: 14659,
  total_countries: 1,
  total_customers: 23905153,
  total_household_ids: 33311636,
  total_individual_ids: 54080052,
  total_known_ids: 15270332,
  total_records: 20372628,
  total_unique_ids: 73374722,
  total_unknown_ids: 0,
  total_us_states: 52,
  updated: faker.date.recent(7),
  geo: mapData,
}

/**
 * City-level geographic insights schema
 */
export const geoCity = {
  city: () => faker.address.city(),
  state: () => faker.address.stateAbbr(),
  size: () => faker.datatype.number(1000),
  spending: () => faker.datatype.number(10000),
  country: () => faker.random.arrayElement(["US", "CA"]),
}

/**
 * Country-level geographic insights schema
 */
export const geoCountry = {
  country: () => faker.random.arrayElement(["US", "CA"]),
  size: () => faker.datatype.number(100000),
  spending: () => faker.datatype.number(1000000),
}

/**
 * State-level geographic insights schema
 */
export const geoState = {
  state: () => faker.address.state(),
  size: () => faker.datatype.number(10000),
  spending: () => faker.datatype.number(100000),
  country: () => faker.random.arrayElement(["US", "CA"]),
}

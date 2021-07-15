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

/**
 * Audience schema
 */
export const audience = {
  name: (index) => `My audience ${index + 1}`,
  size: () => faker.datatype.number({ min: 10000000, max: 999999999 }),
  last_delivered: () => faker.date.recent(),
  create_time: () => faker.date.recent(),
  created_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
  update_time: () => faker.date.recent(),
  updated_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
  lookalike_audience: () => true,
}

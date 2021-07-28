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

const engagementData = () => {
  return {
    id: `${faker.datatype.number({ min: 1, max: 10 })}`,
    name: `Engagement ${faker.datatype.number({ min: 1, max: 10 })}`,
    status: "Delivered",
    description: `Engagement description for ${faker.address.state()}`,
    deliveries: [
      {
        id: "7",
        name: "Facebook",
        type: "facebook",
        size: 20901,
        update_time: "2021-07-13T15:38:42.629Z",
        status: "Delivered",
        next_delivery: "2021-07-28T15:38:42.629Z",
        delivery_schedule_type: "Daily",
      },
    ],
  }
}
const mockEngagements = (num = 3) => {
  return Array.from({ length: num }, engagementData)
}

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
  engagements: () => mockEngagements(2),
}

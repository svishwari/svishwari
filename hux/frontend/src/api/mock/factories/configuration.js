import faker from "faker"

export default {
  status: () => faker.random.arrayElement(["active", "pending"]),
  icon: () =>
    faker.random.arrayElement([
      "uncategorised",
      "commerce_personal",
      "digital_advertising",
      "email_deliverability",
      "experience_data_platform",
      "insight_iq",
    ]),
  name: (index) => `Category ${index + 1}`,
  enabled: faker.datatype.boolean(),
  roadmap: faker.datatype.boolean(),
  created_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
  create_time: () => faker.date.recent(),
  update_time: () => faker.date.recent(),
  type: "module",
  description: `description for ${faker.address.state()}`,
}

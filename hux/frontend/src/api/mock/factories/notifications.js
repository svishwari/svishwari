import faker from "faker"

/**
 * Notification schema
 */
export const notification = {
  created: () => faker.date.recent(),
  description: () =>
    `New engagement named "${faker.address.state()}" created by "${faker.name.findName()}".`,
  notification_type: () => "Success",
  category: () => "Orchestration",
  username: () => `User ${faker.datatype.number({ min: 1, max: 10000 })}`,
}

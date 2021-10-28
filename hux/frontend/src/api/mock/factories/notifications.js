import faker from "faker"

/**
 * Notification schema
 */
export const notification = {
  id: () => faker.datatype.uuid(),
  created: () => faker.date.recent(),
  description: () =>
    `New engagement named "${faker.address.state()}" created by "${faker.name.findName()}".`,
  notification_type: () => "Success",
  category: () => "Orchestration",
}

import faker from "faker"

/**
 * Notification schema
 */
export const notification = {
  id: () => faker.datatype.uuid(),
  create_time: () => faker.date.recent(),
  description: () =>
    `New engagement named "${faker.address.state()}" created by "${faker.name.findName()}".`,
  notification_type: () => faker.random.arrayElement(["critical", "success"]),
  category: () =>
    faker.random.arrayElement(["destinations", "data_sources", "models"]),
  username: () => faker.name.findName(),
}

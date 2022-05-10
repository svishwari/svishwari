import faker from "faker"

/**
 * Notification schema
 */
export const notification = {
  id: () => faker.datatype.uuid(),
  create_time: () => faker.date.recent(),
  description: () =>
    `New engagement named "${faker.address.state()}" created by "${faker.name.findName()}".`,
  notification_type: () => "success",
  category: () => "data_sources",
  username: () => faker.name.findName(),
}

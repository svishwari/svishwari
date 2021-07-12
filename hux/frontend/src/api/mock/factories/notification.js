import faker from "faker"

/**
 * Notification schema
 */
export const notification = {
  created: () => faker.date.recent(),
  description: () => "Data Source CS005 lost connection.",
  notification_type: () => "Success",
  category: () => "Orchestration",
}

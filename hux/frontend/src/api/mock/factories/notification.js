import faker from "faker"

/**
 * Notification schema
 */
export const notification = {
  time: () => faker.date.recent(),
  description: () => 'Data Source CS005 lost connection.',
  type: () => 'Success',
  category: () => 'Orchestration'
}


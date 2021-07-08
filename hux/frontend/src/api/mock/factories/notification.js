import faker from "faker"

/**
 * Notification schema
 */
export const notification = {
  time: () => faker.date.recent(),
  description: () => 'alert data',
  type: () => 'Success',
  category: () => 'Orchestration'
}


import faker from "faker"
const ls = JSON.parse(window.localStorage.vuex || "{}")
const profile = ls.users?.userProfile || {
  firstName: "Sarah",
  lastName: "Huxly",
}

/**
 * User Schema
 */
export const user = {
  email: profile.email,
  display_name: profile.firstName,
  first_name: profile.firstName,
  last_name: profile.lastName,
  role: "admin",
  organization: faker.company.companyName(),
  subscriptions: [],
  dashboard_configuration: {},
  favorites: {
    campaigns: [],
    destinations: [],
    engagements: [],
    audiences: [],
  },
  profile_photo: faker.image.imageUrl(),
  login_count: 0,
  modified: faker.date.recent(),
  pii_access: true,
  access_level: "Admin",
  alerts: {
    orchestration: {
      delivery: {
        informational: true,
        success: false,
        critical: false,
      },
      audiences: {
        informational: true,
        success: false,
        critical: false,
      },
      destinations: {
        informational: true,
        success: false,
        critical: false,
      },
      engagements: {
        informational: true,
        success: false,
        critical: false,
      },
    },
    decisioning: {
      models: {
        informational: true,
        success: false,
        critical: false,
      },
    },
    data_management: {
      data_sources: {
        informational: false,
        success: false,
        critical: false,
      },
    },
  },
  demo_config: {
      demo_mode: true,
      industry: "Automotive",
      description: "Pharmaceutical",
      target: "Physicians",
      track: "Sales"
  }
}

export const requestedUser = [
  {
    email: faker.internet.email(),
    pii_access: faker.random.arrayElement([true, false]),
    display_name: faker.name.findName(),
    access_level: faker.random.arrayElement(["admin", "viewer", "editor"]),
    status: faker.random.arrayElement([
      "To Do",
      "In Progress",
      "In Review",
      "Done",
    ]),
    created: faker.date.recent(),
    updated: faker.date.recent(),
  },
]

/**
 * A single ticket schema
 *
 * @returns {object} ticket
 */
const ticket = () => {
  return {
    status: faker.random.arrayElement([
      "To do",
      "In progress",
      "In review",
      "Done",
    ]),

    id: faker.datatype.number(),

    key: `HUS-${faker.datatype.number({ min: 1000, max: 3000 })}`,

    summary: faker.lorem.words(3),

    create_time: faker.date.recent(),
  }
}

/**
 * Users tickets schema
 *
 * @returns {object} tickets response schema
 */
export const someTickets = () => {
  let num = faker.datatype.number({ min: 5, max: 10 })

  return Array.from({ length: num }, () => ticket())
}

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

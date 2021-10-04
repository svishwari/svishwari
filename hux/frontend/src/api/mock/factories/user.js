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
  email: faker.internet.email(),
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
}

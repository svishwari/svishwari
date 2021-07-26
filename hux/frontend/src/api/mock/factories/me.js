const ls = JSON.parse(window.localStorage.vuex || "{}")
const profile = ls.users?.userProfile || {
  firstName: "Sarah",
  lastName: "Huxly",
}

/**
 * Me schema
 */
export const me = {
  first_name: profile.firstName,
  last_name: profile.lastName,
  full_name: () => `${profile.firstName} ${profile.lastName}`,
}

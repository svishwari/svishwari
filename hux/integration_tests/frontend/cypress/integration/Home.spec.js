import route from "../support/routes.js"
import selector from "../support/selectors.js"

describe("Home", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should have a welcome banner", () => {
    let currentUser = {}
    cy.location("pathname").should("eq", route.home)
    cy.window().then((window) => {
      currentUser = JSON.parse(window.localStorage.getItem("vuex")).users
        .userProfile
      cy.get(selector.home.welcomeBanner).contains(
        currentUser.firstName + " " + currentUser.lastName,
      )
    })
  })

  it("should have a total customers chart", () => {
    cy.get(selector.home.totalCustomersChart)
      .its("length")
      .should("gt", 0)
  })

  it("should have the latest alerts and notifications", () => {
    cy.get(selector.home.latestNotifications).should("exist")

    cy.get(selector.home.latestNotifications).find("table tr")
      .its("length")
      .should("gt", 1)

    cy.get(selector.home.latestNotifications).find("h3")
      .contains("Latest alerts")

    cy.get(selector.home.allNotificationsLink)
      .should("have.attr", "href")
      .and("include", route.notifications)
  })
})

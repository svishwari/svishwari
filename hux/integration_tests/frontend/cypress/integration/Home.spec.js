import route from "../support/routes.js"
import selector from "../support/selectors.js"

describe("Home", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.home)
  })

  it("should have a welcome banner", () => {
    let currentUser = {}

    cy.window().then((window) => {
      currentUser = JSON.parse(window.localStorage.getItem("vuex")).users
        .userProfile
      cy.get(selector.home.welcomeBanner).contains(
        currentUser.firstName + " " + currentUser.lastName,
      )
    })
  })

  it("should have a total customers chart", () => {
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(5000)
    cy.get(selector.home.totalCustomersChart).its("length").should("gt", 0)
  })

  it("should have the latest alerts and notifications", () => {
    cy.get(selector.home.latestNotifications).should("exist")

    cy.get(selector.home.latestNotifications)
      .find("table tr")
      .its("length")
      .should("gt", 1)

    cy.get(selector.home.latestNotifications)
      .find("h3")
      .contains("Latest alerts")
    cy.get(selector.home.homeAlertIdClick).eq(1).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.home.allNotificationsLink)
      .should("have.attr", "href")
      .and("include", route.notifications)
    cy.get(selector.home.demoScriptClick).click()
  })
})

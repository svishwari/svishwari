import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Orchestration > Destinations", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  // TODO in HUS-1373 after HUS-1230 is merged
  it("should be able to manage destinations", () => {
    cy.location("pathname").should("eq", route.home)

    //click on connections on side nav bar
    cy.get(selector.nav.destinations).click()
    cy.location("pathname").should("eq", route.destinations)

    //validate destinations exist by getting total no. of them
    cy.get(selector.destinations).its("length").should("be.gt", 0)

    cy.get(selector.destinations).eq(0).get(".mdi-dots-vertical").eq(0).click()

    cy.get(selector.destination.destinationRemove).eq(0).click()
    cy.get(selector.destination.destinationRemoveConfirmBody).then(
      ($modalBody) => {
        if (
          $modalBody.find(selector.destination.removeDestinationText).length > 0
        ) {
          cy.get(selector.destination.destinationRemoveConfirmFooter)
            .get("button")
            .contains("Yes, remove it")
            .eq(0)
            .contains("v-btn--disabled")

          cy.get(selector.destination.removeDestinationText)
            .eq(1)
            .type("confirm")
        }
      },
    )
    cy.get(selector.destination.destinationRemoveConfirmFooter)
      .get("button")
      .contains("Yes, remove it")
      .eq(0)
      .should("not.contain", "v-btn--disabled")

    cy.get(selector.destination.destinationRemoveConfirmFooter)
      .get("button")
      .contains("Nevermind!")
      .eq(0)
      .click()

    //click on plus-sign for adding a destination
    cy.get(selector.destination.addDestination).click()
    cy.location("pathname").should("eq", route.addDestinations)

    //find a addable destination from the drawer
    cy.get(selector.destination.drawerToggle).click()
    cy.get(selector.destination.destinationsList)
      .contains("Add")
      .as("addableDestinations")

    cy.get("@addableDestinations")
      .its("length")
      .then((addableDestinations) => {
        if (addableDestinations > 0) {
          //if a destination can be added

          cy.get("@addableDestinations").eq(0).click()

          //configure destination details
          cy.get(selector.destination.destinationConfigDetails)
            .get("input")
            .each(($el) => {
              cy.wrap($el).type("123456")
            })
          cy.get(selector.destination.validateDestination).click()
          cy.get(selector.destination.validateDestination).contains("Success")

          //Click on Add and return button
          cy.get(selector.destination.footer).contains("return").click()
          cy.location("pathname").should("eq", route.destinations)
        }
      })

    //click on plus-sign for requesting a destination
    cy.get(selector.destination.addDestination).click()
    cy.location("pathname").should("eq", route.addDestinations)

    cy.get(selector.destination.drawerToggle).click()
    cy.get(selector.destination.requestableDestinationsList)
      .contains("Request")
      .as("requestableDestinations")

    cy.get("@requestableDestinations")
      .its("length")
      .then((requestableDestinations) => {
        if (requestableDestinations > 0) {
          cy.get("@requestableDestinations").eq(0).click().contains("Requested")
        }
      })
  })
})

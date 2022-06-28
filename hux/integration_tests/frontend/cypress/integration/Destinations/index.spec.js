import route from "../../support/routes"
import selector from "../../support/selectors"

describe("Orchestration > Destinations", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.destinations)
  })

  it("should be able to manage destinations", () => {
    cy.location("pathname").should("eq", route.destinations)
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    // validate destinations exist by getting total no. of them
    cy.get(selector.datasource.destinations).its("length").should("be.gt", 0)

    cy.get(selector.datasource.destinations)
      .eq(0)
      .get(".mdi-dots-vertical")
      .eq(0)
      .click()

    cy.get(selector.destination.destinationRemove).last().eq(0).click()
    cy.get(selector.destination.destinationRemoveConfirmBody).then(
      ($modalBody) => {
        if (
          $modalBody.find(selector.destination.removeDestinationText).length > 0
        ) {
          cy.get(selector.destination.destinationRemoveConfirmFooter)
            .find("button")
            .contains("Yes, remove it")
            .should("exist")

          cy.get(selector.destination.removeDestinationText)
            .eq(1)
            .type("confirm")
        }
      },
    )
    cy.get(selector.destination.destinationRemoveConfirmFooter)
      .find("button")
      .contains("Yes, remove it")
      .eq(0)
      .should("not.contain", "v-btn--disabled")

    cy.get(selector.destination.destinationRemoveConfirmFooter)
      .find("button")
      .contains("Nevermind!")
      .eq(0)
      .click()

    // click on plus-sign for adding a destination
    cy.get(selector.destination.addDestination).click()
    cy.location("pathname").should("eq", route.addDestinations)

    // find a addable destination from the drawer
    cy.get(selector.destination.drawerToggle).click()
    cy.get(selector.destination.destinationsList).contains(/\bAdd\b/g)

    // find a requestable destination from the drawer
    cy.get(selector.destination.requestableDestinationsList)
      .contains(/\bRequest\b/g)
      .as("requestableDestinations")

    cy.get("@requestableDestinations")
      .its("length")
      .then((requestableDestinations) => {
        if (requestableDestinations > 0) {
          cy.get("@requestableDestinations").eq(0).click()
          cy.get(selector.destination.cancelRequestDestination).click()
          cy.location("pathname").should("eq", route.destinations)
        }
      })
  })
})

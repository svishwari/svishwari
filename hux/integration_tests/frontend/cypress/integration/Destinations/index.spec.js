import route from "../../support/routes"
import selector from "../../support/selectors"

describe("Orchestration > Destinations", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.destinations)
  })

  it("should be able to manage destinations", () => {
    cy.location("pathname").should("eq", route.destinations)

    // validate destinations exist by getting total no. of them
    cy.get(selector.destinations).its("length").should("be.gt", 0)

    cy.get(selector.destinations).eq(0).get(".mdi-dots-vertical").eq(0).click()

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
    cy.get(selector.destination.destinationsList)
      .contains(/\bAdd\b/g)
      .as("addableDestinations")

    cy.get("@addableDestinations")
      .its("length")
      .then((addableDestinations) => {
        //if a destination can be added, try to add it
        if (addableDestinations > 0) {
          // eslint-disable-next-line cypress/no-unnecessary-waiting
          cy.wait(2000)
          cy.get("@addableDestinations").eq(0).click()
          // eslint-disable-next-line cypress/no-unnecessary-waiting
          cy.wait(2000)

          // configure destination details
          cy.get(selector.destination.destinationConfigDetails)
            .get("input")
            .each(($el, index) => {
              if (index < 5) {
                cy.wrap($el).type("123456")
              }
            })
          cy.get(selector.destination.validateDestination).click()
          cy.get(selector.destination.footer).contains("Cancel").click()
          cy.location("pathname").should("eq", route.destinations)
        }
      })

    // click on plus-sign for requesting a destination
    cy.get(selector.destination.addDestination).click()
    cy.location("pathname").should("eq", route.addDestinations)

    cy.get(selector.destination.drawerToggle).click()
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

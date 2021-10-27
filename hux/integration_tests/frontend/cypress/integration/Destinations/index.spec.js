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
  it.skip("should be able to manage destinations", () => {
    cy.location("pathname").should("eq", route.overview)

    //click on connections on side nav bar
    cy.get(selector.connections).eq(1).click()
    cy.location("pathname").should("eq", route.connections)

    cy.get(selector.destination.removeDots).eq(0).click()
    cy.get(selector.destination.destinationRemove).eq(0).click()
    cy.get(selector.destination.destinationRemoveConfirm)
      .get("button")
      .contains("Nevermind!")
      .eq(0)
      .click()

    //validate destinations exist by getting total no. of them
    cy.get(selector.destinations).its("length").as("destinationsCount")

    //click on plus-sign for adding a destination
    cy.get(selector.destination.addDestination).click()
    cy.location("pathname").should("eq", route.addDestinations)

    /**
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
          cy.location("pathname").should("eq", route.connections)

          //verify if number of destinations incremented by 1
          cy.get("@destinationsCount").then((destinationsCount) => {
            cy.get(selector.destinations)
              .its("length")
              .should("eq", destinationsCount + 1)
          })
        } else {
          //if no destination can be added, cancel adding a destination
          cy.get(selector.destination.footer).contains("Cancel").click()

          //verify no change in number of destinations
          cy.get("@destinationsCount").then((destinationsCount) => {
            cy.get(selector.destinations)
              .its("length")
              .should("eq", destinationsCount)
          })
        }
      })
    */
  })
})

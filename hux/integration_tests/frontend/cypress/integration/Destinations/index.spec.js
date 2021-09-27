import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Tests data souces and destinations in connections", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("testing data management > connections > destinations", () => {
    cy.location("pathname").should("eq", route.overview)

    //click on connections on side nav bar
    cy.get(selector.connections).eq(0).click()
    cy.location("pathname").should("eq", route.connections)

    //validate destinations exist by getting total no. of them
    cy.get(selector.destinations).its("length").as("destinationsCount")

    //add a destination if possible
    cy.get(selector.destination.addDestination).click()
    cy.location("pathname").should("eq", route.addDestinations)
    cy.get(selector.destination.drawerToggle).click()
    cy.get(selector.destination.destinationsList).contains("Add").as("addableDestinations")
    
    cy.get("@addableDestinations").its("length").then((addableDestinations) => {
        if(addableDestinations > 0){
            cy.get("@addableDestinations").eq(0).click()
            cy.get(selector.destination.destinationConfigDetails).get("input").each(($el) => {
                cy.wrap($el).type("123456")
            })
            cy.get(selector.destination.validateDestination).click()
            cy.get(selector.destination.validateDestination).contains("Success")
            cy.get(selector.destination.footer).contains("return").click()
            cy.wait(1000)

            cy.location("pathname").should("eq", route.connections)
            cy.get("@destinationsCount").then((destinationsCount) => {
                cy.get(selector.destinations).its("length").should("eq",destinationsCount + 1)
            })
        }
        else{
            cy.get(selector.destination.footer).contains("Cancel").click()
            cy.get("@destinationsCount").then((destinationsCount) => {
                cy.get(selector.destinations).its("length").should("eq",destinationsCount)
            })
        }
    })
  })

  it("testing data management > connections > datasources", () => {
    cy.location("pathname").should("eq", route.connections)
    cy.get(selector.datasources).its("length").should("be.gt", 0)
  })
})

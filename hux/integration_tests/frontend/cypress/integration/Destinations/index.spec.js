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
            //if a destination can be added
            cy.get("@addableDestinations").eq(0).click()

            //configure destination
            cy.get(selector.destination.destinationConfigDetails).get("input").each(($el) => {
                cy.wrap($el).type("123456")
            })
            cy.get(selector.destination.validateDestination).click()
            cy.get(selector.destination.validateDestination).contains("Success")

            //Add and return
            cy.get(selector.destination.footer).contains("return").click()
            cy.location("pathname").should("eq", route.connections)

            //verify if number of destinations incremented by 1
            cy.get("@destinationsCount").then((destinationsCount) => {
                cy.get(selector.destinations).its("length").should("eq",destinationsCount + 1)
            })
        }
        else{
            //if no destination can be added, cancel
            cy.get(selector.destination.footer).contains("Cancel").click()

            //verify no change in number of destinations
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
